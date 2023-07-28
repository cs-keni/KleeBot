import nextcord
import server_code
import respond
import os
import requests
import json
from weather_data import weather_voicelines, weather_emojis
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv ()

USER_ID = int (os.getenv ("USER_ID")) # need to use int () because getenv returns a string
WEATHER_KEY = os.getenv ("WEATHER_KEY")
BOT_TOKEN = os.getenv ("BOT_TOKEN")

intents = nextcord.Intents.all ()
intents.members = True

client = commands.Bot (command_prefix = '\\', intents = intents)

is_bot_running = False

@client.event
async def on_ready ():
    global is_bot_running
    print ("KleeBot Status: Online")
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
        

#make a ping pong command later!    

@client.command ()
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
            await ctx.message.delete ()
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
        await ctx.send ("Please specify a location! Here is an example usage: \\weather Mondstadt")
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
        await ctx.send ("Uh oh! I couldn't find that location!")
    else: # response.status_code == server_code.INTERNAL_SERVER_ERROR
        await ctx.send ("Oh no! The weather API is down!")
    
client.run (BOT_TOKEN)