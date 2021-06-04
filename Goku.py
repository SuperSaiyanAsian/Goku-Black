"""A program that brings a discord chat bot to life when run."""

import logging
import time
import asyncio
import discord


"""Log data."""
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

messages = joined = 0


def read_token():
    """Read token from text file."""
    with open("token.txt", "r") as file:
        lines = file.readlines()
        return lines[0].strip()


def read_server_id():
    """Read server id from text file."""
    with open("id.txt", "r") as file:
        lines = file.readlines()
        return lines[0].strip()


token = read_token()
serverid = int(read_server_id())
client = discord.Client()


async def update_stats():
    """Update stats.txt every minute."""
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as file:
                file.write(
                    f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(60)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)


@client.event
async def on_ready():
    """Confirm successful login and display listening status."""
    act = discord.Activity(
        name='your commands', type=discord.ActivityType.listening)
    await client.change_presence(activity=act)
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    """Greet newcomers."""
    global joined
    joined += 1

    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server, {member.mention}!""")


@client.event
async def on_message(message):
    """React to certain messages."""
    global messages
    messages += 1
    id = client.get_guild(serverid)

    if message.author == client.user:
        return
    if message.content == "Help":
        embed = discord.Embed(title="Help with commands",
                              description="List of what I am able to do")
        embed.add_field(name="Hello", value="Greets the user")
        embed.add_field(name="sad", value="Express sadness")
        embed.add_field(name="users", value="Prints number of users")
        await message.channel.send(content=None, embed=embed)
    if message.content.find('hello') != -1:
        await message.channel.send('Hello!')
    if message.content.find('sad') != -1:
        await message.channel.send(';(')
    if message.content.find('users') != -1:
        await message.channel.send(f"""# of Members: {id.member_count}""")


client.loop.create_task(update_stats())
client.run(token)
