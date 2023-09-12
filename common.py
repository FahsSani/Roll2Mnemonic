import random
from mnemonic import Mnemonic
import platform
import subprocess
import os
import datetime
from mnemonic import Mnemonic
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
from bitcoinutils.keys import P2pkhAddress, PrivateKey
from art import *

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

def print_Cyan(*args):
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
def print_centered_art_text(text, convert):
    # Default terminal width (you can adjust this value)
    terminal_width = 166 # Adjust to your screen size

    # Calculate the number of spaces needed to center the text
    padding = " " * ((terminal_width - (len(text)*(convert))) // 2)

    # Combine padding and the input text
    centered_text = padding + text

    # Print centered text
    tprint(centered_text, font="standard")
