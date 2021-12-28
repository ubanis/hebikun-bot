""" Hebi bot games module """
import asyncio
import random
from typing import Dict, List, Union

from discord.ext import commands
from discord.commands import Option, slash_command

import dice
import nkodice

GUILD_ID = 317649332125827072
class Games(commands.Cog):
    """
    Hebi games commands class
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def d(self, ctx, message):
        """
        Roll a dice(nDn)
        Args:
            self (Games): class self
            ctx (Discord): discord context
            message:
                message from command user
        """
        result = dice.nDn(message)
        if result is not None:
            await ctx.send(result)
        return

    @slash_command(name='d', description='ダイスを nDn 形式で振ります 例) 3d6 -> 3個の6面ダイスを振る', guild_ids=[GUILD_ID])
    async def slash_d(self, ctx, message):
        """
        Roll a dice(nDn) with slash command
        Args:
            self (Games): class self
            ctx (Discord): discord context
            message:
                message from command user
        """
        result = dice.nDn(message)
        if result is not None:
            await ctx.respond(result)
        else:
            await ctx.respond("なにやらダイスの指定がおかしいようです")
        return

    @slash_command(name='nkodice', description='Nkodiceをします', guild_ids=[GUILD_ID])
    async def slash_nkodice(self, ctx):
        """
        Roll a Nkodice with slash command
        """
        await ctx.respond(nkodice.nkodice_main())

    @commands.command()
    async def nkodice(self, ctx):
        """
        Roll a Nkodice
        Args:
            self (Games): class self
            ctx (Discord): discord context
        """
        await ctx.respond(nkodice.nkodice_main())

    @slash_command(name='omikuji', description='おみくじをします', guild_ids=[GUILD_ID])
    async def slash_omikuji(self, ctx) -> Union[bool,None]:
        """
        omikuji command with slash command
        Args:
            ctx (discord context): context
        Returns:
            bool: command result
        """

        lv1 = {"言い過ぎ": "ごめんなさい", "いいすぎ": "ごめんなさい"}
        lv2 = {"偉い": "謝りました・・・（達成感）", "えらい": "謝りました・・・（達成感）"}
        lv3 = {
            "？": "でも細かいことを気にしすぎだよね、影響されやすいというか",
            "ん？": "でも細かいことを気にしすぎだよね、影響されやすいというか",
        }
        syamu_message: List[Dict[str, str]] = [lv1, lv2, lv3]
        unsei: List[str] = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶", "順平"]
        choice: str = random.choice(unsei)

        await ctx.respond("本日" + ctx.author.name + "の運勢は" + choice)
        if choice == "順平":
            await ctx.respond("やーい！\nお前の運勢シャムゲーム！")
        else:
            return
        for i in syamu_message:

            def check_syamu(mes_ctx):
                if mes_ctx.author == self.bot.user:
                    return False
                elif mes_ctx.content in i:
                    return True
                else:
                    return False

            try:
                msg = await self.bot.wait_for("message", check=check_syamu, timeout=10)
            except asyncio.TimeoutError:
                return
            await ctx.respond(i[msg.content])

    @commands.command()
    async def omikuji(self, ctx) -> Union[bool,None]:
        """omikuji command
        Args:
            ctx (discord context): context
        Returns:
            bool: command result
        """

        lv1 = {"言い過ぎ": "ごめんなさい", "いいすぎ": "ごめんなさい"}
        lv2 = {"偉い": "謝りました・・・（達成感）", "えらい": "謝りました・・・（達成感）"}
        lv3 = {
            "？": "でも細かいことを気にしすぎだよね、影響されやすいというか",
            "ん？": "でも細かいことを気にしすぎだよね、影響されやすいというか",
        }
        syamu_message: List[Dict[str, str]] = [lv1, lv2, lv3]
        unsei: List[str] = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶", "順平"]
        choice: str = random.choice(unsei)

        await ctx.send("本日" + ctx.author.name + "の運勢は" + choice)
        if choice == "順平":
            await ctx.send("やーい！\nお前の運勢シャムゲーム！")
        else:
            return
        for i in syamu_message:

            def check_syamu(mes_ctx):
                if mes_ctx.author == self.bot.user:
                    return False
                elif mes_ctx.content in i:
                    return True
                else:
                    return False

            try:
                msg = await self.bot.wait_for("message", check=check_syamu, timeout=10)
            except asyncio.TimeoutError:
                return
            await ctx.send(i[msg.content])
