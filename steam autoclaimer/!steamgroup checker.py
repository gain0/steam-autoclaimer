import aiohttp
import asyncio
import os
from colorama import Fore, Style

async def check_username(session, username):
    url = f'https://steamcommunity.com/groups/{username}'
    try:
        async with session.get(url) as response:
            text = await response.text(encoding='utf-8', errors='ignore')

            if 'No group could be retrieved for the given URL.' in text:
                print(f"{Fore.GREEN}{username}: available{Style.RESET_ALL}")
    except aiohttp.ClientError as e:
        print(f"Checking username: {Fore.YELLOW}{username}: error - {e}{Style.RESET_ALL}")

async def check_usernames_from_file():
    try:
        folder_path = "lists"  # Folder name where your lists are stored
        file_name = input("Enter the name of the file containing usernames (e.g., usernames.txt): ")
        file_path = os.path.join(folder_path, file_name)

        async with aiohttp.ClientSession() as session:
            print(f"Opening file: {file_path}")
            with open(file_path, 'r') as file:
                usernames = file.read().splitlines()
                tasks = [check_username(session, username) for username in usernames]
                await asyncio.gather(*tasks)
    except FileNotFoundError:
        print(f"File '{file_path}' not found")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to exit...")

async def main():
    await check_usernames_from_file()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
