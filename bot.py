from discord import Client
from discord.message import Message
import discord
from app_utils import handle_searchapi
# import handle_searchapi


class MyClient(Client):
    @staticmethod
    async def on_ready():
        print("Bot is ready")

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        if message.content.startswith("?"):
            stripped = message.content.split()
            if stripped[0] == "?google":
                if len(stripped) > 1:
                    embed = discord.Embed(title="Search results for", colour=discord.Colour(0xffffff),
                                          description=" ".join(stripped[1:]))
                    embed.set_footer(text=f"Search query sent by {message.author}")
                    for item in handle_searchapi.get_googlesearch(" ".join(stripped[1:])):
                        embed.add_field(name=item["title"], value=item["link"], inline=False)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Incomplete search query: syntax ?google <query>")

            if stripped[0] == "?help":
                await message.add_reaction("✅")
                embed = discord.Embed(colour=discord.Colour(0xe18704))
                embed.title = ""
                embed.description = ""
                embed.set_author(name=f"Help for {message.author}",
                                 icon_url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png")
                embed.set_footer(text=f"Bot made by {self.get_user(490636491039572009)}")
                embed.add_field(name="?help", value="show help", inline=False)
                embed.add_field(name="?google <query>", value="searches for a specific query", inline=False)
                await message.author.send(embed=embed)
            else:
                await message.channel.send(f"Command {stripped[0]} not found")


if __name__ == '__main__':
    try:
        with open("token", "r") as token_file:
            token = token_file.read()
    except FileNotFoundError:
        print("You have to create a file named 'token', which contains your bot token")
        exit(0)

    bot = MyClient()
    bot.run(token.strip())
