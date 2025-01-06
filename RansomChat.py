# Author: Antonio Brandao
# Ransomware group chat files: https://github.com/Casualtek/Ransomchats/tree/main
# Thanks to Valéry Marchive - hthttps://twitter.com/ValeryMarchive

import os  # For file and directory operations
import json  # For JSON handling, though not directly used here
from colorama import init, Fore, Style  # For colored console output
import re  # For regular expressions, though not directly used here

# Initialize colorama for Windows support
init()

# Conditional imports based on API choice
api_choice = input(f"{Fore.YELLOW}Choose API (1 for OpenAI, 2 for xAI Grok): {Style.RESET_ALL}")
if api_choice == "1":
    from openai import OpenAI as Client
    api_key_env = "OPENAI_API_KEY"
    default_model = "gpt-4o"  # Using the latest model available
elif api_choice == "2":
    from openai import OpenAI as Client
    api_key_env = "XAI_API_KEY"
    default_model = "grok-beta"
    client_kwargs = {"base_url": "https://api.x.ai/v1"}
else:
    raise ValueError("Invalid API choice")

def load_behavior(group_name):
    """
    Load behavior patterns from a text file for a specific ransomware group.
    
    :param group_name: Name of the ransomware group
    :return: Dictionary with behavior categories and messages
    """
    behavior_file = f"{group_name}_behavior.txt"
    if not os.path.exists(behavior_file):
        raise FileNotFoundError(f"Behavior file for {group_name} not found.")
    
    behavior = {}
    current_category = None
    with open(behavior_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.endswith(':'):
                current_category = line[:-1].lower()
                behavior[current_category] = []
            elif line and current_category:
                behavior[current_category].append(line[2:])
    
    return behavior

def format_bytes(size):
    """
    Convert bytes to a human-readable format.
    
    :param size: Size in bytes
    :return: Formatted size string
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if size < 1024:
            return f"{size:.2f}{unit}B"
        size /= 1024

def show_behavior_options():
    """
    Display available ransomware groups sorted by behavior file size.
    
    :return: Chosen group name
    """
    base_path = 'Ransomchats-main'
    groups = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    # Gather file sizes
    group_sizes = []
    for group in groups:
        file_path = f"{group}_behavior.txt"
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)  # Size in bytes
            group_sizes.append((group, size))
        else:
            group_sizes.append((group, 0))  # File not found, size 0

    # Sort by file size in descending order
    sorted_groups = sorted(group_sizes, key=lambda x: x[1], reverse=True)
    
    print(f"{Fore.YELLOW}Available Ransomware Groups (ordered by behavior file size, largest to smallest):{Style.RESET_ALL}")
    for index, (group, size) in enumerate(sorted_groups, 1):
        if size > 0:
            formatted_size = format_bytes(size)
            print(f"{index}. {group} - {formatted_size}")
        else:
            print(f"{index}. {group} - File not found")
    
    choice = int(input(f"{Fore.GREEN}Choose a group number: {Style.RESET_ALL}")) - 1
    if choice < 0 or choice >= len(sorted_groups):
        raise ValueError("Invalid group selection")
    return sorted_groups[choice][0]

def simulate_chat(group_name, api_key):
    """
    Simulate a chat negotiation with a ransomware group using AI.
    
    :param group_name: Name of the ransomware group
    :param api_key: API key for the chosen AI service
    """
    os.environ[api_key_env] = api_key
    client = Client(api_key=api_key, **client_kwargs if api_choice == "2" else {})

    behavior = load_behavior(group_name)
    
    system_prompt = f"You are a representative of the {group_name} ransomware group. Here's how you should respond:\n"
    for category, messages in behavior.items():
        system_prompt += f"- {category.capitalize()}: {'; '.join(messages)}.\n"
    system_prompt += """
    - Keep responses concise; only mention payment details if asked or if payment is not confirmed.
    - Focus on negotiating the payment amount rather than repeating payment methods.
    - Do not repeat information given unless directly asked again.
    - Always remind of consequences if negotiation fails but only once per topic.
    - Be professional yet threatening, insisting on payment for decryption and secure data deletion.
    """

    messages = [
        {"role": "system", "content": system_prompt},
    ]

    print(f"{Fore.CYAN}Welcome to the {group_name} negotiation chatroom.{Style.RESET_ALL}")
    print(f"Type 'exit' to leave the chat.")

    while True:
        user_input = input(f"{Fore.GREEN}")
        if user_input.lower() == 'exit':
            print(f"{Fore.RED}{group_name}: Goodbye.{Style.RESET_ALL}")
            break
        
        messages.append({"role": "user", "content": user_input})
        
        context = ""
        if any("payment" in message["content"] for message in messages if message["role"] == "assistant"):
            context = "Focus on negotiating the payment amount rather than repeating payment methods. "
        
        completion = client.chat.completions.create(
            model=default_model,
            messages=messages,
            max_tokens=150,
        )
        response = completion.choices[0].message.content
        
        colored_response = f"{Fore.RED}{response}{Style.RESET_ALL}"
        print(f"{Fore.GREEN}You:{Style.RESET_ALL} {Fore.GREEN}{user_input}{Style.RESET_ALL}")
        print(f"{group_name}: {colored_response}")
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    try:
        group_name = show_behavior_options()
        api_key = input(f"{Fore.GREEN}Enter your API key (hidden input): {Style.RESET_ALL}")
        simulate_chat(group_name, api_key)
    except (ValueError, FileNotFoundError, IndexError) as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")