import nextcord
import server_code
import respond
import os
import requests
import json
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv ()

USER_ID = os.getenv ("USER_ID")
WEATHER_KEY = os.getenv ("WEATHER_KEY")
BOT_TOKEN = os.getenv ("BOT_TOKEN")

intents = nextcord.Intents.all ()
intents.members = True

client = commands.Bot (command_prefix = '\\', intents = intents)

@client.event
async def on_ready ():
    print ("KleeBot Status: Online")
    
@client.event
async def on_command_error (ctx, error):
    if isinstance (error, commands.CommandNotFound):
        await ctx.send ("Command not found!")
    else:
        print (f"Error: {error}")
    
@client.command (aliases = ['hi', 'hey'])
async def hello (ctx):
    await ctx.message.delete ()
    await ctx.send (respond.ohayo)
    
@client.command ()
async def logoff (ctx):
    if ctx.author.id == USER_ID:
        await ctx.message.delete ()
        await ctx.send (respond.sayonara)
        await client.close ()
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
        main_weather = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        
        emoji = ""
        voiceline = ""
        if main_weather == "Clear":
            emoji = ':sunny:'
            voiceline = "Oh, it's sunny outside?! Yay! That means the perfect weather for my Boom-Boom adventures!"
        elif main_weather == "Rain":
            emoji = ':cloud_rain:'
            voiceline = "Mwauhahaha, lucky all my new bombs are waterproof!"
        elif main_weather == "Clouds":
            emoji = ':cloud:'
            voiceline = "Clouds, clouds, fluffy clouds! You know, they look just like the cotton candy I had at the Windblume Festival!"
        elif main_weather == "Thunderstorm":
            emoji = ':thunder_cloud_rain'
            voiceline = "What'd I blow up!? ...Oh wait, it's just thunder and lightning. Phew."
        elif main_weather == "Snow":
            emoji = ':cloud_snow:'
            voiceline = "I've got the bestest idea ever! Let's build a Dodoco snowman family! We'll start with Dodoco Dad, then Dodoco Mom, then Dodoco Baby, then... ah... ah.. achoo!"
        elif main_weather == "Drizzle":
            emoji = ':cloud_rain:'
            voiceline = "Hey! Hey! Did you know? If I throw a bomb into the rain, when it explodes, it'll make a white rainbow! I call it a boom-bow!"
        elif main_weather == "Mist":
            emoji = ':fog:'
            voiceline = "Misty days are like stepping into a dream! I'll use my Mystical Glitterbombs to make the mist shimmer and glow like stars in the sky!"
        elif main_weather == "Haze":
            emoji = ':fog:'
            voiceline = "Haze makes me think of stories of Big Sister Jean's and Grandpa Varka's adventures! I would go on adventures too, but Big Sister Jean says I'm too young. Hmph."
        elif main_weather == "Fog":
            emoji = ':fog:'
            voiceline = "Ehhh..?! Everything is so blurry! No.. No! It can't be! Am I already turning old?! Noooooo!"
        elif main_weather == "Smoke":
            emoji = ':fog:'
            voiceline = "Heh, my bombs are way more smoky than this! I'll show you! :bomb: :boom:"
        elif main_weather == "Squall":
            emoji = ':wind_blowing_face:'
            voiceline = "Dear Anemo God, please make Klee's bombs blow in the right direction and only blow up bad guys. The end."
        elif main_weather == "Tornado":
            emoji = ':cloud_tornado:'
            voiceline = "Fwuah!! Did I accidently make the Anemo God mad with my bombs?! I'm sorry!!"
        else:
            emoji = ':cold_sweat:'
            voiceline = "What's this? This is the first I've seen this type of weather!"
        
        await ctx.send (f"{emoji} Here is the weather in {location}! \nStatus: {main_weather}\nTemperature: {temperature}°F\nHumidity: {humidity}%")
        await ctx.send (voiceline)
    elif response.status_code == server_code.NOT_FOUND:
        await ctx.send ("Uh oh! I couldn't find that location!")
    else: # response.status_code == server_code.INTERNAL_SERVER_ERROR
        await ctx.send ("Oh no! The weather API is down!")
    
client.run (BOT_TOKEN)