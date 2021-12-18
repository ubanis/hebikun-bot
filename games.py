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
        nkodice: List[str] = ['う', 'お', 'こ', 'ち', 'ま', 'ん']
        currentdice = nkodice
        choice:str =""
        result:str =""
        outmessage:str =""
        total:int = 0
        addroll:int = 0
        rollcount:int = 0
        dicenum:int=5
        yaku:int=0
        upoint:int=0
        mpoint:int=0
        cpoint:int=0
        udouble:int=1
        mdouble:int=1
        cdouble:int=1
        totalu:int=0
        totalm:int=0
        totalc:int=0
        unchi_flag_now = False
        unko_flag_now = False
        manko_flag_now = False
        omanko_flag_now = False
        chinko_flag_now = False
        chinchin_flag_now = False
        ochinchin_flag_now = False
        unko_combo = 0
        unchi_combo = 0
        manko_combo = 0
        omanko_combo = 0
        chinko_combo = 0
        chinchin_combo = 0
        ochinchin_combo = 0
        p:int=0
        u=o=ko=chi=ma=n=0
        roll:int=3
        round:int=0

        while rollcount < roll:
            round += 1
            result += str(round) + ": "
            for i in range(dicenum):
                choice = random.choice(currentdice)
                result += choice

            u=result.count('う')
            o=result.count('お')
            ko=result.count('こ')
            chi=result.count('ち')
            ma=result.count('ま')
            n=result.count('ん')

            for i in range(u):
                upoint += 500
            for i in range(ma):
                mpoint += 500
            for i in range(chi):
                cpoint += 500
            for i in range(n):
                upoint += 50
                mpoint += 50
                cpoint += 50
            for i in range(ko):
                upoint += 100
                mpoint += 100
                cpoint += 100
            for i in range(o):
                upoint += 300
                mpoint += 300
                cpoint += 300

            if(u>=5):
                udouble = 4
            elif(u>=4):
                udouble = 3
            elif(u>=3):
                udouble = 2

            if(ma>=5):
                mdouble = 4
            elif(ma>=4):
                mdouble = 3
            elif(ma>=3):
                mdouble = 2

            if(chi>=5):
                cdouble = 4
            elif(chi>=4):
                cdouble = 3
            elif(chi>=3):
                cdouble = 2

            if(n>=4):
                udouble = -4
                mdouble = -4
                cdouble = -4
            elif(n>=3):
                udouble = -3
                mdouble = -3
                cdouble = -3

            if(ko>=6):
                udouble = 4
                mdouble = 4
                cdouble = 4
            elif(ko>=5):
                udouble = 3.5
                mdouble = 3.5
                cdouble = 3.5
            elif(ko>=4):
                udouble = 2.5
                mdouble = 2.5
                cdouble = 2.5
            elif(ko>=3):
                udouble = 1.5
                mdouble = 1.5
                cdouble = 1.5

            if(o>=3):
                if(totalu<0):
                    totalu = -totalu
                if(totalm<0):
                    totalm = -totalm
                if(totalc<0):
                    totalc = -totalc

            if(o>=6):
                udouble = 4
                mdouble = 4
                cdouble = 4
            elif(o>=5):
                udouble = 3.5
                mdouble = 3.5
                cdouble = 3.5
            elif(o>=4):
                udouble = 2.5
                mdouble = 2.5
                cdouble = 2.5
            elif(o>=3):
                udouble = 1.5
                mdouble = 1.5
                cdouble = 1.5

            if all([u>=1,n>=1,ko>=1]):
                result += " **U N K O** "
                unko_flag_now = True
                unko_combo += 1
                if(unko_combo == 2):
                    p = 2000
                    result += "*(x2)* "
                elif(unko_combo == 3):
                    p = 4000
                    result += "*(x4)* "
                elif(unko_combo >= 4):
                    p = 8000
                    result += "*(x8)* "
                else:
                    p = 1000
                upoint += p
                addroll = 1
                yaku+=1

            if all([u>=1,n>=1,chi>=1]):
                result += " **U N C H I** "
                unchi_flag_now = True
                unchi_combo += 1
                if(unchi_combo == 2):
                    p = 2000
                    result += "*(x2)* "
                elif(unchi_combo == 3):
                    p = 4000
                    result += "*(x4)* "
                elif(unchi_combo >= 4):
                    p = 8000
                    result += "*(x8)* "
                else:
                    p = 1000
                upoint += p
                addroll = 1
                yaku+=1

            if all([ma>=1,n>=1,ko>=1]):
                result += " **M A N K O** "
                manko_flag_now = True
                manko_combo += 1
                if(manko_combo == 2):
                    p = 2000
                    result += "*(x2)* "
                elif(manko_combo == 3):
                    p = 4000
                    result += "*(x4)* "
                elif(manko_combo >= 4):
                    p = 8000
                    result += "*(x8)* "
                else:
                    p = 1000
                mpoint += p
                addroll = 1
                yaku+=1

            if all([ma>=1 , n>=1 , ko>=1 , o>=1]):
                result += " **O M A N K O** "
                omanko_flag_now = True
                omanko_combo += 1
                if(omanko_combo == 2):
                    p = 10000
                    result += "*(x2)* "
                elif(omanko_combo == 3):
                    p = 20000
                    result += "*(x4)* "
                elif(omanko_combo >= 4):
                    p = 40000
                    result += "*(x8)* "
                else:
                    p = 5000
                mpoint += p
                addroll = 1
                yaku+=1

            if all([chi>=1 , n>=1 , ko>=1]):
                result += " **C H I N K O** "
                chinko_flag_now = True
                chinko_combo += 1
                if(chinko_combo == 2):
                    p = 2000
                    result += "*(x2)* "
                elif(chinko_combo == 3):
                    p = 4000
                    result += "*(x4)* "
                elif(chinko_combo >= 4):
                    p = 8000
                    result += "*(x8)* "
                else:
                    p = 1000
                cpoint += p
                addroll = 1
                yaku+=1

            if all([chi>=2 , n>=2]):
                result += " **C H I N C H I N** "
                chinchin_flag_now = True
                chinchin_combo += 1
                if(chinchin_combo == 2):
                    p = 6000
                    result += "*(x2)* "
                elif(chinchin_combo == 3):
                    p = 12000
                    result += "*(x3)* "
                elif(chinchin_combo >= 4):
                    p = 24000
                    result += "*(x8)* "
                else:
                    p = 3000
                cpoint += p
                addroll = 1
                yaku+=1

            if all([o>=1 , chi>=2 , n>=2]):
                result += " :regional_indicator_o: :regional_indicator_c: :regional_indicator_h: :regional_indicator_i: :regional_indicator_n:  :regional_indicator_c: :regional_indicator_h: :regional_indicator_i: :regional_indicator_n: "
                ochinchin_flag_now = True
                ochinchin_combo += 1
                if(ochinchin_combo == 2):
                    p = 20000
                    result += "*(x2)* "
                elif(ochinchin_combo == 3):
                    p = 40000
                    result += "*(x4)* "
                elif(ochinchin_combo >= 4):
                    p = 80000
                    result += "*(x8)* "
                else:
                    p = 10000
                cpoint += p
                addroll = 1
                yaku=-1000
            dicenum = 5
            if(yaku >= 2):
                dicenum += yaku-1
            elif(yaku == -1000):
                dicenum = 10

            if(unchi_combo >= 1 and unchi_flag_now == False):
                unchi_combo = 0
            if(unko_combo >= 1 and unko_flag_now == False):
                unko_combo = 0
            if(manko_combo >= 1 and manko_flag_now == False):
                manko_combo = 0
            if(omanko_combo >= 1 and omanko_flag_now == False):
                omanko_combo = 0
            if(chinko_combo >= 1 and chinko_flag_now == False):
                chinko_combo = 0
            if(chinchin_combo >= 1 and chinchin_flag_now == False):
                chinchin_combo = 0
            if(ochinchin_combo >= 1 and ochinchin_flag_now == False):
                ochinchin_combo = 0

            unchi_flag_now = unko_flag_now = manko_flag_now = omanko_flag_now = chinko_flag_now = chinchin_flag_now = ochinchin_flag_now = False
            totalu += upoint
            totalm += mpoint
            totalc += cpoint
            totalu *= udouble
            totalm *= mdouble
            totalc *= cdouble
            result += " U: " + str(totalu) + " (x" + str(udouble) + ")" + " M: " + str(totalm) + " (x" + str(mdouble) + ")"  +  " C: " + str(totalc) + " (x" + str(cdouble) + ")\n"
            outmessage += result
            rollcount += 1
            rollcount -= addroll
            udouble = mdouble = cdouble = 1
            upoint = mpoint = cpoint = 0
            yaku=0
            addroll = 0
            result=""
        outmessage += "\nU: " + str(totalu) + " M: " + str(totalm) + " C: " + str(totalc) + "\n合計点数 **" + str(totalu+totalm+totalc) + " 点**\n"

        await ctx.send(outmessage)

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
