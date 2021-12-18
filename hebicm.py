import pathlib
import imghdr
from typing import List

import discord
from discord.ext import commands
import os
import re
import asyncio
import aiohttp
import pandas as pd
import util


class Hebi(commands.Cog):
    def __init__(self, bot):
        self._ask: str = 'ask'
        self._answer: str = 'answer'
        self._command: str = 'command'
        self._csv_file: str = "/home/user/btsync/hebi.csv"
        self.bot = bot
        self._df: pd.DataFrame = None

        self._hebi_commands: dict = {}
        self.load_csv()
        self.set_hebi_commands()

        self._timeout_message = self._df.at['@timeout_message', self._answer]
        self._what_message = self._df.at['@what_message', self._answer]
        self._learn_message = self._df.at['@learn_message', self._answer]
        self._bot_setmes_help_message = self._df.at['@setmes_help_message',
                                                    self._answer]
        self._chmes_success_message = self._df.at['@chmes_success_message',
                                                  self._answer]
        self._chmes_fail_message = self._df.at['@chmes_fail_message', self.
                                               _answer]
        self._unknown_message = self._df.at['@unknown_command_message', self.
                                            _answer]

    def load_csv(self):
        """load csv file to pandas DataFrame

        Returns:
            bool: if load error has return False
        """
        try:
            self._df = pd.read_csv(self._csv_file, index_col=0)
        except pd.io.common.EmptyDataError as e:
            print(e)
            return False
        self._df.sort_values(self._ask, inplace=True)
        print(self._df.info())

    def set_hebi_commands(self):
        """set self.hebi_commands dict
        """
        self._hebi_commands = {
            'base_command': {
                'pattern': r'(.*)\(.*\)',
                'function': None,
                'description': 'このコマンドは利用できません'
            },
            'send_file': {
                'pattern':
                r'send_file\(\"(.*)\"\)',
                'function':
                self.bot_command_send_file,
                'description':
                '[send_file ファイルパス] ローカル用コマンドなので \
                                !setmes ではファイルを指定できません'
            },
            'open_url_image': {
                'pattern':
                r'open_url_image\(\"(.*)\"\)',
                'function':
                self.bot_command_open_url_image,
                'description':
                '[open_url_image 画像のURL] 指定されたURLの画像を\
                                メッセージの後貼り付けます'
            },
            'send_url': {
                'pattern':
                r'send_url\(\"(.*)\"\)',
                'function':
                self.bot_command_send_url,
                'description':
                '[send_url 指定URL] 指定されたURLを\
                                メッセージの後貼り付けます'
            },
            'weather': {
                'pattern':
                r'weather\(\"(.*)\"\)',
                'function':
                self.bot_command_weather,
                'description':
                '[weather 都市コード] 指定コードの天気を貼り付けます\
                    　コードはこちらで確認してください。\
                    http://weather.livedoor.com/forecast/rss/primary_area.xml'
            }
        }

    def get_command(self, command_str: str):
        """get a command dict from self.hebi_commands

        Args:
            command_str (str): command string

        Returns:
            dict: one command dict or None
        """
        m = re.search(
            self._hebi_commands.get('base_command', {}).get('pattern'),
            command_str)
        if m is None:
            return None
        command_name = m.group(1)
        if command_name not in self._hebi_commands:
            return None
        return self._hebi_commands[command_name]

    @commands.command()
    async def help(self, ctx):
        """send help message to user dm

        Args:
            ctx (discord context): context
        """
        dm_user = self.bot.get_user(ctx.message.author.id)
        dm = await dm_user.create_dm()
        embed = discord.Embed(title="コマンドのヘルプ", color=0x26de12)
        embed.add_field(name='!help', value='ヘルプ', inline=False)
        embed.add_field(name='!hebi', value='へびが20秒間コメントを待ちます', inline=False)
        embed.add_field(name='!omikuji', value='おみくじする', inline=False)
        embed.add_field(
            name='!h [message]', value='[message] をへびに送信', inline=False)
        embed.add_field(name='!p', value='現在のDrawpileユーザー一覧を表示', inline=False)

        embed.add_field(
            name='!activity [name]',
            value='へびのプレイ中のゲームを [name] にする',
            inline=False)
        embed.add_field(
            name='!setmes [ask] [answer]',
            value='[ask] 覚えさせたい(修正したい)言葉 [answer] その返答',
            inline=False)
        embed.add_field(
            name='!setmes [ask] [answer] [command] [value]',
            value='メッセージにコマンドを含む場合は [command] 命令文 \
                [value] 文字列 を !setmes に加えてください',
            inline=False)
        embed.add_field(
            name='!listcommand', value='メッセージに使えるコマンド一覧を表示', inline=False)
        embed.add_field(
            name='[補足]',
            value='空白を含む文章は \" \" で囲みましょう　\
                そうしないとバラバラのメッセージと受け取られます',
            inline=False)
        await dm.send(content=None, embed=embed)

    @commands.command()
    async def listcommand(self, ctx):
        """list a command to user dm

        Args:
            ctx (discord context): context
        """
        dm_user = self.bot.get_user(ctx.message.author.id)
        dm = await dm_user.create_dm()
        embed = discord.Embed(title='メッセージで使えるコマンド一覧', color=0x26de12)
        for d in self._hebi_commands:
            embed.add_field(
                name=d,
                value=self._hebi_commands[d]['description'],
                inline=False)
        await dm.send(content=None, embed=embed)

    @commands.command()
    async def setmes(self, ctx, *messages):
        """change or set message to bot

        Args:
            ctx (discord context): context
            :param ctx: discord channel context
            :type messages: str
        """
        mes_num: int = len(messages)
        if mes_num != 2 and mes_num != 4:
            await ctx.send(self._bot_setmes_help_message)
            return

        command_strings: str = 'none'

        if mes_num == 4:
            command_strings = '{0}(\"{1}\")'.format(messages[2], messages[3])
            if self.get_command(command_strings) is None:
                await ctx.send(self._unknown_message)
                return

        new_strings: List[str] = [messages[0], messages[1], command_strings]

        if messages[0] in self._df.index:
            self._df.loc[new_strings[0]] = [new_strings[1], new_strings[2]]
            if util.write_new_word_csv(self._df, self._csv_file):
                await ctx.send(self._chmes_success_message)
            else:
                await ctx.send(self._chmes_fail_message)
            return
        else:
            if util.write_word_csv(new_strings, self._csv_file):
                self._df.loc[new_strings[0]] = [new_strings[1], new_strings[2]]
                await ctx.send(self._learn_message)
            return

    @commands.command()
    async def activity(self, ctx, *, message=' '):
        """change bot activity to message

        Args:
            ctx (discord context): context
            message (str, optional): Defaults to ' '. new activity name string
        """
        if message == ' ':
            return
        await self.bot.change_presence(activity=discord.Game(name=message))

    @commands.command()
    async def test(self, ctx):
        """test bot command

        Args:
            ctx (discord context): context
        """
        emoji = discord.utils.get(self.bot.emojis, name='hebi')
        if emoji:
            await ctx.message.add_reaction(emoji)

    @commands.command()
    async def reload(self, ctx):
        """bot message DataFrame reload

        Args:
            ctx (discord context): context
        """
        self._df.drop(self._df.index, inplace=True)
        self.load_csv()
        return

    @commands.command()
    async def p(self, ctx):
        url: str = "http://localhost:27780/api/sessions/"
        session_data = []
        output: str = '**Drawpileサーバーユーザー一覧**\n\n'
        message: str = 'Drawpileサーバーからの応答なし'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        api_data1 = await resp.json()
                    else:
                        await ctx.send(message)
                        return False
        except aiohttp.InvalidURL as e:
            print(e)
            return False

        for d in api_data1:
            title = d['title']
            url = 'http://localhost:27780/api/sessions/{0}/'.format(d['id'])
            session_data.append([title, url])

        for sd in session_data:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(sd[1]) as resp:
                        if resp.status == 200:
                            api_data2 = await resp.json()
                        else:
                            await ctx.send(message)
                            return False
            except aiohttp.InvalidURL as e:
                print(e)
                return False

            output += '__{0}__\n'.format(sd[0])
            for dd in api_data2['listings']:
                output += '[roomcode: {0}]\n'.format(dd['roomcode'])
            for dd in api_data2['users']:
                if dd['online']:
                    output += '{0}\n'.format(dd['name'])
            output += '\n'

        await ctx.send(output)

    @commands.command()
    async def hebi(self, ctx):
        """bot wait for message until 20 seconds

        Args:
            ctx (discord context): context

        Returns:
            bool: command success result
        """
        await ctx.send(self._what_message)

        def check_hebi(m):
            if m.author == self.bot.user or ctx.message.author != m.author:
                return False
            elif m.content in self._df.index:
                return True
            else:
                return False

        try:
            msg = await self.bot.wait_for(
                'message', check=check_hebi, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send(self._timeout_message)
            return

        await ctx.send(self._df.at[msg.content, self._answer])

        command_str = self._df.at[msg.content, self._command]
        if command_str != "none":
            await self.hebi_commands_run(ctx, command_str)

    @commands.command()
    async def h(self, ctx, *, message=' '):
        """send a message to bot

        Args:
            ctx (discord context): context
            message (str, optional): Defaults to ' '. message to bot
        """
        if message == ' ':
            return

        if message not in self._df.index:
            return

        await ctx.send(self._df.at[message, self._answer])
        command_str = self._df.at[message, self._command]

        if command_str != 'none':
            await self.hebi_commands_run(ctx, command_str)

    async def hebi_commands_run(self, ctx, command_str):
        """hebi bot command execute

        Args:
            ctx (channel context): discord channel context
            command_str (str): command strings

        Returns:
            bool: command execute success?
        """
        command_error_message: str = 'HEBI_ERROR: hebi command error'

        command: dict = self.get_command(command_str)
        if command is None:
            print(command_error_message)
            return False

        mob = re.search(command.get('pattern'), command_str)
        if mob is None:
            print(command_error_message)
            return False

        try:
            is_success = await command['function'](ctx, mob)
        except KeyError as e:
            print(e)
            return False

        if is_success:
            print(command_str)
        else:
            print(command_error_message)
            return False

    async def bot_command_send_file(self, ctx, mob=None):
        """send file command call from hebi_commands_run

        Args:
            ctx (discord context): context
            mob (Match Object, optional): Defaults to None.
            command string match objects
        Returns:
            bool: if has error return False
        """
        if mob is None:
            return False

        send_file_not_found_message = 'HEBI_ERROR: Send file not found'
        path = mob.group(1)
        file_path = pathlib.Path(path)

        if file_path.exists():
            await ctx.send(file=discord.File(mob.group(1)))
            return True
        else:
            print(send_file_not_found_message)
            return False

    async def bot_command_send_url(self, ctx, mob=None):
        """send url message command call from hebi_commands_run

        Args:
            ctx (discord context): context
            mob (Match Object, optional): Defaults to None.
            command string match objects
        Returns:
            bool: if has error return False
        """
        if mob is None:
            return False
        await ctx.send(mob.group(1))
        return True

    async def bot_command_open_url_image(self, ctx, mob=None):
        """download image from url then send a file
        command call from hebi_commands_run

        Args:
            ctx (discord context): context
            mob (Match Object, optional): Defaults to None.
            command string match objects

        Returns:
            bool: if has error return False
        """
        if mob is None:
            return False

        content = {'image/jpeg': 'jpg',
                  'image/png': 'png', 'image/gif': 'gif'}
        temp_file = '/home/user/discord-bot/open_url.temp'

        if not await util.download_file(mob.group(1), temp_file, content):
            return False

        image_type: str = imghdr.what(temp_file)
        if image_type is None:
            return False

        new_name: str = 'upload.{0}'.format(image_type)
        try:
            os.rename(temp_file, new_name)
            await ctx.send(file=discord.File(new_name))
            os.remove(new_name)
            return True
        except OSError as e:
            print(e)
            return False

    async def bot_command_weather(self, ctx, mob=None):
        url = "http://weather.livedoor.com/forecast/webservice/json/v1?city={0}".format(
            mob.group(1))
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        api_data = await resp.json()
                    else:
                        return False
        except aiohttp.InvalidURL as e:
            print(e)
            return False

        send_strings: str = '{0}\n'.format(api_data['title'])

        for weather in api_data['forecasts']:
            weather_date: str = weather['dateLabel']
            weather_fore_asts: str = weather['telop']
            s: str = '{0} : {1}\n'.format(weather_date, weather_fore_asts)
            send_strings += s

        send_strings += api_data['description']['text']
        await ctx.send(send_strings)
        return True
