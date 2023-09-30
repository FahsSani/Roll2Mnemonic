import random
from mnemonic import Mnemonic
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
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk


# Set the locale to your preferred formatting (e.g., en_US.UTF-8)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

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
    terminal_width = 166 # Adjust to your screen size

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
