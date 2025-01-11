import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, 
                             QPushButton, QLabel, QStatusBar, QInputDialog, QMessageBox, QFileDialog)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
import os
import json
from openai import OpenAI as Client

class ChatApp(QWidget):
    def __init__(self, group_name, api_key, model, behaviour_path):
        super().__init__()
        
        self.setWindowTitle(f"{group_name} Negotiation Chatroom")
        self.setGeometry(100, 100, 600, 500)  # Increased height for more UI elements
        
        # Custom palette for dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        
        # Top section for group profile
        profile_layout = QHBoxLayout()
        self.profile_image = QLabel()
        pixmap = QPixmap('path/to/ransomware_icon.png')  # Replace with path to an image
        self.profile_image.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_layout.addWidget(self.profile_image)
        profile_info = QLabel(f"<h2>{group_name}</h2><p>Known for: Hacking, Data Encryption</p>")
        profile_info.setStyleSheet("color: white;")
        profile_layout.addWidget(profile_info)
        main_layout.addLayout(profile_layout)

        # Chat area
        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont('Arial', 12))
        self.chat_area.setStyleSheet("background-color: #353535; color: white;")
        main_layout.addWidget(self.chat_area)

        # Input area
        input_layout = QHBoxLayout()
        self.message_entry = QLineEdit(self)
        self.message_entry.setFont(QFont('Arial', 12))
        self.message_entry.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.message_entry.setPlaceholderText("Type your message here...")
        self.message_entry.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(QFont('Arial', 12))
        self.send_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.message_entry)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("background-color: #353535; color: white;")
        self.status_bar.showMessage("Negotiation in progress...", 0)  # Permanent message
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)

        # Initialize chat
        self.group_name = group_name
        self.api_key = api_key
        self.model = model
        self.behaviour_path = behaviour_path  
        self.messages = [{"role": "system", "content": self.get_system_prompt(group_name)}]
        self.initialize_chat()

    def initialize_chat(self):
        self.chat_area.append(f"<b><font color='red'>Welcome to the {self.group_name} negotiation chatroom.</font></b>")
        self.chat_area.append("Type 'exit' to leave the chat.")

    def get_system_prompt(self, group_name):
        behaviour = self.load_behaviour(group_name)
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
        return system_prompt

    def load_behaviour(self, group_name):
        behaviour_file = os.path.join(self.behaviour_path, f"{group_name}_behaviour.txt")
        if not os.path.exists(behaviour_file):
            raise FileNotFoundError(f"Behaviour file for {group_name} not found in {self.behaviour_path}.")
        
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

    def send_message(self):
        message = self.message_entry.text()
        self.handle_message(message)

    def handle_message(self, message):
        if message.lower() == 'exit':
            QApplication.quit()
        else:
            # Victim's (user's) message in blue
            self.chat_area.append(f"<b><font color='blue'>You:</font> {message}</b>")
            self.messages.append({"role": "user", "content": message})
            
            try:
                client = Client(api_key=self.api_key, base_url="https://api.x.ai/v1" if self.model == "grok-beta" else None)
                completion = client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    max_tokens=150,
                )
                response = completion.choices[0].message.content
                # Ransomware group's response in red
                self.chat_area.append(f"<b><font color='red'>{self.group_name}:</font> {response}</b>")
                self.messages.append({"role": "assistant", "content": response})
                self.status_bar.showMessage("Response received", 5000)  # Message disappears after 5 seconds
            except Exception as e:
                self.chat_area.append(f"<b><font color='red'>Error:</font> {str(e)}</b>")
                self.status_bar.showMessage("An error occurred", 5000)
        
        self.message_entry.clear()
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())

def select_api():
    items = ["OpenAI", "xAI Grok"]
    item, ok = QInputDialog.getItem(None, "Select API", "Choose your AI API:", items, 0, False)
    if ok and item:
        if item == "OpenAI":
            return "1", "OPENAI_API_KEY", "gpt-4o"
        elif item == "xAI Grok":
            return "2", "XAI_API_KEY", "grok-beta"
    raise ValueError("No API selected.")

def show_behaviour_options():
    base_path = os.path.join(os.getcwd(), 'behaviour')
    groups = []
    
    for file_name in os.listdir(base_path):
        if file_name.endswith('_behaviour.txt'):
            group = file_name.replace('_behaviour.txt', '')
            groups.append(group)
    
    if not groups:
        raise FileNotFoundError("No behaviour files found in the behaviour directory.")
    
    item, ok = QInputDialog.getItem(None, "Select Ransomware Group", "Choose a group:", groups, 0, False)
    if ok and item:
        return item
    raise ValueError("No group selected.")

def select_behaviour_folder():
    folder = QFileDialog.getExistingDirectory(None, "Select Behaviour Folder", os.getcwd(), QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
    if not folder:
        raise ValueError("No folder selected.")
    print(f"Selected folder: {folder}")  # For debugging
    return folder

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        api_choice, api_key_env, model = select_api()
        api_key, ok = QInputDialog.getText(None, "API Key", f"Enter your API key for {api_choice}:")
        if not ok or not api_key:
            raise ValueError("API key not provided.")
        
        behaviour_path = select_behaviour_folder()
        print(f"Behaviour path: {behaviour_path}")  # For debugging
        group_name = show_behaviour_options()
        ex = ChatApp(group_name, api_key, model, behaviour_path)
        ex.show()
        sys.exit(app.exec_())
    except (ValueError, FileNotFoundError) as e:
        QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")