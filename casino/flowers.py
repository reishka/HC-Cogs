import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from collections import namedtuple, defaultdict, deque
from datetime import datetime
from copy import deepcopy
from .utils import checks
from cogs.utils.chat_formatting import pagify, box
from enum import Enum
from __main__ import send_cmd_help
import os
import time
import logging
import random

default_settings = {"PAYDAY_TIME": 300, "PAYDAY_CREDITS": 150,
                    "REGISTER_CREDITS": 100}


class GamblingError(Exception):
    pass


class OnCooldown(GamblingError):
    pass


class InvalidBid(GamblingError):
    pass


class CasinoError(Exception):
    pass


class AccountAlreadyExists(CasinoError):
    pass


class NoAccount(CasinoError):
    pass


class InsufficientBalance(CasinoError):
    pass


class NegativeValue(CasinoError):
    pass


class SameSenderAndReceiver(CasinoError):
    pass


NUM_ENC = "\N{COMBINING ENCLOSING KEYCAP}"


class Casino:

    def __init__(self, bot, file_path):
        self.ledgers = dataIO.load_json(file_path)
        self.bot = bot

    def create_ledger(self, user, *, initial_balance=0):
        server = user.server
        if not self.ledger_exists(user):
            if server.id not in self.ledgers:
                self.ledgers[server.id] = {}
            else:
                balance = initial_balance
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            ledger = {"name": user.name,
                       "balance": balance,
                       "created_at": timestamp
                       }
            self.ledgers[server.id][user.id] = ledger
            self._save_casino()
            return self.get_ledger(user)
        else:
            raise AccountAlreadyExists()

    def ledger_exists(self, user):
        try:
            self._get_ledger(user)
        except NoAccount:
            return False
        return True

    def withdraw_flowers(self, user, amount):
        server = user.server

        if amount < 0:
            raise NegativeValue()

        ledger = self._get_ledger(user)
        if ledger["balance"] >= amount:
            ledger["balance"] -= amount
            self.ledgers[server.id][user.id] = ledger
            self._save_casino()
        else:
            raise InsufficientBalance()

    def deposit_flowers(self, user, amount):
        server = user.server
        if amount < 0:
            raise NegativeValue()
        ledger = self._get_ledger(user)
        ledger["balance"] += amount
        self.ledgers[server.id][user.id] = ledger
        self._save_casino()

    def set_flowers(self, user, amount):
        server = user.server
        if amount < 0:
            raise NegativeValue()
        ledger = self._get_ledger(user)
        ledger["balance"] = amount
        self.ledgers[server.id][user.id] = ledger
        self._save_casino()

    def transfer_flowers(self, sender, receiver, amount):
        if amount < 0:
            raise NegativeValue()
        if sender is receiver:
            raise SameSenderAndReceiver()
        if self.ledger_exists(sender) and self.ledger_exists(receiver):
            sender_acc = self._get_ledger(sender)
            if sender_acc["balance"] < amount:
                raise InsufficientBalance()
            self.withdraw_flowers(sender, amount)
            self.deposit_flowers(receiver, amount)
        else:
            raise NoAccount()

    def can_spend(self, user, amount):
        ledger = self._get_ledger(user)
        if ledger["balance"] >= amount:
            return True
        else:
            return False

    def wipe_casino(self, server):
        self.ledgers[server.id] = {}
        self._save_casino()

    def get_server_ledgers(self, server):
        if server.id in self.ledgers:
            raw_server_ledgers = deepcopy(self.ledgers[server.id])
            ledgers = []
            for k, v in raw_server_ledgers.items():
                v["id"] = k
                v["server"] = server
                acc = self._create_ledger_obj(v)
                ledgers.append(acc)
            return ledgers
        else:
            return []

    def get_all_ledgers(self):
        ledgers = []
        for server_id, v in self.ledgers.items():
            server = self.bot.get_server(server_id)
            if server is None:
                # Servers that have since been left will be ignored
                # Same for users_id from the old casino format
                continue
            raw_server_ledgers = deepcopy(self.ledgers[server.id])
            for k, v in raw_server_ledgers.items():
                v["id"] = k
                v["server"] = server
                acc = self._create_ledger_obj(v)
                ledgers.append(acc)
        return ledgers

    def get_balance(self, user):
        ledger = self._get_ledger(user)
        return ledger["balance"]

    def get_ledger(self, user):
        acc = self._get_ledger(user)
        acc["id"] = user.id
        acc["server"] = user.server
        return self._create_ledger_obj(acc)

    def _create_ledger_obj(self, ledger):
        ledger["member"] = ledger["server"].get_member(ledger["id"])
        ledger["created_at"] = datetime.strptime(ledger["created_at"],
                                                  "%Y-%m-%d %H:%M:%S")
        Account = namedtuple("Account", "id name balance "
                             "created_at server member")
        return Account(**ledger)

    def _save_casino(self):
        dataIO.save_json("data/gambling/casino.json", self.ledgers)

    def _get_ledger(self, user):
        server = user.server
        try:
            return deepcopy(self.ledgers[server.id][user.id])
        except KeyError:
            raise NoAccount()


class SetParser:
    def __init__(self, argument):
        allowed = ("+", "-")
        if argument and argument[0] in allowed:
            try:
                self.sum = int(argument)
            except:
                raise
            if self.sum < 0:
                self.operation = "withdraw"
            elif self.sum > 0:
                self.operation = "deposit"
            else:
                raise
            self.sum = abs(self.sum)
        elif argument.isdigit():
            self.sum = int(argument)
            self.operation = "set"
        else:
            raise


class Gambling:
    """Casino
    Get rich and have fun with flowers!"""

    def __init__(self, bot):
        global default_settings
        self.bot = bot
        self.casino = Casino(bot, "data/gambling/casino.json")
        self.file_path = "data/gambling/settings.json"
        self.settings = dataIO.load_json(self.file_path)
        self.settings = defaultdict(lambda: default_settings, self.settings)
        self.payday_register = defaultdict(dict)
        self.slot_register = defaultdict(dict)

    @commands.group(name="casino", pass_context=True)
    async def _casino(self, ctx):
        """Casino operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_casino.command(pass_context=True, no_pm=True)
    async def register(self, ctx):
        """Registers an ledger at the Hammer Council casino"""
        settings = self.settings[ctx.message.server.id]
        author = ctx.message.author
        flowers = 0
        if ctx.message.server.id in self.settings:
            flowers = settings.get("REGISTER_CREDITS", 0)
        try:
            ledger = self.casino.create_ledger(author, initial_balance=flowers)
            await self.bot.say("{} Account opened. Current balance: {}"
                               "".format(author.mention, ledger.balance))
        except AccountAlreadyExists:
            await self.bot.say("{} You already have an ledger at the"
                               " Hammer Council casino.".format(author.mention))

    @_casino.command(pass_context=True)
    async def balance(self, ctx, user: discord.Member=None):
        """Shows balance of user.
        Defaults to yours."""
        if not user:
            user = ctx.message.author
            try:
                await self.bot.say("{} Your balance is: {}".format(
                    user.mention, self.casino.get_balance(user)))
            except NoAccount:
                await self.bot.say("{} You don't have an ledger at the"
                                   " Hammer Council casino. Type `{}casino register`"
                                   " to open one.".format(user.mention,
                                                          ctx.prefix))
        else:
            try:
                await self.bot.say("{}'s balance is {}".format(
                    user.name, self.casino.get_balance(user)))
            except NoAccount:
                await self.bot.say("That user has no casino ledger.")

    @_casino.command(pass_context=True)
    async def transfer(self, ctx, user: discord.Member, sum: int):
        """Transfer flowers to other users"""
        author = ctx.message.author
        try:
            self.casino.transfer_flowers(author, user, sum)
            logger.info("{}({}) transferred {} :cherry_blossom: to {}({})".format(
                author.name, author.id, sum, user.name, user.id))
            await self.bot.say("{} :cherry_blossom: have been transferred to {}'s"
                               " ledger.".format(sum, user.name))
        except NegativeValue:
            await self.bot.say("You need to transfer at least 1 credit.")
        except SameSenderAndReceiver:
            await self.bot.say("You can't transfer :cherry_blossom: to yourself.")
        except InsufficientBalance:
            await self.bot.say("You don't have that sum in your casino ledger.")
        except NoAccount:
            await self.bot.say("That user has no casino ledger.")

    @_casino.command(name="set", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _set(self, ctx, user: discord.Member, flowers: SetParser):
        """Sets flowers of user's casino ledger. See help for more operations
        Passing positive and negative values will add/remove flowers instead
        Examples:
            casino set @HammerCouncil 26 - Sets 26 flowers
            casino set @HammerCouncil +2 - Adds 2 flowers
            casino set @HammerCouncil -6 - Removes 6 flowers"""
        author = ctx.message.author
        try:
            if flowers.operation == "deposit":
                self.casino.deposit_flowers(user, flowers.sum)
                logger.info("{}({}) added {} :cherry_blossom: to {} ({})".format(
                    author.name, author.id, flowers.sum, user.name, user.id))
                await self.bot.say("{} :cherry_blossom: have been added to {}"
                                   "".format(flowers.sum, user.name))
            elif flowers.operation == "withdraw":
                self.casino.withdraw_flowers(user, flowers.sum)
                logger.info("{}({}) removed {} :cherry_blossom: to {} ({})".format(
                    author.name, author.id, flowers.sum, user.name, user.id))
                await self.bot.say("{} :cherry_blossom: have been withdrawn from {}"
                                   "".format(flowers.sum, user.name))
            elif flowers.operation == "set":
                self.casino.set_flowers(user, flowers.sum)
                logger.info("{}({}) set {} :cherry_blossom: to {} ({})"
                            "".format(author.name, author.id, flowers.sum,
                                      user.name, user.id))
                await self.bot.say("{}'s :cherry_blossom: have been set to {}".format(
                    user.name, flowers.sum))
        except InsufficientBalance:
            await self.bot.say("User doesn't have enough :cherry_blossom:.")
        except NoAccount:
            await self.bot.say("User has no casino ledger.")

    @_casino.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def reset(self, ctx, confirmation: bool=False):
        """Deletes all server's casino ledgers"""
        if confirmation is False:
            await self.bot.say("This will delete all casino ledgers on "
                               "this server.\nIf you're sure, type "
                               "{}casino reset yes".format(ctx.prefix))
        else:
            self.casino.wipe_casino(ctx.message.server)
            await self.bot.say("All casino ledgers of this server have been "
                               "deleted.")

    @commands.command(pass_context=True, no_pm=True)
    async def payday(self, ctx):  # TODO
        """Get some free flowers"""
        author = ctx.message.author
        server = author.server
        id = author.id
        if self.casino.ledger_exists(author):
            if id in self.payday_register[server.id]:
                seconds = abs(self.payday_register[server.id][
                              id] - int(time.perf_counter()))
                if seconds >= self.settings[server.id]["PAYDAY_TIME"]:
                    self.casino.deposit_flowers(author, self.settings[
                                              server.id]["PAYDAY_CREDITS"])
                    self.payday_register[server.id][
                        id] = int(time.perf_counter())
                    await self.bot.say(
                        "{} Here, take some :cherry_blossom:. Enjoy! (+{}"
                        " :cherry_blossom:!)".format(
                            author.mention,
                            str(self.settings[server.id]["PAYDAY_CREDITS"])))
                else:
                    dtime = self.display_time(
                        self.settings[server.id]["PAYDAY_TIME"] - seconds)
                    await self.bot.say(
                        "{} Too soon. For your next payday you have to"
                        " wait {}.".format(author.mention, dtime))
            else:
                self.payday_register[server.id][id] = int(time.perf_counter())
                self.casino.deposit_flowers(author, self.settings[
                                          server.id]["PAYDAY_CREDITS"])
                await self.bot.say(
                    "{} Here, take some :cherry_blossom:. Enjoy! (+{} :cherry_blossom:!)".format(
                        author.mention,
                        str(self.settings[server.id]["PAYDAY_CREDITS"])))
        else:
            await self.bot.say("{} You need an ledger to receive :cherry_blossom:."
                               " Type `{}casino register` to open one.".format(
                                   author.mention, ctx.prefix))

    @commands.group(pass_context=True)
    async def leaderboard(self, ctx):
        """Server / global leaderboard
        Defaults to server"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self._server_leaderboard)

    @leaderboard.command(name="server", pass_context=True)
    async def _server_leaderboard(self, ctx, top: int=10):
        """Prints out the server's leaderboard
        Defaults to top 10"""
        # Originally coded by Airenkun - edited by irdumb
        server = ctx.message.server
        if top < 1:
            top = 10
        casino_sorted = sorted(self.casino.get_server_ledgers(server),
                             key=lambda x: x.balance, reverse=True)
        if len(casino_sorted) < top:
            top = len(casino_sorted)
        topten = casino_sorted[:top]
        highscore = ""
        place = 1
        for acc in topten:
            highscore += str(place).ljust(len(str(top)) + 1)
            highscore += (acc.name + " ").ljust(23 - len(str(acc.balance)))
            highscore += str(acc.balance) + "\n"
            place += 1
        if highscore != "":
            for page in pagify(highscore, shorten_by=12):
                await self.bot.say(box(page, lang="py"))
        else:
            await self.bot.say("There are no ledgers in the casino.")

    @leaderboard.command(name="global")
    async def _global_leaderboard(self, top: int=10):
        """Prints out the global leaderboard
        Defaults to top 10"""
        if top < 1:
            top = 10
        casino_sorted = sorted(self.casino.get_all_ledgers(),
                             key=lambda x: x.balance, reverse=True)
        unique_ledgers = []
        for acc in casino_sorted:
            if not self.already_in_list(unique_ledgers, acc):
                unique_ledgers.append(acc)
        if len(unique_ledgers) < top:
            top = len(unique_ledgers)
        topten = unique_ledgers[:top]
        highscore = ""
        place = 1
        for acc in topten:
            highscore += str(place).ljust(len(str(top)) + 1)
            highscore += ("{} |{}| ".format(acc.name, acc.server.name)
                          ).ljust(23 - len(str(acc.balance)))
            highscore += str(acc.balance) + "\n"
            place += 1
        if highscore != "":
            for page in pagify(highscore, shorten_by=12):
                await self.bot.say(box(page, lang="py"))
        else:
            await self.bot.say("There are no ledgers in the casino.")

    def already_in_list(self, ledgers, user):
        for acc in ledgers:
            if user.id == acc.id:
                return True
        return False

    @commands.command()
    async def payouts(self):
        """Shows slot machine payouts"""
        await self.bot.whisper(SLOT_PAYOUTS_MSG)

    @commands.command(pass_context=True, no_pm=True)
    async def slot(self, ctx, bid: int):
        """Play the slot machine"""
        author = ctx.message.author
        server = author.server
        settings = self.settings[server.id]
        valid_bid = settings["SLOT_MIN"] <= bid and bid <= settings["SLOT_MAX"]
        slot_time = settings["SLOT_TIME"]
        last_slot = self.slot_register.get(author.id)
        now = datetime.utcnow()
        try:
            if last_slot:
                if (now - last_slot).seconds < slot_time:
                    raise OnCooldown()
            if not valid_bid:
                raise InvalidBid()
            if not self.casino.can_spend(author, bid):
                raise InsufficientBalance
            await self.slot_machine(author, bid)
        except NoAccount:
            await self.bot.say("{} You need an ledger to use the slot "
                               "machine. Type `{}casino register` to open one."
                               "".format(author.mention, ctx.prefix))
        except InsufficientBalance:
            await self.bot.say("{} You need an ledger with enough funds to "
                               "play the slot machine.".format(author.mention))
        except OnCooldown:
            await self.bot.say("Slot machine is still cooling off! Wait {} "
                               "seconds between each pull".format(slot_time))
        except InvalidBid:
            await self.bot.say("Bid must be between {} and {}."
                               "".format(settings["SLOT_MIN"],
                                         settings["SLOT_MAX"]))

    async def slot_machine(self, author, bid):
        default_reel = deque(SMReel)
        reels = []
        self.slot_register[author.id] = datetime.utcnow()
        for i in range(3):
            default_reel.rotate(random.randint(-999, 999)) # weeeeee
            new_reel = deque(default_reel, maxlen=3) # we need only 3 symbols
            reels.append(new_reel)                   # for each reel
        rows = ((reels[0][0], reels[1][0], reels[2][0]),
                (reels[0][1], reels[1][1], reels[2][1]),
                (reels[0][2], reels[1][2], reels[2][2]))

        slot = "~~\n~~" # Mobile friendly
        for i, row in enumerate(rows): # Let's build the slot to show
            sign = "  "
            if i == 1:
                sign = ">"
            slot += "{}{} {} {}\n".format(sign, *[c.value for c in row])

        payout = PAYOUTS.get(rows[1])
        if not payout:
            # Checks for two-consecutive-symbols special rewards
            payout = PAYOUTS.get((rows[1][0], rows[1][1]),
                     PAYOUTS.get((rows[1][1], rows[1][2]))
                                )
        if not payout:
            # Still nothing. Let's check for 3 generic same symbols
            # or 2 consecutive symbols
            has_three = rows[1][0] == rows[1][1] == rows[1][2]
            has_two = (rows[1][0] == rows[1][1]) or (rows[1][1] == rows[1][2])
            if has_three:
                payout = PAYOUTS["3 symbols"]
            elif has_two:
                payout = PAYOUTS["2 symbols"]

        if payout:
            then = self.casino.get_balance(author)
            pay = payout["payout"](bid)
            now = then - bid + pay
            self.casino.set_flowers(author, now)
            await self.bot.say("{}\n{} {}\n\nYour bid: {}\n{} → {}!"
                               "".format(slot, author.mention,
                                         payout["phrase"], bid, then, now))
        else:
            then = self.casino.get_balance(author)
            self.casino.withdraw_flowers(author, bid)
            now = then - bid
            await self.bot.say("{}\n{} Nothing!\nYour bid: {}\n{} → {}!"
                               "".format(slot, author.mention, bid, then, now))

    @commands.group(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def gamblingset(self, ctx):
        """Changes gambling module settings"""
        server = ctx.message.server
        settings = self.settings[server.id]
        if ctx.invoked_subcommand is None:
            msg = "```"
            for k, v in settings.items():
                msg += "{}: {}\n".format(k, v)
            msg += "```"
            await send_cmd_help(ctx)
            await self.bot.say(msg)

    @gamblingset.command(pass_context=True)
    async def slotmin(self, ctx, bid: int):
        """Minimum slot machine bid"""
        server = ctx.message.server
        self.settings[server.id]["SLOT_MIN"] = bid
        await self.bot.say("Minimum bid is now {} :cherry_blossom:.".format(bid))
        dataIO.save_json(self.file_path, self.settings)

    @gamblingset.command(pass_context=True)
    async def slotmax(self, ctx, bid: int):
        """Maximum slot machine bid"""
        server = ctx.message.server
        self.settings[server.id]["SLOT_MAX"] = bid
        await self.bot.say("Maximum bid is now {} :cherry_blossom:.".format(bid))
        dataIO.save_json(self.file_path, self.settings)

    @gamblingset.command(pass_context=True)
    async def slottime(self, ctx, seconds: int):
        """Seconds between each slots use"""
        server = ctx.message.server
        self.settings[server.id]["SLOT_TIME"] = seconds
        await self.bot.say("Cooldown is now {} seconds.".format(seconds))
        dataIO.save_json(self.file_path, self.settings)

    @gamblingset.command(pass_context=True)
    async def paydaytime(self, ctx, seconds: int):
        """Seconds between each payday"""
        server = ctx.message.server
        self.settings[server.id]["PAYDAY_TIME"] = seconds
        await self.bot.say("Value modified. At least {} seconds must pass "
                           "between each payday.".format(seconds))
        dataIO.save_json(self.file_path, self.settings)

    @gamblingset.command(pass_context=True)
    async def paydayflowers(self, ctx, flowers: int):
        """Credits earned each payday"""
        server = ctx.message.server
        self.settings[server.id]["PAYDAY_CREDITS"] = flowers
        await self.bot.say("Every payday will now give {} :cherry_blossom:."
                           "".format(flowers))
        dataIO.save_json(self.file_path, self.settings)

    @gamblingset.command(pass_context=True)
    async def registerflowers(self, ctx, flowers: int):
        """Credits given on registering an ledger"""
        server = ctx.message.server
        if flowers < 0:
            flowers = 0
        self.settings[server.id]["REGISTER_CREDITS"] = flowers
        await self.bot.say("Registering an ledger will now give {} :cherry_blossom:."
                           "".format(flowers))
        dataIO.save_json(self.file_path, self.settings)

    # What would I ever do without stackoverflow?
    def display_time(self, seconds, granularity=2):
        intervals = (  # Source: http://stackoverflow.com/a/24542445
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),    # 60 * 60 * 24
            ('hours', 3600),    # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )

        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])


def check_folders():
    if not os.path.exists("data/gambling"):
        print("Creating data/gambling folder...")
        os.makedirs("data/gambling")


def check_files():

    f = "data/gambling/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default gambling's settings.json...")
        dataIO.save_json(f, {})

    f = "data/gambling/casino.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty casino.json...")
        dataIO.save_json(f, {})


def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("red.gambling")
    if logger.level == 0:
        # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='data/gambling/gambling.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(Gambling(bot))
