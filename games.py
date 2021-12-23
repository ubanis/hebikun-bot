from typing import Dict, List
from discord.ext import commands

import random
import asyncio
import dice

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def d(self, ctx,message):
        result = dice.nDn(message)
        if result is not None:
            await ctx.send(result)
        return

    @commands.command()
    async def nkodice(self, ctx):
        nkodice: List[str] = ["う", "お", "こ", "ち", "ま", "ん"]
        current_dice = nkodice
        choice: str = ""
        result: str = ""
        out_message: str = ""
        add_roll: int = 0
        roll_count: int = 0
        dice_num: int = 5
        yaku: int = 0
        u_point: int = 0
        m_point: int = 0
        c_point: int =0
        u_double: float = 1
        m_double: float = 1
        c_double: float = 1
        total_u: float = 0
        total_m: float = 0
        total_c: float = 0
        unchi_flag_now = False
        unko_flag_now = False
        manko_flag_now = False
        omanko_flag_now = False
        chinko_flag_now = False
        chinchin_flag_now = False
        ochinchin_flag_now = False
        unko_combo: int = 0
        unchi_combo: int = 0
        manko_combo: int = 0
        omanko_combo: int = 0
        chinko_combo: int = 0
        chinchin_combo: int = 0
        ochinchin_combo: int = 0
        combo_bonus: int = 0
        dice_u = dice_o = dice_ko = dice_chi = dice_ma = dice_n = 0
        roll: int = 3
        round: int = 0
        ochinchin_str: str = " :regional_indicator_o: \
:regional_indicator_c: :regional_indicator_h: :regional_indicator_i: \
:regional_indicator_n:  :regional_indicator_c: :regional_indicator_h: \
:regional_indicator_i: :regional_indicator_n: "

        while roll_count < roll:
            round += 1
            result += str(round) + ": "
            for i in range(dice_num):
                choice = random.choice(current_dice)
                result += choice

            dice_u = result.count("う")
            dice_o = result.count("お")
            dice_ko = result.count("こ")
            dice_chi = result.count("ち")
            dice_ma = result.count("ま")
            dice_n = result.count("ん")

            u_point += 500 * dice_u
            m_point += 500 * dice_ma
            c_point += 500 * dice_chi
            u_point += 50 * dice_n
            m_point += 50 * dice_n
            c_point += 50 * dice_n
            u_point += 100 * dice_ko
            m_point += 100 * dice_ko
            c_point += 100 * dice_ko
            u_point += 300 * dice_o
            m_point += 300 * dice_o
            c_point += 300 * dice_o

            if dice_u >= 5:
                u_double = 4
            elif dice_u >= 4:
                u_double = 3
            elif dice_u >= 3:
                u_double = 2

            if dice_ma >= 5:
                m_double = 4
            elif dice_ma >= 4:
                m_double = 3
            elif dice_ma >= 3:
                m_double = 2

            if dice_chi >= 5:
                c_double = 4
            elif dice_chi >= 4:
                c_double = 3
            elif dice_chi >= 3:
                c_double = 2

            if dice_n >= 4:
                u_double = m_double = c_double = -4
            elif dice_n >= 3:
                u_double = m_double = c_double = -3

            if dice_ko >= 6:
                u_double = m_double = c_double = 4
            elif dice_ko >= 5:
                u_double = m_double = c_double = 3.5
            elif dice_ko >= 4:
                u_double = m_double = c_double = 2.5
            elif dice_ko >= 3:
                u_double = m_double = c_double = 1.5

            if dice_o >= 3:
                if total_u < 0:
                    total_u = -total_u
                if total_m < 0:
                    total_m = -total_m
                if total_c < 0:
                    total_c = -total_c

            if dice_o >= 6:
                u_double = 4
                m_double = 4
                c_double = 4
            elif dice_o >= 5:
                u_double = 3.5
                m_double = 3.5
                c_double = 3.5
            elif dice_o >= 4:
                u_double = 2.5
                m_double = 2.5
                c_double = 2.5
            elif dice_o >= 3:
                u_double = 1.5
                m_double = 1.5
                c_double = 1.5

            if all([dice_u >= 1, dice_n >= 1, dice_ko >= 1]):
                result += " **U N K O** "
                unko_flag_now = True
                unko_combo += 1
                if unko_combo == 2:
                    combo_bonus = 2000
                    result += "*(x2)* "
                elif unko_combo == 3:
                    combo_bonus = 4000
                    result += "*(x4)* "
                elif unko_combo >= 4:
                    combo_bonus = 8000
                    result += "*(x8)* "
                else:
                    combo_bonus = 1000
                u_point += combo_bonus
                add_roll = 1
                yaku += 1

            if all([dice_u >= 1, dice_n >= 1, dice_chi >= 1]):
                result += " **U N C H I** "
                unchi_flag_now = True
                unchi_combo += 1
                if unchi_combo == 2:
                    combo_bonus = 2000
                    result += "*(x2)* "
                elif unchi_combo == 3:
                    combo_bonus = 4000
                    result += "*(x4)* "
                elif unchi_combo >= 4:
                    combo_bonus = 8000
                    result += "*(x8)* "
                else:
                    combo_bonus = 1000
                u_point += combo_bonus
                add_roll = 1
                yaku += 1

            if all([dice_ma >= 1, dice_n >= 1, dice_ko >= 1]):
                result += " **M A N K O** "
                manko_flag_now = True
                manko_combo += 1
                if manko_combo == 2:
                    combo_bonus = 2000
                    result += "*(x2)* "
                elif manko_combo == 3:
                    combo_bonus = 4000
                    result += "*(x4)* "
                elif manko_combo >= 4:
                    combo_bonus = 8000
                    result += "*(x8)* "
                else:
                    combo_bonus = 1000
                m_point += combo_bonus
                add_roll = 1
                yaku += 1

            if all([dice_ma >= 1, dice_n >= 1, dice_ko >= 1, dice_o >= 1]):
                result += " **O M A N K O** "
                omanko_flag_now = True
                omanko_combo += 1
                if omanko_combo == 2:
                    combo_bonus = 10000
                    result += "*(x2)* "
                elif omanko_combo == 3:
                    combo_bonus = 20000
                    result += "*(x4)* "
                elif omanko_combo >= 4:
                    combo_bonus = 40000
                    result += "*(x8)* "
                else:
                    combo_bonus = 5000
                m_point += combo_bonus
                add_roll = 1
                yaku += 1

            if all([dice_chi >= 1, dice_n >= 1, dice_ko >= 1]):
                result += " **C H I N K O** "
                chinko_flag_now = True
                chinko_combo += 1
                if chinko_combo == 2:
                    combo_bonus = 2000
                    result += "*(x2)* "
                elif chinko_combo == 3:
                    combo_bonus = 4000
                    result += "*(x4)* "
                elif chinko_combo >= 4:
                    combo_bonus = 8000
                    result += "*(x8)* "
                else:
                    combo_bonus = 1000
                c_point += combo_bonus
                add_roll = 1
                yaku += 1

            if all([dice_chi >= 2, dice_n >= 2]):
                result += " **C H I N C H I N** "
                chinchin_flag_now = True
                chinchin_combo += 1
                if chinchin_combo == 2:
                    combo_bonus = 6000
                    result += "*(x2)* "
                elif chinchin_combo == 3:
                    combo_bonus = 12000
                    result += "*(x3)* "
                elif chinchin_combo >= 4:
                    combo_bonus = 24000
                    result += "*(x8)* "
                else:
                    combo_bonus = 3000
                c_point += combo_bonus
                add_roll = 1
                yaku += 1

            if all([dice_o >= 1, dice_chi >= 2, dice_n >= 2]):
                result += ochinchin_str
                ochinchin_flag_now = True
                ochinchin_combo += 1
                if ochinchin_combo == 2:
                    combo_bonus = 20000
                    result += "*(x2)* "
                elif ochinchin_combo == 3:
                    combo_bonus = 40000
                    result += "*(x4)* "
                elif ochinchin_combo >= 4:
                    combo_bonus = 80000
                    result += "*(x8)* "
                else:
                    combo_bonus = 10000
                c_point += combo_bonus
                add_roll = 1
                yaku = -1000
            dice_num = 5
            if yaku >= 2:
                dice_num += yaku - 1
            elif yaku == -1000:
                dice_num = 10

            if unchi_combo >= 1 and unchi_flag_now == False:
                unchi_combo = 0
            if unko_combo >= 1 and unko_flag_now == False:
                unko_combo = 0
            if manko_combo >= 1 and manko_flag_now == False:
                manko_combo = 0
            if omanko_combo >= 1 and omanko_flag_now == False:
                omanko_combo = 0
            if chinko_combo >= 1 and chinko_flag_now == False:
                chinko_combo = 0
            if chinchin_combo >= 1 and chinchin_flag_now == False:
                chinchin_combo = 0
            if ochinchin_combo >= 1 and ochinchin_flag_now == False:
                ochinchin_combo = 0

            unchi_flag_now = (
                unko_flag_now
            ) = (
                manko_flag_now
            ) = (
                omanko_flag_now
            ) = chinko_flag_now = chinchin_flag_now = ochinchin_flag_now = False
            total_u += u_point
            total_m += m_point
            total_c += c_point
            total_u *= u_double
            total_m *= m_double
            total_c *= c_double
            result += (
                " U: "
                + str(total_u)
                + " (x"
                + str(u_double)
                + ")"
                + " M: "
                + str(total_m)
                + " (x"
                + str(m_double)
                + ")"
                + " C: "
                + str(total_c)
                + " (x"
                + str(c_double)
                + ")\n"
            )
            out_message += result
            roll_count += 1
            roll_count -= add_roll
            u_double = m_double = c_double = 1
            u_point = m_point = c_point = 0
            yaku = 0
            add_roll = 0
            result = ""
        out_message += (
            "\nU: "
            + str(total_u)
            + " M: "
            + str(total_m)
            + " C: "
            + str(total_c)
            + "\n合計点数 **"
            + str(total_u + total_m + total_c)
            + " 点**\n"
        )

        await ctx.send(out_message)

    @commands.command()
    async def omikuji(self, ctx):
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
            "ん？": "でも細かいことを気にしすぎだよね、影響されやすいというか"
        }
        syamu_message: List[Dict[str, str]] = [lv1, lv2, lv3]
        unsei: List[str] = ['大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶', '順平']
        choice: str = random.choice(unsei)

        await ctx.send('本日' + ctx.author.name + 'の運勢は' + choice)
        if choice == '順平':
            await ctx.send('やーい！\nお前の運勢シャムゲーム！')
        else:
            return
        for i in syamu_message:

            def check_syamu(m):
                if m.author == self.bot.user:
                    return False
                elif m.content in i:
                    return True
                else:
                    return False

            try:
                msg = await self.bot.wait_for(
                    'message', check=check_syamu, timeout=10)
            except asyncio.TimeoutError:
                return
            await ctx.send(i[msg.content])
