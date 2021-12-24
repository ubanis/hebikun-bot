import asyncio
import imghdr
import os
import pathlib
import re
from typing import List, Union

import aiohttp
import discord
import pandas as pd
from discord.ext import commands

import util

class HebiCommand:
    """
    Hebi command class
    """
    def __init__(self, name:str, pattern:str, function, desc:str):
        self.__name: str = name
        self.__pattern: str = pattern
        self.__function = function
        self.__description: str = desc

    @property
    def name(self) -> str:
        """str: command name"""
        return self.__name
    @property
    def pattern(self) -> str:
        """str: command matching pattern"""
        return self.__pattern
    @property
    def function(self):
        """any: command method pointer"""
        return self.__function
    @property
    def description(self) -> str:
        """str: command description"""
        return self.__description

class Hebi(commands.Cog):
    """
    Hebi command class
    """
    def __init__(self, bot):
        self._ask: str = 'ask'
        self._answer: str = 'answer'
        self._command: str = 'command'
        self._csv_file: str = "../data/hebi.csv"
        self.bot = bot
        self._df: pd.DataFrame = None

        self.command_list = []
        self.load_csv()
        self.set_hebi_commands()

        self._timeout_message: str = self._df.at['@timeout_message', self._answer]
        self._what_message: str = self._df.at['@what_message', self._answer]
        self._learn_message: str = self._df.at['@learn_message', self._answer]
        self._bot_setmes_help_message: str = self._df.at['@setmes_help_message',
                                                    self._answer]
        self._chmes_success_message: str = self._df.at['@chmes_success_message',
                                                  self._answer]
        self._chmes_fail_message: str = self._df.at['@chmes_fail_message', self.
                                               _answer]
        self._unknown_message: str = self._df.at['@unknown_command_message', self.
                                            _answer]

    def load_csv(self) -> bool:
        """load csv file to pandas DataFrame

        Returns:
            bool: if load error has return False
        """
        try:
            self._df = pd.read_csv(self._csv_file, index_col=0)
        except pd.io.common.EmptyDataError as error:
            print(error)
            return False
        self._df.sort_values(self._ask, inplace=True)
        print(self._df.info())
        return True

    def set_hebi_commands(self):
        """set self.hebi_commands dict
        """
        self.command_list = [
                HebiCommand("base_command",r'(.*)\(.*\)',None,"このコマンドは利用できません"),
                HebiCommand("send_file",
                            r'send_file\(\"(.*)\"\)',
                            self.bot_command_send_file,
                            "[send_file ファイルパス] ローカル用コマンドなので \
                            !setmes ではファイルを指定できませんdesc-grandy"),
                HebiCommand("open_url_image",
                            r'open_url_image\(\"(.*)\"\)',
                            self.bot_command_open_url_image,
                            "[open_url_image 画像のURL] 指定されたURLの画像を\
                            メッセージの後貼り付けます"),
                HebiCommand("send_url",
                            r'send_url\(\"(.*)\"\)',
                            self.bot_command_send_url,
                            "[send_url 指定URL] 指定されたURLを\
                            メッセージの後貼り付けます"),
                HebiCommand("weather",
                            r'weather\(\"(.*)\"\)',
                            self.bot_command_weather,
                            "[weather 都市コード] 指定コードの天気を貼り付けます\
                            　コードはこちらで確認してください。\
                            http://weather.livedoor.com/forecast/rss/primary_area.xmldesc-kyle")
            ]

    def get_command(self, command_str: str) -> Union[None, HebiCommand]:
        """get a command dict from self.hebi_commands

        Args:
            command_str (str): command string

        Returns:
            HebiCommand or None 
        """
        match_str = re.search( self.command_list[0].pattern,command_str)
        if match_str is None:
            return None
        command_name = match_str.group(1)
        for cm_list in self.command_list:
            if cm_list.name == command_name:
                return cm_list
        return None

    @commands.command()
    async def help(self, ctx):
        """send help message to user dm

        Args:
            ctx (discord context): context
        """
        dm_user = self.bot.get_user(ctx.message.author.id)
        dm_context = await dm_user.create_dm()
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
        await dm_context.send(content=None, embed=embed)

    @commands.command()
    async def listcommand(self, ctx):
        """list a command to user dm

        Args:
            ctx (discord context): context
        """
        dm_user = self.bot.get_user(ctx.message.author.id)
        dm_context = await dm_user.create_dm()
        embed = discord.Embed(title='メッセージで使えるコマンド一覧', color=0x26de12)

        for cm_list in self.command_list:
            embed.add_field(
                name = cm_list.name,
                value = cm_list.description,
                inline = False)
        await dm_context.send(content=None, embed=embed)

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
            command_strings = f"{messages[2]}(\"{messages[3]}\")"
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
    async def p(self, ctx) -> bool:
        """
        List of drawpile login users
        Args:
            self (Hebi): self
            ctx (Discord): Discord context
        Returns:
            command success
        """
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
        except aiohttp.InvalidURL as error:
            print(error)
            return False

        for data in api_data1:
            title = data['title']
            url = f"http://localhost:27780/api/sessions/{data['id']}/"
            session_data.append([title, url])

        for data in session_data:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(data[1]) as resp:
                        if resp.status == 200:
                            api_data2 = await resp.json()
                        else:
                            await ctx.send(message)
                            return False
            except aiohttp.InvalidURL as error:
                print(error)
                return False

            output += f"__{data[0]}__\n"
            for room_data in api_data2['listings']:
                output += f"[roomcode: {room_data['roomcode']}]\n"
            for room_data in api_data2['users']:
                if room_data['online']:
                    output += f"{room_data['name']}\n"
            output += "\n"

        await ctx.send(output)
        return True

    @commands.command()
    async def hebi(self, ctx) -> bool:
        """bot wait for message until 20 seconds

        Args:
            ctx (discord context): context

        Returns:
            bool: command success result
        """
        await ctx.send(self._what_message)

        def check_hebi(ch_mes):
            if ch_mes.author == self.bot.user or ctx.message.author != ch_mes.author:
                return False
            elif ch_mes.content in self._df.index:
                return True
            else:
                return False

        try:
            wait_msg = await self.bot.wait_for(
                'message', check=check_hebi, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send(self._timeout_message)
            return False

        await ctx.send(self._df.at[wait_msg.content, self._answer])

        command_str = self._df.at[wait_msg.content, self._command]
        if command_str != "none":
            await self.hebi_commands_run(ctx, command_str)
        return True

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

    async def hebi_commands_run(self, ctx, command_str) -> bool:
        """hebi bot command execute

        Args:
            ctx (channel context): discord channel context
            command_str (str): command strings

        Returns:
            bool: command execute success?
        """
        command_error_message: str = 'HEBI_ERROR: hebi command error'

        command2: Union[HebiCommand, None] = self.get_command(command_str)

        if command2 is None:
            print(command_error_message)
            return False

        mob2 = re.search(command2.pattern, command_str)

        if mob2 is None:
            print(command_error_message)
            return False

        try:
            is_success = await command2.function(ctx, mob2)
        except:
            print(command_error_message)
            return False

        if is_success:
            print(command_str)
        else:
            print(command_error_message)
            return False
        return False

    async def bot_command_send_file(self, ctx, mob=None) -> bool:
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

    async def bot_command_send_url(self, ctx, mob=None) -> bool:
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

    async def bot_command_open_url_image(self, ctx, mob=None) -> bool:
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
        temp_file = './open_url.temp'

        if not await util.download_file(mob.group(1), temp_file, content):
            return False

        image_type: Union[str, None] = imghdr.what(temp_file)
        if image_type is None:
            return False

        new_name: str = f"upload.{image_type}"
        try:
            os.rename(temp_file, new_name)
            await ctx.send(file=discord.File(new_name))
            os.remove(new_name)
            return True
        except OSError as error:
            print(error)
            return False

    async def bot_command_weather(self, ctx, mob=None) -> bool:
        url = f"http://weather.livedoor.com/forecast/webservice/json/v1?city={mob.group(1)}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        api_data = await resp.json()
                    else:
                        return False
        except aiohttp.InvalidURL as error:
            print(error)
            return False

        send_strings: str = f"{api_data['title']}\n')"

        for weather in api_data['forecasts']:
            weather_date: str = weather['dateLabel']
            weather_fore_asts: str = weather['telop']
            s: str = f"{weather_date} : {weather_fore_asts}\n"
            send_strings += s

        send_strings += api_data['description']['text']
        await ctx.send(send_strings)
        return True
