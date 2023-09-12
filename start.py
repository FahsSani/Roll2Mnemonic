from common import *
from diceroll import roll_dice_auto, roll_dice_manual_binary,  roll_dice_manual_num, generate_seed_phrase 
from mcc import generate_wallet

# Clear terminal
clear_terminal()

# Print a centered disclaimer notice
text1 = "* DISCLAIMER *"
print_centered_art_text(text1,6)

# Print disclaimer details
print_red(f"""
\n This tool is 100% open-source, and its code can be reviewd from repository (https://github.com/FahsSani/Roll2Mnemonic)
\n This tool simplifies the process of converting decimal and binary numbers into corresponding BIP39 mnemonic words then generates a valid mnemonic seed phrase.
\n It also provides in-depth information about the generated mnemonic seed phrase, including private keys, public keys, and addresses.
\n It's important to exercise caution when using it on potentially unsecure devices, as it could lead to financial losses.
\n It is advisable to use a trusted offline device when employing such tools.
\n If you're new to cryptocurrency, we highly recommend using established wallet software and adhering to industry best practices to safeguard your digital assets.
\n Always maintain backups of your mnemonic seed phrases in secure, offline locations.
\n Exercise extreme caution when sharing or storing mnemonic seed phrases on digital devices or online platforms.
\n When opting to utilize this tool, you recognize the inherent risks involved and the importance of verifying the data generated using third-party sources
 before proceeding with real-life transactions.
""")


input(" Press any key to continue...")

restart_flag = True
while restart_flag:

    # Clear terminal
    clear_terminal()

    # Print title
    text2 = "* ROLL   TO   MNEMONIC *"
    print_centered_art_text(text2,5)

    # Information box
    creator_info = f"Created By          : Sani Fahs"
    twitter_info = f"Twitter             : @SaniExp"
    github_info = f"GitHub              : https://github.com/FahsSani"
    lightning_info = f"Lightning Donations : sani@walletofsatoshi.com"
    max_info_length = max( len(creator_info), len(twitter_info),len(github_info), len(lightning_info))
    box_width = max_info_length + 4  # Adjust the box width based on the max info length
    info_box = " " + "+" + "-" * (box_width - 2) + "+"
    info_box += f"\n | {creator_info.ljust(max_info_length)} |"
    info_box += f"\n | {twitter_info.ljust(max_info_length)} |"
    info_box += f"\n | {github_info.ljust(max_info_length)} |"
    info_box += f"\n | {lightning_info.ljust(max_info_length)} |"
    info_box += "\n +" + "-" * (box_width - 2) + "+"
    print_bright_orange(info_box)

    while True:
        choice = input("\n Enter 'r' to generate random dice numbers automatically or 'm' to fill in manually: ").lower()
        if choice == "r":
            while True:
                num_words = int(input(" Enter the number of words for the mnemonic seed phrase (12, 15, 18, 21, or 24): "))
                if num_words in [12, 15, 18, 21, 24]:
                    mnemonic_seed = roll_dice_auto(num_words)
                    seed_phrase = ' '.join(mnemonic_seed)
                    print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}\n")
                    break
                else:
                    print(" Invalid input. Please choose from the given options.")
            break
        elif choice == "m":
            while True:
                num_words = int(input(" Enter the number of words for the mnemonic seed phrase (12, 15, 18, 21, or 24): "))
                if num_words in [12, 15, 18, 21, 24]:
                    inner_loop_flag = True
                    while inner_loop_flag:
                        choice = input(" Enter 'd' to input the 6-sided dice roll numbers or 'b' to input binary numbers: ")
                        if choice == "b":
                            mnemonic_seed = roll_dice_manual_binary(num_words)
                            seed_phrase = ' '.join(mnemonic_seed)
                            print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}\n")
                            inner_loop_flag = False
                        elif choice == "d":
                            mnemonic_seed = roll_dice_manual_num(num_words)
                            seed_phrase = ' '.join(mnemonic_seed)
                            print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}\n")
                            inner_loop_flag = False
                        else:
                            print(" Invalid input. Please choose from the given options.")
                    break
                else:
                    print(" Invalid input. Please choose from the given options.")
            break
        else:
            print(" Invalid input. Please choose from the given options.")
    while True:
        choice = input(" Enter 'c' to continue to Mnenmonic Code Converter or 'r' to roll the dice again: ").lower()
        if choice == "c":
            wallets = generate_wallet(seed_phrase)
            choice = input(" Enter any key to roll the dice again").lower()
            break
        elif choice == "r":
            restart_flag = True
            break
        else:
            print(" Invalid input. Please choose 'c' to continue to Mnenmonic Code Converter or 'r' to roll the dice again.")
