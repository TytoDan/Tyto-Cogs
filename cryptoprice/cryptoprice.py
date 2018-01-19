import discord
from discord.ext import commands
from cryptocompy import price

class CryptoPrice:
    """Check price of cryptocurrencies!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='price', pass_context=True)
    async def price(self, ctx, coin, returnCurr='USD', ex='all'):
        """Checks current price and 24hr percentage change of a coin. Optionally specify the return currency and the exchange (eg GDAX)."""
        coin = coin.upper()
        returnCurr = returnCurr.upper()
        #Cryptocompare switches IOTA and IOT for some reason, this just fixes that
        if coin == "IOTA":
            coinSearch = "IOT"
        elif coin == "IOT":
            coinSearch = "IOTA"
        else:
            coinSearch = coin

        #Get dictionary of coin info, then try to get the price (p) and 24hr change (c24h) from the API.
        try:
            print("Trying to get coin from API")
			dict = price.get_current_price(coinSearch, returnCurr, e=ex, try_conversion=True, full=True, format='display')
			print("Trying to get price from returned JSON")
            p = dict[coinSearch][returnCurr]['PRICE'].replace(" ", "")
			print("Trying to get 24hr change")
            c24h = dict[coinSearch][returnCurr]['CHANGEPCT24HOUR']
            print("Got everything, saying message")
			await self.bot.say("The current price of {} is {} ({}%)".format(coin,p,c24h))
        except KeyError as e:
            print("KeyError. Can't find data!", e)
            await self.bot.say("Something went wrong. Check console log for more information.")

def setup(bot):
    bot.add_cog(CryptoPrice(bot))