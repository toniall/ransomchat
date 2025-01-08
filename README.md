# Ransomware Chat Simulation

This repository contains a Python script for simulating chat negotiations with ransomware groups based on real-world behavior patterns.

**Author:** Antonio Brandao  
**Data Source:** Based on real ransomware chat logs from [Casualtek/Ransomchats](https://github.com/Casualtek/Ransomchats/tree/main).  
**Special Thanks:** Valéry Marchive for insights and contributions.

## Features

- **Behavior Analysis:** Reads behavior patterns from text files extracted from actual ransomware negotiations, allowing for realistic simulation of ransomware group interactions.
- **API Flexibility:** Supports integration with either OpenAI or xAI Grok APIs, giving flexibility in AI model usage for responses.
- **User Interface:** Offers a command-line interface with color-coded outputs to differentiate between user and ransomware responses.
- **File Management:** Includes a script to update terminology from 'behavior' to 'behaviour' for consistency with British English or specific project needs.

## Usage

- Choose between OpenAI or xAI Grok for AI-powered responses in simulated ransomware negotiations.
- Select from a list of ransomware groups, sorted by the size of their behavior data, to simulate interactions.
- Engage in a simulated negotiation where the AI responds based on predefined behavior patterns.

## Requirements

- Python 3.x
- `openai` library for OpenAI API integration
- `colorama` for colored terminal text on Windows
- An API key for either OpenAI or xAI Grok services

## Installation

1. **Clone the repository**:
  ```bash
   git clone https://github.com/toniall/ransomchat.git
   cd ransomchat
  ```
  
2. **Set up and activate a virtual environment**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # For Linux/macOS
  ```

3. **Install dependencies**:
 ```bash 
  pip install -r requirements.txt
  ```

4. **Run the Python script**:
  ```bash
  python3 RamsonChat.py
  ```
5. **Run the Python GUI for the Chat**:
  ```bash
  python3 RamsonChatPyQt.py
  ```

## Note

This tool is for **educational, research, or demonstration purposes only**. It should not be used for any malicious activities or to engage with actual ransomware groups.

![image](https://github.com/user-attachments/assets/6fa23a4f-14fd-4333-b18f-dcc6e053bc62)


![image](https://github.com/user-attachments/assets/e1e147ad-b6eb-4763-a5bb-6fc51002ec07)

