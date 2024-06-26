import random
from mnemonic import Mnemonic
from mnemonic import Mnemonic as bip39
import platform
import subprocess
import keyboard
import os
import locale
import datetime
from bip32utils import BIP32Key
import hashlib
import binascii
import base58
import bech32
from hashlib import sha256
from bitcoinaddress import segwit_addr
from bitcoinaddress.key.key import Key
from bitcoinaddress.address import Address
from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey
from art import *
import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
from pycoin.symbols.btc import network as BTC
import hmac
from pycoin.encoding.bytes32 import from_bytes_32, to_bytes_32

# Set the locale to your preferred formatting (e.g., en_US.UTF-8)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def disclaimer():
    # Clear terminal
    clear_terminal()

    # Print a centered disclaimer notice
    text1 = "* DISCLAIMER *"
    print_centered_art_text(text1, 6, "Standard")

    # Print disclaimer details
    print_red(f"""

    \n This tool is designed solely for educational purposes. Please refrain from utilizing any keys generated by this tool as actual Bitcoin private keys.
    \n Modifying this code may result in generating incorrect keys and addresses.
    \n Exercise caution to avoid sending bitcoin to addresses for which you lack the corresponding keys.
    \n This tool simplifies the process of converting decimal and binary numbers into corresponding BIP39 mnemonic words then generates a valid mnemonic seed phrase.
    \n It also provides in-depth information about the generated mnemonic seed phrase, including private keys, public keys, and addresses.
    \n It's important to exercise caution when using it on potentially unsecure devices, as it could lead to financial losses.
    \n It is advisable to use a trusted offline device when employing such tools.
    \n If you're new to Bitcoin, we highly recommend using established wallet software and adhering to industry best practices to safeguard your digital assets.
    \n Always maintain backups of your mnemonic seed phrases in secure, offline locations.
    \n Exercise extreme caution when sharing or storing mnemonic seed phrases on digital devices or online platforms.
    """)

def foot_note():
    print(f"\n To confirm binary to decimal conversion, visit: https://www.rapidtables.com/convert/number/binary-to-decimal.html")
    print(" To cross-check decimal to index/word conversion, visit: https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt")
    print(" To confirm your mnemonic seed phrase, visit: https://iancoleman.io/bip39/")
    print(" Note that binary numbers start from 0, while the BIP39 wordlist starts from 1, so remember to add 1 to the decimal result to match the word.")

def main():
    # Clear terminal
    clear_terminal()
    
    # Print title
    text2 = "* ROLL   TO   MNEMONIC *"
    print_centered_art_text(text2, 5, "Standard")

    # Information box
    creator_info = f"Created By          : Sani Fahs"
    twitter_info = f"Twitter             : @SaniExp"
    github_info = f"GitHub              : https://github.com/FahsSani"
    lightning_info = f"Lightning Donations : sani@walletofsatoshi.com"
    max_info_length = max(len(creator_info), len(twitter_info), len(github_info), len(lightning_info))
    box_width = max_info_length + 4
    info_box = " " + "+" + "-" * (box_width - 2) + "+"
    info_box += f"\n | {creator_info.ljust(max_info_length)} |"
    info_box += f"\n | {twitter_info.ljust(max_info_length)} |"
    info_box += f"\n | {github_info.ljust(max_info_length)} |"
    info_box += f"\n | {lightning_info.ljust(max_info_length)} |"
    info_box += "\n +" + "-" * (box_width - 2) + "+"
    print_bright_orange(info_box)

# Functions to print text in color
def print_red(*args):
    text = ' '.join(map(str, args))
    print("\033[91m" + text + "\033[0m")  # '\033[91m' is the ANSI escape code for red color

def print_blue(*args):
    text = ' '.join(map(str, args))
    print("\033[94m" + text + "\033[0m")  # '\033[94m' is the ANSI escape code for blue color

def print_green(*args):
    text = ' '.join(map(str, args))
    print("\033[92m" + text + "\033[0m")  # '\033[92m' is the ANSI escape code for green color

def print_cyan(*args):
    text = ' '.join(map(str, args))
    print("\033[96m" + text + "\033[0m")  # '\033[93m' is the ANSI escape code for orange color

def print_purple(*args):
    text = ' '.join(map(str, args))
    print("\033[95m" + text + "\033[0m")  # '\033[95m' is the ANSI escape code for purple color

def print_bright_orange(*args):
    text = ' '.join(map(str, args))
    print("\033[38;5;208m" + text + "\033[0m")  # '\033[38;5;208m' is the ANSI escape code for bright orange color

# Clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Display a centered art text
def print_centered_art_text(text, convert, fonttype):
    # Default terminal width (you can adjust this value)
    terminal_width = 166  # Adjust to your screen size

    # Calculate the number of spaces needed to center the text
    padding = " " * ((terminal_width - (len(text) * convert)) // 2)

    # Combine padding and the input text
    centered_text = padding + text

    # Print centered text
    tprint(centered_text, font=fonttype)

def maximize_window():
    system = platform.system()
    
    if system == 'Windows':
        # Windows: Send Win + Up Arrow
        keyboard.press_and_release('win+up')
    elif system == 'Darwin':
        # macOS: Send Ctrl + Command + F
        keyboard.press_and_release('ctrl+cmd+f')
    elif system == 'Linux':
        try:
            # Linux: Send Alt + F10 (using wmctrl if available)
            subprocess.check_output(['wmctrl', '--version'])
            subprocess.run(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,maximized_vert,maximized_horz'])
        except subprocess.CalledProcessError:
            # If wmctrl is not available, send Alt + F10 using keyboard
            keyboard.press_and_release('alt+f10')
    else:
        print(f"Unsupported operating system: {system}")
   
# Function to check if a seed phrase is valid
def is_valid_seed(seed_phrase):
    try:
        mnemo = Mnemonic("english")
        return mnemo.check(seed_phrase)
    except ValueError:
        return False
