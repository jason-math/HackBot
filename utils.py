import random
import json
import os
from settings_files import *
import discord
from discord.ext import commands


def in_bot_commands():
    def predicate(ctx):
        return ctx.message.channel.name == "bot-commands"
    return commands.check(predicate)


vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)


def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

    return text


async def create_channel(guild, author, users):
    private_category = None
    for category in guild.categories:
        if category.name == "Private Voice Channels":
            private_category = category
            break
    if private_category is None:
        return
    channel_name = "%s's room" % author.name
    for channel in guild.voice_channels:
        if channel.name == channel_name.lower():
            await channel.delete()
            break
    await guild.create_voice_channel(channel_name, category=private_category)
    private_channel = None
    for channel in guild.voice_channels:
        if channel.name == channel_name.lower():
            private_channel = channel
            break
    if private_channel is None:
        return
    hacker_role = None
    for role in guild.roles:
        if role.name == "Hacker":
            hacker_role = role
            break
    if hacker_role is None:
        hacker_role = guild.default_role
    await private_channel.set_permissions(guild.default_role, view_channel=False, send_messages=False)
    await private_channel.set_permissions(hacker_role, view_channel=False, send_messages=False)
    await private_channel.set_permissions(author, view_channel=False, send_messages=False)
    for user in users:
        await private_channel.set_permissions(user, view_channel=True, send_messages=True)
    return private_channel
