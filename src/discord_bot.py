import os
import json
import datetime as dt
import openai
import discord
from logging import getLogger, INFO, DEBUG, Formatter
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    r'./log/discord_bot.log',
    encoding='utf-8',
    maxBytes=100000,
    backupCount=5
)
handler.setLevel(DEBUG)
formatter = Formatter(
    '%(asctime)s : %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)

logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

intents = discord.Intents.default()
intents.message_content = True

openai.api_key = os.getenv('OPENAI_API_KEY')

DISCORD_CHANNEL_NAME = 'gpt'
MODEL_NAME = 'gpt-3.5-turbo-16k-0613'
HISTORY_LIMIT = 30

def completion_gpt(messages):
    logger.debug(messages)
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages
    )

    logger.debug(json.dumps(response))
    return response.choices[0].message.content

class MyClient(discord.Client):
    async def on_ready(self):
        logger.info(f'Logged on as {self.user}')
        logger.info('Model Name > %s', MODEL_NAME)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        logger.debug(message)

        if type(message.channel) is discord.TextChannel and message.channel.name == DISCORD_CHANNEL_NAME:
            # await message.channel.send(completion_gpt(message.content))
            thread = await message.create_thread(name=message.content[:90])
            await message.add_reaction('\U0001F4E9')
            # await thread.send('You said: ' + message.content)
            await thread.send(completion_gpt([{
                'role': 'user',
                'content': message.content
            }]))


        if type(message.channel) is discord.Thread and message.channel.parent.name == DISCORD_CHANNEL_NAME:
            # await message.channel.send('You said: ' + message.content)
            to_gpt_message = []
            async for post in message.channel.history(limit=HISTORY_LIMIT):
                if post.type == discord.MessageType.thread_starter_message:
                    post.author = 'user'
                    post.content = post.system_content

                if post.author == self.user:
                    role = 'assistant'
                else:
                    role = 'user'

                to_gpt_message.append({
                    'role': role,
                    'content': post.content,
                    'created_at': post.created_at
                })

            to_gpt_message = sorted(to_gpt_message, key=lambda d: d['created_at'])
            to_gpt_message = [{k: v for k, v in d.items() if k != 'created_at'}
                               for d in to_gpt_message]

            await message.add_reaction('\U0001F4E9')
            await message.channel.send(completion_gpt(to_gpt_message))


client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_BOT_TOKEN'))
