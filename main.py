from imports import *

load_dotenv ()

USER_ID = int (os.getenv ("USER_ID")) # need to use int () because getenv returns a string
WEATHER_KEY = os.getenv ("WEATHER_KEY")
BOT_TOKEN = os.getenv ("BOT_TOKEN")

intents = nextcord.Intents.all ()
intents.members = True
intents.typing = False
intents.presences = False

client = commands.Bot (command_prefix = '\\', intents = intents)

is_bot_running = False

@client.event
async def on_ready ():
    global is_bot_running
    print (respond.online)
    is_bot_running = True
    
@client.event
async def on_command_error (ctx, error):
    if isinstance (error, commands.CommandNotFound):
        await ctx.send ("Command not found!")
    else:
        print (f"Error: {error}")
    
@client.command (aliases = ['hi', 'hey'])
async def hello (ctx):
    if is_bot_running:
        # gonna purposely leave out ctx.message.delete () for funsies
        await ctx.send (respond.hello) # might change this response later haha
    else:
        await ctx.send (respond.not_running)
        

@client.command ()
async def ping (ctx):
    await ctx.send (respond.pong)
    latency = f"Latency: {round (client.latency * 1000)}ms"
    await ctx.send (latency)

@client.command () # something wrong with this command...
async def logon (ctx):
    global is_bot_running 
    if ctx.author.id == USER_ID:
        if not is_bot_running:
            await ctx.message.delete ()
            await ctx.send (respond.ohayo)
            is_bot_running = True
        else:
            await ctx.send (respond.already_on)
    else:
        await ctx.send (respond.no_perms)
    
@client.command ()
async def logoff (ctx):
    global is_bot_running
    if ctx.author.id == USER_ID:
        if is_bot_running:
            await ctx.send (respond.sayonara)
            await client.close ()
            is_bot_running = False
        else:
            await ctx.send (respond.not_running)
    else:
        await ctx.send (respond.no_perms)
        
@client.command ()
async def weather (ctx, *, location = None):
    # just in case if the user only does \weather instead of \weather <location>
    if location is None:
        await ctx.message.delete ()
        await ctx.send (respond.specify_location)
        return
    
    api_key = WEATHER_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {"q": location, "appid": api_key, "units": "imperial"}
    
    response = requests.get (base_url, params = params)
    
    if response.status_code == server_code.OK:
        weather_data = response.json ()
        main_weather = weather_data["weather"][0]["main"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        
        if main_weather in weather_voicelines:
            voiceline = weather_voicelines[main_weather]
            emoji = weather_emojis[main_weather]
        else:
            voiceline = respond.unknown_weather
            emoji = ":cold_sweat:"
        
        await ctx.send (f"{emoji} Here is the weather in {location}! \nStatus: {main_weather}\nTemperature: {temperature}°F\nHumidity: {humidity}%")
        await ctx.send (voiceline)
    elif response.status_code == server_code.NOT_FOUND:
        await ctx.send (respond.location_not_found)
    else: # response.status_code == server_code.INTERNAL_SERVER_ERROR
        await ctx.send (respond.weather_down)
        
@client.command (aliases = ['qotd', 'get_quote', 'quote_of_the_day'])
async def quote (ctx):
    if is_bot_running:
        pdt = pytz.timezone ('America/Los_Angeles') # setting it to PDT since it's my timezone
        now = datetime.now (pdt)
        today = now.strftime ('%Y-%m-%d') #formatting it to YYYY-MM-DD to fix bug
        random.seed (today) # seeding the random number generator with the current date
        quote = random.choice (quotes)
        await ctx.send (quote)
    else:
        await ctx.send (respond.not_running)
        
@client.command (aliases = ['dice', 'diceroll', 'roll', 'rolldice', 'dice_roll'])
async def roll_dice (ctx):
    dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    number = random.randint (1, 6)
    dice_emoji = dice_faces[number - 1]
    await ctx.send (f"You rolled a {number}! {dice_emoji}")
    
@client.command (aliases = ['a', 'av'])
async def avatar (ctx, member: nextcord.Member = None):
    if not member:
        member = ctx.author
    avatar_url = member.avatar.url
    embed = nextcord.Embed (title = f"{member.display_name}'s Avatar", color = nextcord.Color.blurple ())
    embed.set_image (url = avatar_url)
    await ctx.send (embed=embed)
    
client.run (BOT_TOKEN)