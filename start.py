from common import *
from diceroll import roll_dice_auto, roll_dice_manual_binary, roll_dice_manual_num
from mccmainnet import generate_mainnet_wallet
from mcctestnet import generate_testnet_wallet

seed_phrase = ""

def disclaimer():
    # Clear terminal
    clear_terminal()

    # Print a centered disclaimer notice
    text1 = "* DISCLAIMER *"
    print_centered_art_text(text1, 6, "Standard")

    # Print disclaimer details
    print_red(f"""
    \n This tool is 100% open-source, and its code can be reviewed from repository (https://github.com/FahsSani/Roll2Mnemonic).
    \n Modifying this code may result in generating incorrect keys and addresses.
    \n Exercise caution to avoid sending bitcoin to addresses for which you lack the corresponding keys.
    \n This tool simplifies the process of converting decimal and binary numbers into corresponding BIP39 mnemonic words then generates a valid mnemonic seed phrase.
    \n It also provides in-depth information about the generated mnemonic seed phrase, including private keys, public keys, and addresses.
    \n It's important to exercise caution when using it on potentially unsecure devices, as it could lead to financial losses.
    \n It is advisable to use a trusted offline device when employing such tools.
    \n If you're new to Bitcoin, we highly recommend using established wallet software and adhering to industry best practices to safeguard your digital assets.
    \n Always maintain backups of your mnemonic seed phrases in secure, offline locations.
    \n Exercise extreme caution when sharing or storing mnemonic seed phrases on digital devices or online platforms.
    \n When using this tool, you recognize the inherent risks involved and that you should verify data from trusted Bitcoin sources before performing real transactions.
    """)

def foot_note():
    print(
        " For binary to decimal conversion verification, visit: https://www.rapidtables.com/convert/number/binary-to-decimal.html")
    print(
        " To cross-check decimal to index/word conversion, visit: https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt")
    print(" For confirming your mnemonic seed phrase, visit: https://iancoleman.io/bip39/")
    print(
        " Please note that binary numbers start from 0, while the BIP39 wordlist starts from 1, so remember to add 1 to the decimal result to match the word.")

def enable_buttons():
    generate_manual_button.config(state="normal")  # Disable the button to prevent any errors
    generate_random_button.config(state="normal")  # Disable the button to prevent any errors
    continue_button.config(state="normal")  # Disable the button to prevent any errors
    result_label.config(text="")

def disable_buttons():
    generate_random_button.config(state="disabled")  # Enable the button after generating
    generate_manual_button.config(state="disabled")  # Enable the button after generating
    continue_button.config(state="disabled")  # Enable the button after generating
    result_label.config(text="The 'Generate' buttons are temporarily disabled to prevent potential errors.\n Functionality will be reactivated once you've completed entering the numbers.")

# Function to generate QR code
def generate_qr_code():
    text = qr_text_entry.get("1.0", "end-1c")  # Get all text from the Text widget
    if text:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((250, 250))  # Resize the image if needed

        # Convert the PIL image to a PhotoImage object
        qr_photo = ImageTk.PhotoImage(qr_img)

        qr_code_label.config(image=qr_photo)
        qr_code_label.image = qr_photo  # Store a reference to the PhotoImage to prevent it from being garbage collected

        # Destroy the QR code image reference and clear the text box 
        qr_code_label.after(60000, lambda: clear_qr_code())

    else:
        qr_code_label.config(image="")
        qr_code_label.image = None

def clear_qr_code():
    qr_code_label.config(image="", text="")
    qr_code_label.image = None
    qr_text_entry.delete("1.0", "end")

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
    box_width = max_info_length + 4  # Adjust the box width based on the max info length
    info_box = " " + "+" + "-" * (box_width - 2) + "+"
    info_box += f"\n | {creator_info.ljust(max_info_length)} |"
    info_box += f"\n | {twitter_info.ljust(max_info_length)} |"
    info_box += f"\n | {github_info.ljust(max_info_length)} |"
    info_box += f"\n | {lightning_info.ljust(max_info_length)} |"
    info_box += "\n +" + "-" * (box_width - 2) + "+"
    print_bright_orange(info_box)

def generate_random_dice_numbers():
    main()
    global seed_phrase  # Use the global seed_phrase variable
    num_words = int(num_words_var.get())
    mnemonic_seed = roll_dice_auto(num_words)
    seed_phrase = ' '.join(mnemonic_seed)
    print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}\n")
    foot_note()
    continue_button.config(state="normal")  # Enable the button after generating
    result_label.config(text="")
    
def generate_manual_dice_numbers():
    main()
    global seed_phrase  # Use the global seed_phrase variable
    num_words = int(num_words_var.get())

    choice = dice_choice_var.get()
    if choice == "Binary":
        disable_buttons()
        mnemonic_seed = roll_dice_manual_binary(num_words)
        enable_buttons()
        seed_phrase = ' '.join(mnemonic_seed)
        print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}\n")
        foot_note()
        result_label.config(text="")
    else:
        disable_buttons()
        mnemonic_seed = roll_dice_manual_num(num_words)
        enable_buttons()
        seed_phrase = ' '.join(mnemonic_seed)
        print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}\n")
        foot_note()
        result_label.config(text="")

def mnemonic_converter():
    global seed_phrase  # Use the global seed_phrase variable
    passphrase = passphrase_entry.get().strip()

    try:
        num_child_keys = int(child_keys_entry.get())
        if 1 <= num_child_keys <= 25:
            network_type = network_type_var.get()  # Get the selected network type
            if network_type == "Mainnet":
                generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase)
            elif network_type == "Testnet":
                generate_testnet_wallet(seed_phrase, num_child_keys, passphrase)
            # subprocess.Popen(['python', 'qrgen.py'])
        else:
            result_label.config(text="Invalid number of child keys. Must be between 1 and 25.")
    except ValueError:
        result_label.config(text="Invalid number of child keys. Must be an integer.")

disclaimer()

# Create the main window
root = tk.Tk()
root.title("Roll2Mnemonic")
root.geometry("455x530")  # Set the width and height of the window

# Create tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand='yes')

# Create tab 1: Dice Roll
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Dice Roll & Mnemonic Seed Phrase")

frame1 = tk.LabelFrame(tab1, text="Mnemonic Seed Phrase Word Count", labelanchor="n")
frame1.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

num_words_var = tk.IntVar()
num_words_var.set(12)

mnemonic_words = [12, 15, 18, 21, 24]

for i, word_count in enumerate(mnemonic_words):
    num_words_button = tk.Radiobutton(frame1, text=str(word_count) + " Words", variable=num_words_var, value=word_count,
                                      command=lambda count=word_count: num_words_var.set(count))
    num_words_button.grid(row=0, column=i + 2, padx=4, pady=0)

frame2 = tk.LabelFrame(tab1, text="Choose Manual Dice Input Type", padx=10, pady=1, labelanchor="n")
frame2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

dice_choice_var = tk.StringVar()
dice_choice_var.set("Binary")
dice_choice_binary = tk.Radiobutton(frame2, text="Binary/Coin Toss", variable=dice_choice_var, value="Binary")
dice_choice_dice = tk.Radiobutton(frame2, text="6-sided Dice Roll", variable=dice_choice_var, value="Dice")
dice_choice_binary.grid(row=0, column=0, padx=5, pady=0)
dice_choice_dice.grid(row=0, column=1, padx=5, pady=0)

generate_random_button = tk.Button(tab1, text="Generate Random Dice Numbers", command=generate_random_dice_numbers)
generate_manual_button = tk.Button(tab1, text="Generate Manual Dice Numbers", command=generate_manual_dice_numbers)
generate_random_button.grid(row=2, column=0, padx=22, pady=10)
generate_manual_button.grid(row=2, column=1, padx=22, pady=10)

frame3 = tk.LabelFrame(tab1, text="Passphrase (optional)", padx=10, pady=10, labelanchor="n")
frame3.grid(row=4, column=0, columnspan=10, padx=10, pady=10)

passphrase_entry = tk.Entry(frame3)
passphrase_entry.grid(row=0, column=1)

# Set a larger width for the passphrase_entry
passphrase_entry.config(width=40)  # You can adjust the width as needed

frame4 = tk.LabelFrame(tab1, text="Number of Child Keys (1-25)", padx=10, pady=10, labelanchor="n")
frame4.grid(row=5, column=0, columnspan=10, padx=10, pady=10)

child_keys_entry = tk.Entry(frame4, justify="center")
child_keys_entry.insert(0, "5")  # Default value
child_keys_entry.grid(row=0, column=1)
child_keys_entry.config(width=25)  # You can adjust the width as needed

frame5 = tk.LabelFrame(tab1, text="Choose Network Type", padx=10, pady=0, labelanchor="n")
frame5.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

network_type_var = tk.StringVar()
network_type_var.set("Mainnet")
network_type_mainnet = tk.Radiobutton(frame5, text="Mainnet", variable=network_type_var, value="Mainnet")
network_type_testnet = tk.Radiobutton(frame5, text="Testnet", variable=network_type_var, value="Testnet")
network_type_mainnet.grid(row=0, column=0, padx=5, pady=1)
network_type_testnet.grid(row=0, column=1, padx=5, pady=1)

continue_button = tk.Button(tab1, text="Mnemonic Code Converter", command=mnemonic_converter)
continue_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

result_label = tk.Label(tab1, text="", padx=10, pady=20)
result_label.grid(row=8, column=0, columnspan=2)

# Create tab 3: QR Code Generator
tab3 = tk.Frame(notebook)
notebook.add(tab3, text="QR Code Generator")

# QR Code Generator UI elements
qr_label = tk.Label(tab3, text="Enter the intended text then click Generate QR Code:")
qr_label.grid(row=0, column=0, padx=10, pady=7)

qr_text_entry = tk.Text(tab3, height=5, width=45) 
qr_text_entry.grid(row=1, column=0, padx=10, pady=1)

qr_warning_label = tk.Label(tab3, text=f"Make sure to copy the intended text correctly."
                            "\nMake sure not to add spaces after your text, this will affect the resulting QR Code."
                            "\nMistakes may lead to serious losses."
                            "\nFor added privacy, QR code and text will be cleared after 1 minute of generation.", fg="red")
qr_warning_label.grid(row=2, column=0, padx=10, pady=0)


generate_qr_button = tk.Button(tab3, text="Generate QR Code", command=generate_qr_code)
generate_qr_button.grid(row=6, column=0, padx=10, pady=10)

# Display the QR code here
qr_code_label = tk.Label(tab3)
qr_code_label.grid(row=7, column=0)

# Start the GUI event loop
continue_button.config(state="disabled")
result_label.config(text=f"The 'Mnemonic Code Converter' button is temporarily disabled. \nGenerate dice number to enable.")

root.mainloop()
