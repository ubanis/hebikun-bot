import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
import re
import shutil
import imghdr
import util


class HebiListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        login_message: str = 'MESSAGE: bot login'
        game_str: str = 'おちんちん魔城伝説'

        print(login_message)
        print(self.bot.user.name)
        await self.bot.change_presence(activity=discord.Game(name=game_str))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error

    @commands.Cog.listener()
    async def on_message(self, message):
        local_dir: str = './upload/'
        test_local_dir: str = './temp/'
        temp_file: str = './~test.obj'
        playlist_dir: str = '/home/user/Musicbot/Playlists/'
        nsfw_channel_id: int = 317650564869521408
        test_channel_id: int = 317891419547369492
        bot_channel_id: int = 583000685688258594
        # general_channel_id = 317649332125827072

        if message.author.bot:
            return
        elif message.channel.id == nsfw_channel_id:
            await self.gallery_image_download(message, local_dir, temp_file,
                                              False)
        elif message.channel.id == bot_channel_id:
            await self.text_download(message, playlist_dir, True)
        elif message.channel.id == test_channel_id:
            await self.gallery_image_download(message, test_local_dir,
                                              temp_file, True)

    async def text_download(self, message, target_dir, istest=True):
        success_message: str = 'MESSAGE: text added to MusicBot Playlists -> '
        upload_message: str = "テキストファイルをMusicbotのPlaylistsフォルダに転送しました"
        content = {'text/plain': 'txt'}

        if message.attachments:
            for m in message.attachments:
                url = m.url
                filename = m.filename
                if not await util.download_file(url, filename, content):
                    continue
                try:
                    shutil.move(filename, target_dir)
                except shutil.Error as e:
                    print(e)
                    continue
                print(success_message, filename)
                emoji = discord.utils.get(self.bot.emojis, name='hebi')
                if emoji:
                    await message.add_reaction(emoji)
                    await message.channel.send(upload_message)

    async def gallery_image_download(self,
                                     message,
                                     target_dir,
                                     temp_file='~temp.tmp',
                                     istest=True):
        """Discord NSFW Gallery image upload

        Args:
            message (discord message): discord content message
            target_dir (str): save to gallery path
            temp_file (str): download temp filename or file path
            istest (bool): test mode enable or deisable
        """
        success_message: str = 'MESSAGE: image added to gallery -> '
        not_image_message: str = 'ERROR: File type is not image'
        header: str = 'discord-'
        content = {'image/jpeg': 'jpg',
                   'image/png': 'png', 'image/gif': 'gif'}
        regex = r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)"
        image_pattern = r".*\.(jpg|png|gif|jpeg)"
        url_pattern = re.compile(regex)
        match_obj = url_pattern.findall(message.content)

        if message.attachments:
            for m in message.attachments:
                url = m.url
                filename = m.filename
                if not await util.download_file(url, filename, content):
                    continue
                image_type = imghdr.what(filename)
                if image_type is None:
                    try:
                        os.remove(filename)
                    except OSError as e:
                        print(e)
                        continue
                image_type = 'jpg' if image_type == 'jpeg' else image_type
                number = len(util.get_files(target_dir, image_pattern))
                number_str = str(number + 1).zfill(6)
                new_name = '{0}{1}.{2}'.format(header, number_str, image_type)
                try:
                    os.rename(filename, new_name)
                except OSError as e:
                    print(e)
                    continue
                try:
                    shutil.move(new_name, target_dir)
                except shutil.Error as e:
                    print(e)
                    continue
                print(success_message, new_name)
                emoji = discord.utils.get(self.bot.emojis, name='hebi')
                if emoji:
                    await message.add_reaction(emoji)

        if match_obj:
            for i in range(len(match_obj)):
                url = match_obj[i][0] + match_obj[i][1]
                if not await util.download_file(url, temp_file, content):
                    continue
                image_type = imghdr.what(temp_file)
                if image_type is None:
                    try:
                        os.remove(temp_file)
                    except OSError as e:
                        print(e)
                        break
                    print(not_image_message)
                    continue
                image_type = 'jpg' if image_type == 'jpeg' else image_type
                number = len(util.get_files(target_dir, image_pattern))
                number_str = str(number + 1).zfill(6)
                new_name = header + number_str + '.' + image_type
                try:
                    os.rename(temp_file, new_name)
                except OSError as e:
                    print(e)
                    break
                try:
                    shutil.move(new_name, target_dir)
                except shutil.Error as e:
                    print(e)
                    break
                print(success_message, new_name)
                emoji = discord.utils.get(self.bot.emojis, name='hebi')
                if emoji:
                    await message.add_reaction(emoji)
