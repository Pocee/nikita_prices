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

class MapButtonView(discord.ui.View):
    def __init__(self, maps_data):
        super().__init__(timeout=60)
        self.maps_data = maps_data
        
        # Filter maps that have bosses
        maps_with_bosses = {m['name']: m for m in maps_data if m.get('bosses')}
        
        # Create buttons for each map (limit to 25 buttons max)
        for map_name in list(maps_with_bosses.keys())[:25]:
            button = discord.ui.Button(label=map_name, style=discord.ButtonStyle.primary)
            button.callback = self.make_callback(map_name, maps_with_bosses[map_name])
            self.add_item(button)

    def make_callback(self, map_name, map_data):
        async def callback(interaction: discord.Interaction):
            boss_list = map_data.get('bosses', [])
            response = f"📍 **{map_name}**\n"
            
            for boss in boss_list:
                spawn_chance = int(boss['spawnChance'] * 100)
                response += f"\n☠️**{boss['name']} — Spawn: {spawn_chance}%**☠️"
                
                locations = boss.get('spawnLocations', [])
                if locations:
                    for loc in locations:
                        loc_chance = int(loc.get('chance', 1) * 100)
                        if loc_chance == 100:
                            response += f"\n> {loc['name']}"
                        else:
                            response += f"\n> {loc['name']} {loc_chance}%"
                else:
                    response += "\n> Sin ubicación"
            
            if len(response) > 2000:
                response = response[:1990] + "...\n(truncado)"
            
            await interaction.response.edit_message(content=response, view=None)
        return callback

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

@bot.command(name='bosses', aliases=['b'])
async def bosses(ctx, *, query: str = None):
    """Get boss spawn information for Tarkov maps"""
    logger.info(f'Bosses command received from {ctx.author} with query: {query}')
    
    try:
        maps_data = tarkov_client.get_maps_and_bosses()
        
        if not maps_data:
            await ctx.send("❌ No se pudo obtener información de mapas.")
            return
        
        # Command: !bosses all
        if query and query.strip().lower() == "all":
            response = "📍 **Bosses en Todos los Mapas**\n"
            for map_data in maps_data:
                boss_list = map_data.get('bosses', [])
                if not boss_list:
                    continue
                
                map_name = map_data['name']
                boss_entries = [f"{b['name']} ({int(b['spawnChance'] * 100)}%)" for b in boss_list]
                response += f"\n**{map_name}**: {', '.join(boss_entries)}"
            
            if len(response) > 2000:
                response = response[:1990] + "...\n(truncado)"
            await ctx.send(response)
            return
        
        # If no query, show buttons to choose map
        if not query:
            view = MapButtonView(maps_data)
            await ctx.send("📌 Selecciona un mapa:", view=view)
            return
        
        query = query.strip()
        
        # Search by exact map name
        for map_data in maps_data:
            if map_data['name'].lower() == query.lower():
                boss_list = map_data.get('bosses', [])
                response = f"📍 **Bosses en {map_data['name']}**\n"
                
                for boss in boss_list:
                    spawn_chance = int(boss['spawnChance'] * 100)
                    response += f"\n☠️**{boss['name']} — Spawn: {spawn_chance}%**☠️"
                    
                    locations = boss.get('spawnLocations', [])
                    if locations:
                        for loc in locations:
                            loc_chance = int(loc.get('chance', 1) * 100)
                            if loc_chance == 100:
                                response += f"\n> {loc['name']}"
                            else:
                                response += f"\n> {loc['name']} {loc_chance}%"
                    else:
                        response += "\n> Sin ubicación"
                
                if len(response) > 2000:
                    response = response[:1990] + "...\n(truncado)"
                await ctx.send(response)
                return
        
        # Search by boss name
        found = []
        for map_data in maps_data:
            for boss in map_data.get('bosses', []):
                if boss['name'].lower() == query.lower():
                    found.append((map_data['name'], boss))
        
        if found:
            response = f"🔍 **'{query}' aparece en:**\n"
            for map_name, boss in found:
                spawn_chance = int(boss['spawnChance'] * 100)
                response += f"\n☠️**{map_name} — Spawn: {spawn_chance}%**☠️"
                
                locations = boss.get('spawnLocations', [])
                if locations:
                    for loc in locations:
                        loc_chance = int(loc.get('chance', 1) * 100)
                        if loc_chance == 100:
                            response += f"\n> {loc['name']}"
                        else:
                            response += f"\n> {loc['name']} {loc_chance}%"
                else:
                    response += "\n> Sin ubicación"
            
            if len(response) > 2000:
                response = response[:1990] + "...\n(truncado)"
            await ctx.send(response)
            return
        
        await ctx.send(f"❌ No se encontró '{query}'. Usa `!bosses` sin argumentos para ver los mapas.")
    
    except Exception as e:
        logger.error(f"Error processing bosses command: {e}", exc_info=True)
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='help', aliases=['h'])
async def help_command(ctx):
    """Show available commands"""
    help_text = (
        "🛠️ **Comandos disponibles:**\n"
        "`!price <item>` o `!p <item>` → Muestra precios del mercado.\n"
        "`!bosses` o `!b` → Muestra botones para elegir mapa.\n"
        "`!bosses <mapa>` → Muestra bosses de ese mapa.\n"
        "`!bosses <nombre>` → Busca un boss por nombre.\n"
        "`!bosses all` → Lista compacta de todos los bosses.\n"
        "`!ping` → Verifica si el bot está activo.\n"
    )
    await ctx.send(help_text)

if __name__ == "__main__":
    if not TOKEN or TOKEN == "your_token_here":
        logger.error("DISCORD_TOKEN not set in .env file.")
        print("Error: DISCORD_TOKEN not set in .env file.")
    else:
        logger.info("Starting bot...")
        bot.run(TOKEN)
