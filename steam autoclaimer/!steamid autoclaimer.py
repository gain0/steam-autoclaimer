import os
import aiohttp
import asyncio
from colorama import Fore, Style
import keyboard

async def check_username(session, username, success_flag, lock):
    url = f'https://steamcommunity.com/id/{username}'
    try:
        async with session.get(url) as response:
            text = await response.text(encoding='utf-8', errors='ignore')

            if not success_flag.is_set() and 'The specified profile could not be found.' in text:
                async with lock:  # Acquire lock for exclusive access
                    if not success_flag.is_set():
                        print(f"{Fore.GREEN}{username}: available{Style.RESET_ALL}")
                        keyboard.write(username)  # Type the username
                        await asyncio.sleep(0.5)  # Add a delay of 0.5 seconds
                        keyboard.send('enter')  # Hit Enter after typing
                        success_flag.set()  # Set the flag to indicate success
                return True  # Indicate username found and typed
    except aiohttp.ClientError as e:
        print(f"Checking username: {Fore.YELLOW}{username}: error - {e}{Style.RESET_ALL}")

    return False  # Indicate username not found

async def check_usernames_from_file():
    try:
        folder_name = "lists"  # Change this to your folder name
        file_name = input(f"Enter the name of the file containing usernames in '{folder_name}' (e.g., usernames.txt): ")

        # Construct the full path to the file within the folder
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        file_path = os.path.join(folder_path, file_name)

        async with aiohttp.ClientSession() as session:
            print(f"Opening file: {file_path}")
            with open(file_path, 'r') as file:
                usernames = file.read().splitlines()
                success_flag = asyncio.Event()  # Success flag outside loop
                lock = asyncio.Lock()  # Lock to synchronize typing
                first_loop = True

                for loop_count in range(1, len(usernames) + 1):
                    print(f"Loop #{loop_count}")

                    if first_loop:
                        print("Starting in 5 seconds...")
                        for i in range(5, 0, -1):
                            print(f"Countdown: {i}")
                            await asyncio.sleep(1)
                        first_loop = False  # Update flag after countdown

                    tasks = [check_username(session, username, success_flag, lock) for username in usernames]
                    await asyncio.gather(*tasks)

                    # Check if success flag is set, break the loop if it is
                    if success_flag.is_set():
                        print("Success! Exiting the loop.")
                        break

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
