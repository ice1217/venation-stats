import discord
import os
import pymongo
from datetime import datetime
import pytz

mongodb_url = os.environ["MONGODB_URL"]
mongodb_db = os.environ["MONGODB_DB"]
client = pymongo.MongoClient(mongodb_url)
db = client[mongodb_db]

mongodb_message_col = 'message_log'
mongodb_voice_col = 'voice_log'
mongodb_duration_col = 'voice_duration_log'

token = os.environ['TOKEN']
client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  if message.guild.name != 'Venation':
    return

  if message.author == client.user:
    return

  elif message.author.name == 'tandai':
    return

  elif message.author.name == 'anya':
    return

  else:
    message_json = {
      'author': message.author.name,
      'channel': message.channel.name,
      'postingdate': message.created_at.__str__(),
      'content': message.content
    }
    col = db[mongodb_message_col]
    col.insert_one(message_json)
    return

@client.event
async def on_voice_state_update(member, before, after):
  
  if member.guild.name != 'Venation':
    return
  
  timezone_WIB = pytz.timezone('Asia/Jakarta')
  current_time = datetime.now(timezone_WIB).__str__()

  before_channel = ''
  after_channel = ''
  member_name = member.name

  if before.channel is None:
    before_channel = 'none'
  else:
    before_channel = before.channel.name

  if after.channel is None:
    after_channel = 'none'
  else:
    after_channel = after.channel.name

  voice_json = {
    'member': member_name,
    'before_channel': before_channel,
    'after_channel': after_channel,
    'timestamp': current_time
  }
  col = db[mongodb_voice_col]
  col.insert_one(voice_json)

  if before.channel is not None:
    q = {"member": member_name, "after_channel": before_channel}
    mydoc = col.find(q).limit(1).sort("timestamp",pymongo.DESCENDING)
    prev_entry = mydoc[0]
    prev_time = prev_entry["timestamp"]
    #print(prev_time)

    timeformat = "%Y-%m-%d %H:%M:%S.%f%z"

    diff = datetime.strptime(current_time, timeformat) - datetime.strptime(prev_time, timeformat)
    duration_str = str(diff.seconds) + "." + str(diff.microseconds)
    duration = float(duration_str)
    #print(duration)

    duration_json = {
          'member': member_name,
          'channel': before_channel,
          'start_time': prev_time,
          'end_time': current_time,
          'duration_seconds': duration
    }
    col = db[mongodb_duration_col]
    col.insert_one(duration_json)
    return
  
  else:
    return

client.run(token)
