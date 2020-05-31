from discord import Client
from discord.message import Message
import discord
from app_utils import handle_searchapi
import json


# TODO: rewrite file for bot module
#
#
#


class MyClient(Client):
    def __init__(self):
        super().__init__()
        with open("app_utils/config.json", "r") as config:
            MyClient.prefix = json.loads(config.read())["prefix"]

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f"{MyClient.prefix}help"))
        print("Bot is ready")

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        if message.content.startswith(MyClient.prefix):
            stripped = message.content.split()
            if stripped[0] == f"{MyClient.prefix}google":
                if len(stripped) > 1:
                    embed = discord.Embed(title="Search results for", colour=discord.Colour(0xffffff),
                                          description=" ".join(stripped[1:]))
                    embed.set_footer(text=f"Search query sent by {message.author}")
                    for item in handle_searchapi.get_googlesearch(" ".join(stripped[1:])):
                        embed.add_field(name=item["title"], value=item["link"], inline=False)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(f"Incomplete search query: syntax {MyClient.prefix}google <query>")
            elif stripped[0] == f"{MyClient.prefix}prefix":
                if len(stripped) > 1:
                    MyClient.prefix = stripped[1]
                    with open("app_utils/config.json", "w") as config:
                        config.write(json.dumps({"prefix": stripped[1]}))
                else:
                    await message.channel.send("Prefix: " + MyClient.prefix)
            elif stripped[0] == f"{MyClient.prefix}help":
                await message.add_reaction("✅")
                embed = discord.Embed(colour=discord.Colour(0xe18704))
                embed.title = ""
                embed.description = ""
                embed.set_author(name=f"Help for {message.author}",
                                 icon_url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png")
                embed.set_footer(text=f"Bot made by {self.get_user(490636491039572009)}")
                embed.add_field(name=f"{MyClient.prefix}help", value="show help", inline=False)
                embed.add_field(name=f"{MyClient.prefix}google <query>", value="searches for a specific query", inline=False)
                embed.add_field(name=f"{MyClient.prefix}prefix <optional: new prefix>",
                                value="displays or changes the prefix", inline=False)
                await message.author.send(embed=embed)
            else:
                await message.channel.send(f"Command {stripped[0]} not found")


if __name__ == '__main__':
    try:
        with open("bot_token", "r") as token_file:
            token = token_file.read()
    except FileNotFoundError:
        print("You have to create a file named 'bot_token', which contains your bot token")
        exit(0)

    bot = MyClient()
    bot.run(token.strip())
