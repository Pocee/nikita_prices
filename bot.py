import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from tarkov_client import TarkovClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
tarkov_client = TarkovClient()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='price')
async def price(ctx, *, item_name):
    try:
        items = tarkov_client.get_item_price(item_name)
        if not items:
            await ctx.send(f"No items found matching '{item_name}'.")
            return

        # Limit to first 3 results to avoid spam
        for item in items[:3]:
            name = item.get('name', 'Unknown')
            short_name = item.get('shortName', 'Unknown')
            avg_price = item.get('avg24hPrice', 'N/A')
            base_price = item.get('basePrice', 'N/A')
            change_48h = item.get('changeLast48hPercent', 'N/A')
            link = item.get('link', '')
            
            # Format sellFor prices (best price)
            sell_for = item.get('sellFor', [])
            best_sell = max(sell_for, key=lambda x: x['price']) if sell_for else None
            best_sell_str = f"{best_sell['price']} ({best_sell['source']})" if best_sell else "N/A"

            embed = discord.Embed(title=f"{name} ({short_name})", url=link, color=0x00ff00)
            embed.add_field(name="Avg 24h Price", value=f"{avg_price} ₽", inline=True)
            embed.add_field(name="Base Price", value=f"{base_price} ₽", inline=True)
            embed.add_field(name="Best Sell", value=f"{best_sell_str}", inline=True)
            embed.add_field(name="48h Change", value=f"{change_48h}%", inline=True)
            
            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    if not TOKEN or TOKEN == "your_token_here":
        print("Error: DISCORD_TOKEN not set in .env file.")
    else:
        bot.run(TOKEN)
