import os
import json
import platform
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init()

# Conditional imports based on API choice
api_choice = input(f"{Fore.YELLOW}Choose API (1 for OpenAI, 2 for xAI Grok): {Style.RESET_ALL}")
if api_choice == "1":
    from openai import OpenAI as Client
    api_key_env = "OPENAI_API_KEY"
    default_model = "gpt-4o"
    client_kwargs = {}
elif api_choice == "2":
    from openai import OpenAI as Client
    api_key_env = "XAI_API_KEY"
    default_model = "grok-beta"
    client_kwargs = {"base_url": "https://api.x.ai/v1"}
else:
    raise ValueError("Invalid API choice")

def load_behaviour(group_name):
    """
    Load behaviour patterns from a text file for a specific ransomware group.
    """
    behaviour_path = os.path.join(os.getcwd(), 'behaviour')
    behaviour_file = os.path.join(behaviour_path, f"{group_name}_behaviour.txt")

    if not os.path.exists(behaviour_file):
        raise FileNotFoundError(f"Behaviour file for {group_name} not found in {behaviour_path}.")

    behaviour = {}
    current_category = None

    with open(behaviour_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.endswith(':'):
                current_category = line[:-1].lower()
                behaviour[current_category] = []
            elif line and current_category:
                behaviour[current_category].append(line[2:])

    return behaviour

def format_bytes(size):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if size < 1024:
            return f"{size:.2f}{unit}B"
        size /= 1024

def show_behaviour_options():
    """
    Display available ransomware groups sorted by behaviour file size.
    """
    base_path = os.path.join(os.getcwd(), 'behaviour')
    groups = []

    # Search for files ending with '_behaviour.txt'
    for filename in os.listdir(base_path):
        if filename.endswith('_behaviour.txt'):
            group_name = filename.replace('_behaviour.txt', '')
            file_path = os.path.join(base_path, filename)
            size = os.path.getsize(file_path)
            groups.append((group_name, size))

    if not groups:
        raise FileNotFoundError("No behaviour files found in the 'behaviour' directory.")

    sorted_groups = sorted(groups, key=lambda x: x[1], reverse=True)

    print(f"{Fore.YELLOW}Available Ransomware Groups:{Style.RESET_ALL}")
    for index, (group, size) in enumerate(sorted_groups, 1):
        formatted_size = format_bytes(size)
        print(f"{index}. {group} - {formatted_size}")

    choice = int(input(f"{Fore.GREEN}Choose a group number: {Style.RESET_ALL}")) - 1
    if choice < 0 or choice >= len(sorted_groups):
        raise ValueError("Invalid group selection")

    return sorted_groups[choice][0]

def clear_screen():
# Determine the operating system and clear the screen accordingly
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def simulate_chat(group_name, api_key):
    """
    Simulate a chat negotiation with a ransomware group using AI.
    """
    os.environ[api_key_env] = api_key
    client = Client(api_key=api_key, **client_kwargs)

    behaviour = load_behaviour(group_name)

    system_prompt = f"You are a representative of the {group_name} ransomware group. Here's how you should respond:\n"
    for category, messages in behaviour.items():
        system_prompt += f"- {category.capitalize()}: {'; '.join(messages)}.\n"

    system_prompt += """
    - Keep responses concise; only mention payment details if asked or if payment is not confirmed.
    - Focus on negotiating the payment amount rather than repeating payment methods.
    - Do not repeat information given unless directly asked again.
    - Always remind of consequences if negotiation fails but only once per topic.
    - Be professional yet threatening, insisting on payment for decryption and secure data deletion.
    """

    messages = [{"role": "system", "content": system_prompt}]

    print(f"{Fore.CYAN}Welcome to the {group_name} negotiation chatroom.{Style.RESET_ALL}")
    print(f"Type 'exit' to leave the chat.")

    while True:
        user_input = input(f"{Fore.GREEN}")
        if user_input.lower() == 'exit':
            print(f"{Fore.RED}{group_name}: Goodbye.{Style.RESET_ALL}")
            break

        messages.append({"role": "user", "content": user_input})

        completion = client.chat.completions.create(
            model=default_model,
            messages=messages,
            max_tokens=150,
        )

        response = completion.choices[0].message.content

        print(f"{Fore.GREEN}You:{Style.RESET_ALL} {Fore.GREEN}{user_input}{Style.RESET_ALL}")
        print(f"{group_name}: {Fore.RED}{response}{Style.RESET_ALL}")
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    try:
        group_name = show_behaviour_options()
        api_key = input(f"{Fore.GREEN}Enter your API key (hidden input): {Style.RESET_ALL}")
        # Clear the screen after API key input
        clear_screen()
        simulate_chat(group_name, api_key)
    except (ValueError, FileNotFoundError, IndexError) as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
