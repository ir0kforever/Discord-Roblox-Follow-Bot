from discord.ext import commands
import discord, requests, random, threading, asyncio

with open('cookies.txt', 'r') as cookies:
    cookies1 = cookies.read().splitlines()

bot = commands.Bot(command_prefix='.?')

@bot.event
async def on_ready():
    print('Bot is online!')

def follow_user(cookie, prox, userid):
    with requests.session() as session:
        try:
            proxy = {'http':prox, 'https':prox}
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.get('https://www.roblox.com/home').content.decode('utf8').split("Roblox.XsrfToken.setToken('")[1].split("');")[0]
            follow = session.post(f'https://friends.roblox.com/v1/users/{userid}/follow', proxies=proxy)
        except:
            pass

def add_user(cookie, userid):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.get('https://www.roblox.com/home').content.decode('utf8').split("Roblox.XsrfToken.setToken('")[1].split("');")[0]
            session.post(f'https://friends.roblox.com/v1/users/{userid}/request-friendship')
    except:
        pass



@bot.command()
async def follow(ctx, userId):
    await ctx.send(f'<@{ctx.author.id}>, we have started the follow bot!')
    prox = ""
    for chunk in requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=150000&country=all&ssl=all&anonymity=all').iter_content(chunk_size=10000):
        if chunk:
            chunk = chunk.decode()
            prox += chunk
    proxies = prox.splitlines()
    for x in range(1):
        for x in cookies1:
            threading.Thread(target=follow_user, args=(x, random.choice(proxies), userId,)).start()
            await asyncio.sleep(0.01)

@bot.command()
async def friends(ctx, userId):
    await ctx.send(f'<@{ctx.author.id}>, we have started the friend bot!')
    for x in cookies1:
        threading.Thread(target=add_user, args=(x, userId,)).start()


@bot.command()
async def cookies(ctx):
    await ctx.send(f'There are currently {len(cookies1)} cookies in our server!')
            



bot.run(TOKEN) # Token goes here
