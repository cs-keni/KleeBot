import nextcord # noqa: F401
import server_code # noqa: F401
import respond # noqa: F401
import os # noqa: F401
import requests # noqa: F401
import json # noqa: F401
import random # noqa: F401
import pytz # noqa: F401
from weather_data import weather_voicelines, weather_emojis # noqa: F401
from nextcord.ext import commands # noqa: F401
from genshin_quotes import quotes # noqa: F401
from commands import command_descriptions # noqa: F401
from datetime import datetime # noqa: F401
from dotenv import load_dotenv # noqa: F401

# note: we will add noqa to ignore the warnings for unused imports