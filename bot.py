import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from tarkov_client import TarkovClient
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('tarkov_bot')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
tarkov_client = TarkovClient()

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f'Error in command {ctx.command}: {error}')
    await ctx.send(f"An error occurred: {str(error)}")

@bot.command(name='ping')
async def ping(ctx):
    """Simple ping command to test if bot is responding"""
    logger.info(f'Ping command received from {ctx.author}')
    await ctx.send('🏓 Pong!')

@bot.command(name='price', aliases=['p'])
async def price(ctx, *, item_name: str = None):
    """Get price information for a Tarkov item"""
    logger.info(f'Price command received from {ctx.author} for item: {item_name}')
    
    if not item_name:
        await ctx.send("Please provide an item name. Usage: `!price <item_name>`")
        return
    
    try:
        items = tarkov_client.get_item_price(item_name)
        logger.info(f'Found {len(items) if items else 0} items for query: {item_name}')
        
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
            logger.info(f'Sent price info for {name}')

    except Exception as e:
        logger.error(f"Error processing price command: {e}", exc_info=True)
        await ctx.send(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if not TOKEN or TOKEN == "your_token_here":
        logger.error("DISCORD_TOKEN not set in .env file.")
        print("Error: DISCORD_TOKEN not set in .env file.")
    else:
        logger.info("Starting bot...")
        bot.run(TOKEN)
