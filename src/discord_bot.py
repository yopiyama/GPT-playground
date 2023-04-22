import os
import datetime as dt
import openai
import discord
from logging import getLogger, INFO, DEBUG, StreamHandler

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False

intents = discord.Intents.default()
intents.message_content = True

openai.api_key = os.getenv('OPENAI_API_KEY')

DISCORD_CHANNEL_NAME = 'gpt'

def completion_gpt(messages):
    logger.debug(messages)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    logger.debug(response.choices[0].message.content)
    return response.choices[0].message.content

class MyClient(discord.Client):
    async def on_ready(self):
        logger.info(f'Logged on as {self.user}')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        logger.debug(message)

        if type(message.channel) is discord.TextChannel and message.channel.name == DISCORD_CHANNEL_NAME:
            # await message.channel.send(completion_gpt(message.content))
            thread = await message.create_thread(name=message.content)
            await message.add_reaction('\U0001F4E9')
            # await thread.send('You said: ' + message.content)
            await thread.send(completion_gpt([{
                'role': 'user',
                'content': message.content
            }]))


        if type(message.channel) is discord.Thread and message.channel.parent.name == DISCORD_CHANNEL_NAME:
            # await message.channel.send('You said: ' + message.content)
            to_gpt_message = []
            async for post in message.channel.history(limit=10):
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

            await message.channel.send(completion_gpt(to_gpt_message))


client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_BOT_TOKEN'))
