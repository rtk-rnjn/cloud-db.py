# Cloud-DB.py

An easy-to-use Wrapper for the Cloud-DB API.

**Join the Discord server in links to get an API Key!**

## Installing

Python 3.8 or higher is required.

```md
# Linux/macOS

python3 -m pip install -U cloud-db.py

# Windows

py -3 -m pip install -U cloud-db.py

```

## Usage

```python
from cloud_db import Client

# import the package

db = Client("API Key")
# Contruct the client with API Key
# OR 
db = Client("API Key", auto_retry = True)
# Contruct the client with API Key with auto_retry set to True
# auto_retry basically is to tell the lib to retry if you're on cooldown.
# This makes it almost impossible to get to get the OnCooldown exception.

# Join the Discord server to get an API Key!
```

## Examples

Please read the docstring on all of these.

```python
await db.set("Hello", "World") # True
# or
await db.set("Hello", "World", return_data = True)
# return_data set to True to get the data returned instead of just a boolean.
# Result(success = True, message = Success, data = Data(name = 'Hello', value = World))

await db.get("Hello")
# Result(success = True, message = Success, data = Data(name = 'Hello', value = World))

# or

await db.get("Hello", only_value = True) # World
# only_value set to True to only get the value of the key instead of a Result() object. 

await db.all()
# Result(success = True, message = Success, data = [Data(name = 'Hello', value = World)])

await db.delete("Hello") # True

await db.set("Number", 100) # True

await db.add("Number", 200)
# Result(success = True, message = Success, data = None, number = 300)

await db.subtract("Number", 300)
# Result(success = True, message = Success, data = None, number = 0)

await db.all()
# Result(success = True, message = Success, data = [Data(name = 'Number', value = 0)])

await db.delete("Hello") # True

await db.all()
# Result(success = True, message = Success, data = None)
```

## Real-Life Example

Usage in a [discord.py](https://github.com/Rapptz/discord.py) Bot. In this example we are storing user bio's. \

```python
import discord
from discord.ext import commands
from cloud_db import Client

bot = commands.Bot(command_prefix = "cd!")
# assigning our db to the bot so we can access it anywhere we got access to the bot.
bot.db = Client("API Key")


# Make sure you've done this -> await db.set("user_bios", {}), add the user_bios key so we can edit it each time.

async def user_has_bio(user_id: int) -> bool:
    all_bios = await bot.db.get("user_bios", only_value = True)
    if str(user_id) not in all_bios:
        return False

    return True


async def add_or_edit_bio(user_id: int, bio: str) -> None:
    all_bios = await bot.db.get("user_bios", only_value = True)
    all_bios[str(user_id)] = str(bio)
    await bot.db.set("user_bios", all_bios)


async def remove_bio(user_id: int) -> None:
    all_bios = await bot.db.get("user_bios", only_value = True)
    del all_bios[str(user_id)]
    await bot.db.set("user_bios", all_bios)


async def get_user_bio(user_id: int) -> str:
    all_bios = await bot.db.get("user_bios", only_value = True)
    return all_bios[str(user_id)]


@bot.command(aliases = ["setbio"])
async def addbio(ctx, bio: str):
    check_if_exists = await user_has_bio(ctx.author.id)
    if check_if_exists is True:
        await ctx.send(
            f"{ctx.author.mention}, you aleady have a bio set. You can edit it via {ctx.prefix}editbio"
            f" or see it in {ctx.prefix}userinfo."
        )
        return

    await add_or_edit_bio(ctx.author.id, bio)
    await ctx.send(f"{ctx.author.mention}, successfully set that as your bio. See it in {ctx.prefix}userinfo.")
    return


@bot.command(aliases = ["changebio"])
async def editbio(ctx, bio: str):
    check_if_exists = await user_has_bio(ctx.author.id)
    if check_if_exists is False:
        await ctx.send(f"{ctx.author.mention}, you don't have a bio set. You can set one via {ctx.prefix}addbio")
        return

    await add_or_edit_bio(ctx.author.id, bio)
    await ctx.send(f"{ctx.author.mention}, successfully edited your bio to that. See it in {ctx.prefix}userinfo.")
    return


@bot.command(aliases = ["deletebio"])
async def removebio(ctx):
    check_if_exists = await user_has_bio(ctx.author.id)
    if check_if_exists is False:
        await ctx.send(f"{ctx.author.mention}, you don't have a bio set. You can set one via {ctx.prefix}addbio.")
        return

    await remove_bio(ctx.author.id)
    await ctx.send(
        f"{ctx.author.mention}, successfully removed your bio. You can use {ctx.prefix}addbio to set one again.")
    return


@bot.command()
async def userinfo(ctx, member: discord.Member):
    member = member or ctx.author

    emb = discord.Embed(
        title = "Userinfo",
        description = f"**Full Name:** {member}\n**ID:** {member.id}",
        colour = member.colour
    )

    has_bio = await user_has_bio(ctx.author.id)
    if has_bio is True:
        bio = await get_user_bio(ctx.author.id)
        emb.add_field(
            name = "✏️Bio",
            value = str(bio)
        )

    await ctx.send(embed = emb)


# Extra command to get all bio's as bot owner, for some reason.
@bot.command()
@commands.is_owner()
async def allbios(ctx):
    all_bios = await bot.db.get("user_bios")
    list_to_join = [f"**User ID:** {uid}\n**Bio:** {bio}\n" for uid, bio in all_bios.items()]
    if not list_to_join:
        return await ctx.send("looks like there a no bio's..")

    return await ctx.send("\n".join(list_to_join))

```

## Links

- API: https://cloud-db.ml/
- Discord Server: https://discord.gg/nEtTMS934g
- Wrapper Creator server: https://discord.gg/yCzcfju
- JavaScript version: https://www.npmjs.com/package/cloud-db.js

This is a really basic wrapper for the cloud-db API. Any suggestions are welcome!