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
    print(f"\n To confirm binary to decimal conversion, visit: https://www.rapidtables.com/convert/number/binary-to-decimal.html")
    print(" To cross-check decimal to index/word conversion, visit: https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt")
    print(" To confirm your mnemonic seed phrase, visit: https://iancoleman.io/bip39/")
    print(" Please note that binary numbers start from 0, while the BIP39 wordlist starts from 1, so remember to add 1 to the decimal result to match the word.")

def enable_buttons():
    start_dice_button.config(state="normal")
    continue_button.config(state="normal")
    continue_button2.config(state="normal")
    result_label.config(text="")
    result_label2.config(text="")

def disable_buttons():
    start_dice_button.config(state="disabled")
    continue_button.config(state="disabled")
    continue_button2.config(state="disabled")
    result_label.config(text="Buttons are temporarily disabled to prevent potential errors.\n Functionality will be reactivated once you've completed Dice Roll.")
    result_label2.config(text="Buttons are temporarily disabled to prevent potential errors.\n Functionality will be reactivated once you've completed Dice Roll.")

def on_own_dice_select():
    dice_choice_binary.config(state="normal")
    dice_choice_dice.config(state="normal")

def on_entropy_dice_select():
    dice_choice_binary.config(state="disabled")
    dice_choice_dice.config(state="disabled")

def on_own_mnemonic_select():
    frame12.grid_remove()
    frame13.grid()
    frame14.grid_remove()
    result_label2.config(text="")

def on_entropy_mnemonic_select():
    frame12.grid()
    frame13.grid_remove()
    frame14.grid()
    result_label2.config(text="")

# Function to generate QR code
def generate_qr_code():
    text = qr_text_entry.get("1.0", "end-1c")  # Get all text from the Text widget
    if text:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
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

def format_with_thousand_separator(value):
    return locale.format_string("%d", value, grouping=True)

def on_entry_change(event):
    try:
        value = int(entropy_entry2.get().replace(',', ''))
        formatted_value = format_with_thousand_separator(value)
        entropy_entry2.delete(0, tk.END)
        entropy_entry2.insert(0, formatted_value)
    except ValueError:
        pass

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

def start_dice():
    global seed_phrase
    main()
    dice = dice_type.get()
    num_words = int(num_words_var.get())

    if dice == "Entropy":
        mnemonic_seed = roll_dice_auto(num_words)
        continue_button.config(state="normal")
        result_label.config(text="")

    elif dice == "Own":
        choice = dice_choice_var.get()
        if choice == "Binary":
            disable_buttons()
            mnemonic_seed = roll_dice_manual_binary(num_words)
            enable_buttons()
        else:
            disable_buttons()
            mnemonic_seed = roll_dice_manual_num(num_words)
            enable_buttons()

    seed_phrase = ' '.join(mnemonic_seed)
    print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}")
    foot_note()
    result_label.config(text="Dice Roll Completed Successfully.")

def mnemonic_converter():
    global seed_phrase
    passphrase = passphrase_entry.get().strip()
    list_type = add_list_type_var.get()
    try:
        num_child_keys = int(child_keys_entry.get())
        if 1 <= num_child_keys <= 25:
            network_type = network_type_var.get()
            result_label.config(text="Mnemonic Seed Phrase Generated Successfully.")
            if network_type == "Mainnet":
                generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
            elif network_type == "Testnet":
                generate_testnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
        else:
            result_label.config(text="Invalid number of child keys. Must be between 1 and 25.")
    except ValueError:
        result_label.config(text="Invalid number of child keys. Must be an integer.")

def mnemonic_converter2():
    main()
    passphrase = passphrase_entry2.get().strip()
    num_words = int(num_words_var2.get())
    mnemonic_type2_value = mnemonic_type2.get()
    list_type = add_list_type2_var.get()

    if mnemonic_type2_value == "Entropy":
        try:
            num_child_keys = int(child_keys_entry2.get())
            if 1 <= num_child_keys <= 25:
                try:
                    entropy_generation = int(entropy_entry2.get().replace(',', ''))
                    if 1000 <= entropy_generation <= 10000000:
                        entropy_lengths = {"12": 128, "15": 160, "18": 192, "21": 224, "24": 256}
                        entropy_bytes = entropy_lengths.get(str(num_words))

                        random_data_list = [os.urandom(entropy_bytes // 8) for _ in range(entropy_generation)]
                        print(f"\n Generating a list of {entropy_generation:,} random Hex entropies.")
                        entropy_display = display_entropy2.get()
                        if entropy_display == "Display":
                            for i, entropy in enumerate(random_data_list):
                                print(f"  Entropy {i + 1:,}: {entropy.hex()}")
                        while True:
                            chosen_entropy = random.choice(random_data_list)
                            print(f"\n Choosing a random Hex entropy from the list.")
                            if entropy_display == "Display":
                                print(f"  Entropy {random_data_list.index(chosen_entropy) + 1:,}: {chosen_entropy.hex()} has been chosen.\n")
                            mnemonic = Mnemonic("english")
                            seed_phrase = mnemonic.to_mnemonic(chosen_entropy)

                            if is_valid_seed(seed_phrase):
                                result_label2.config(text="Mnemonic Seed Phrase Generated Successfully.")
                                network_type = network_type2_var.get()
                                if network_type == "Mainnet":
                                    generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                                elif network_type == "Testnet":
                                    generate_testnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                                return
                    else:
                        result_label2.config(text="Invalid number of entropies, must be between 10,000 and 10,000,000.")
                except ValueError:
                    result_label2.config(text="Invalid number of entropies, must be an integer.")
            else:
                result_label2.config(text="Invalid number of child keys, must be between 1 and 25.")
        except ValueError:
            result_label2.config(text="Invalid number of child keys, must be an integer.")

    else:
        seed_phrase = frame13_entry.get("1.0", "end-1c")
        try:
            num_child_keys = int(child_keys_entry2.get())
            if 1 <= num_child_keys <= 25:
                try:
                    if is_valid_seed(seed_phrase):
                        result_label2.config(text="Mnemonic Seed Phrase Generated Successfully.")
                        network_type = network_type2_var.get()                       
                        if network_type == "Mainnet":
                            generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                        elif network_type == "Testnet":
                            generate_testnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                    else:
                        result_label2.config(text="Invalid Mnemonic Seed Phrase, make sure that the seed phrase is valid"
                                                  "\nand that there are no spaces before or after the seed phrase.")
                except Exception as e:
                    result_label2.config(text=f"An error occurred while generating the wallet: {str(e)}")
            else:
                result_label2.config(text="Invalid number of child keys, must be between 1 and 25.")
        except ValueError:
            result_label2.config(text="Invalid number of child keys, must be an integer.")

maximize_window()
disclaimer()

# Create the main window
root = tk.Tk()
root.title("Roll2Mnemonic")
root.geometry("450x480")

# Create tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand='yes')

# Create tab 1: Dice Roll
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Dice Roll To Mnemonic")

frame0 = tk.LabelFrame(tab1, text="Dice Roll Type", labelanchor="n")
frame0.grid(row=0, column=0, columnspan=12, padx=10, pady=5)
dice_type = tk.StringVar()
dice_type.set("Entropy")
dice_type_entropy = tk.Radiobutton(frame0, text="Generate From Entropy", variable=dice_type, value="Entropy")
dice_type_own = tk.Radiobutton(frame0, text="Enter Your Own Numbers", variable=dice_type, value="Own")
dice_type_entropy.grid(row=0, column=0, padx=10, pady=0)
dice_type_own.grid(row=0, column=1, padx=10, pady=0)
dice_type_own.bind("<Button-1>", lambda event: on_own_dice_select())
dice_type_entropy.bind("<Button-1>", lambda event: on_entropy_dice_select())

frame1 = tk.LabelFrame(tab1, text="Mnemonic Seed Phrase Word Count", labelanchor="n")
frame1.grid(row=1, column=0, columnspan=12, padx=10, pady=5)

num_words_var = tk.IntVar()
num_words_var.set(12)
mnemonic_words = [12, 15, 18, 21, 24]
for i, word_count in enumerate(mnemonic_words):
    num_words_button = tk.Radiobutton(frame1, text=str(word_count) + " Words", variable=num_words_var, value=word_count,
                                      command=lambda count=word_count: num_words_var.set(count))
    num_words_button.grid(row=0, column=i + 2, padx=4, pady=0)

frame2 = tk.LabelFrame(tab1, text="Choose Input Type", padx=10, pady=0, labelanchor="n")
frame2.grid(row=2, column=0, columnspan=12, padx=10, pady=5)
dice_choice_var = tk.StringVar()
dice_choice_var.set("Binary")
dice_choice_binary = tk.Radiobutton(frame2, text="Binary/Coin Toss", variable=dice_choice_var, value="Binary")
dice_choice_dice = tk.Radiobutton(frame2, text="6-sided Dice Roll", variable=dice_choice_var, value="Dice")
dice_choice_binary.grid(row=0, column=0, padx=4, pady=0)
dice_choice_dice.grid(row=0, column=1, padx=4, pady=0)

start_dice_button = tk.Button(tab1, text="Start Dice Roll", command=start_dice)
start_dice_button.grid(row=3, column=0, columnspan=12, padx=10, pady=5)

frame3 = tk.LabelFrame(tab1, text="Passphrase (optional)", padx=10, pady=5, labelanchor="n")
frame3.grid(row=4, column=0, columnspan=1, padx=26, pady=0)
passphrase_entry = tk.Entry(frame3, justify="center")
passphrase_entry.grid(row=0, column=1)
passphrase_entry.config(width=25)

frame4 = tk.LabelFrame(tab1, text="Number Of Child Keys (1-25)", padx=10, pady=5, labelanchor="n")
frame4.grid(row=4, column=1, columnspan=1, padx=10, pady=10)
child_keys_entry = tk.Entry(frame4, justify="center")
child_keys_entry.insert(0, "5")
child_keys_entry.grid(row=0, column=1)
child_keys_entry.config(width=25)

frame5 = tk.LabelFrame(tab1, text="Addresses Details", padx=10, pady=0, labelanchor="n")
frame5.grid(row=5, column=0, columnspan=12, padx=10, pady=6)
add_list_type_var = tk.StringVar()
add_list_type_var.set("AddMain")
add_list_type_addmain = tk.Radiobutton(frame5, text="Addresses & Private Keys", variable=add_list_type_var, value="AddMain")
add_list_type_addfull = tk.Radiobutton(frame5, text="Addresses & Public/Private Keys", variable=add_list_type_var, value="AddFull")
add_list_type_addmain.grid(row=0, column=0, padx=5, pady=0)
add_list_type_addfull.grid(row=0, column=1, padx=5, pady=0)

frame6 = tk.LabelFrame(tab1, text="Choose Network Type", padx=10, pady=0, labelanchor="n")
frame6.grid(row=6, column=0, columnspan=12, padx=10, pady=0)
network_type_var = tk.StringVar()
network_type_var.set("Mainnet")
network_type_mainnet = tk.Radiobutton(frame6, text="Mainnet", variable=network_type_var, value="Mainnet")
network_type_testnet = tk.Radiobutton(frame6, text="Testnet", variable=network_type_var, value="Testnet")
network_type_mainnet.grid(row=0, column=0, padx=5, pady=0)
network_type_testnet.grid(row=0, column=1, padx=5, pady=0)

continue_button = tk.Button(tab1, text="Generate Keys & Addresses", command=mnemonic_converter)
continue_button.grid(row=7, column=0, columnspan=12, padx=10, pady=10)

result_label = tk.Label(tab1, text="", padx=10, pady=5, fg="red")
result_label.grid(row=8, column=0, columnspan=12)

# Create tab 2: Mnemonic Code Converter
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="Seed To Mnemonic")

frame11 = tk.LabelFrame(tab2, text="Mnemonic Seed Phrase", labelanchor="n")
frame11.grid(row=0, column=0, columnspan=12, padx=10, pady=5)
mnemonic_type2 = tk.StringVar()
mnemonic_type2.set("Entropy")
mnemonic_type2_entropy = tk.Radiobutton(frame11, text="Generate From Entropy", variable=mnemonic_type2, value="Entropy")
mnemonic_type2_own = tk.Radiobutton(frame11, text="Enter Your Own Seed", variable=mnemonic_type2, value="Own")
mnemonic_type2_entropy.grid(row=0, column=0, padx=10, pady=0)
mnemonic_type2_own.grid(row=0, column=1, padx=10, pady=0)
mnemonic_type2_own.bind("<Button-1>", lambda event: on_own_mnemonic_select())
mnemonic_type2_entropy.bind("<Button-1>", lambda event: on_entropy_mnemonic_select())

frame12 = tk.LabelFrame(tab2, text="Mnemonic Seed Phrase Word Count", labelanchor="n")
frame12.grid(row=2, column=0, columnspan=12, padx=10, pady=5)
num_words_var2 = tk.IntVar()
num_words_var2.set(12)
mnemonic_words = [12, 15, 18, 21, 24]
for i, word_count in enumerate(mnemonic_words):
    num_words_button = tk.Radiobutton(frame12, text=str(word_count) + " Words", variable=num_words_var2, value=word_count,
                                      command=lambda count=word_count: num_words_var2.set(count))
    num_words_button.grid(row=0, column=i + 2, padx=4, pady=0)

frame13 = tk.LabelFrame(tab2, text="Enter Your Own Mnemonic Seed Phrase (12, 15, 18, 21, 24 Words Only)", padx=10, pady=5, labelanchor="n")
frame13.grid(row=2, column=0, columnspan=12, padx=11, pady=5)
frame13_entry = tk.Text(frame13, height=7, width=54, font=("Helvetica", 9))
frame13_entry.grid(row=0, column=0, padx=10, pady=0)
frame13_entry.insert("1.0", "Word1 Word2 Word3 .....")

frame14 = tk.LabelFrame(tab2, text="Enter Number Of Hex Entropies To Generate (1,000 - 10,000,000)", padx=10, pady=6,labelanchor="n")
frame14.grid(row=3, column=0, columnspan=12, padx=10, pady=6)

entropy_entry2 = tk.Entry(frame14, justify="center")
entropy_entry2.insert(0, "1,000,000")
entropy_entry2.grid(row=0, column=0, columnspan=6, padx=5, pady=0)
entropy_entry2.config(width=30)
entropy_entry2.bind("<FocusOut>", on_entry_change)

display_entropy2 = tk.StringVar()
display_entropy2.set("Hide")
display_entropy2_yes = tk.Radiobutton(frame14, text="Display Entropy", variable=display_entropy2, value="Display")
display_entropy2_no = tk.Radiobutton(frame14, text="Hide Entropy", variable=display_entropy2, value="Hide")
display_entropy2_yes.grid(row=0, column=10)
display_entropy2_no.grid(row=0, column=11)

label_below_radios = tk.Label(frame14, text="Displaying a long list of entropies may take a significant amount of time", fg="red")
label_below_radios.grid(row=1, column=0, columnspan=12)

frame15 = tk.LabelFrame(tab2, text="Passphrase (optional)", padx=10, pady=5, labelanchor="n")
frame15.grid(row=5, column=0, columnspan=6, padx=10, pady=5)
passphrase_entry2 = tk.Entry(frame15, justify="center")
passphrase_entry2.grid(row=0, column=1)
passphrase_entry2.config(width=25)

frame16 = tk.LabelFrame(tab2, text="Number Of Child Keys (1-25)", padx=10, pady=5, labelanchor="n")
frame16.grid(row=5, column=6, columnspan=6, padx=10, pady=5)
child_keys_entry2 = tk.Entry(frame16, justify="center")
child_keys_entry2.insert(0, "5")
child_keys_entry2.grid(row=0, column=1)
child_keys_entry2.config(width=25)

frame17 = tk.LabelFrame(tab2, text="Addresses Details", padx=10, pady=0, labelanchor="n")
frame17.grid(row=7, column=0, columnspan=12, padx=10, pady=6)
add_list_type2_var = tk.StringVar()
add_list_type2_var.set("AddMain")
add_list_type2_addmain = tk.Radiobutton(frame17, text="Addresses & Private Keys", variable=add_list_type2_var, value="AddMain")
add_list_type2_addfull = tk.Radiobutton(frame17, text="Addresses & Public/Private Keys", variable=add_list_type2_var, value="AddFull")
add_list_type2_addmain.grid(row=0, column=0, padx=5, pady=0)
add_list_type2_addfull.grid(row=0, column=1, padx=5, pady=0)

frame18 = tk.LabelFrame(tab2, text="Choose Network Type", padx=10, pady=0, labelanchor="n")
frame18.grid(row=8, column=0, columnspan=12, padx=10, pady=6)
network_type2_var = tk.StringVar()
network_type2_var.set("Mainnet")
network_type2_mainnet = tk.Radiobutton(frame18, text="Mainnet", variable=network_type2_var, value="Mainnet")
network_type2_testnet = tk.Radiobutton(frame18, text="Testnet", variable=network_type2_var, value="Testnet")
network_type2_mainnet.grid(row=0, column=0, padx=5, pady=0)
network_type2_testnet.grid(row=0, column=1, padx=5, pady=0)

continue_button2 = tk.Button(tab2, text="Generate Mnemonic Seed Phrase", command=mnemonic_converter2)
continue_button2.grid(row=9, column=0, columnspan=12, padx=10, pady=6)

result_label2 = tk.Label(tab2, text="", padx=10, pady=3, fg="red")
result_label2.grid(row=10, column=0, columnspan=12)

# Create tab 3: QR Code Generator
tab3 = tk.Frame(notebook)
notebook.add(tab3, text="QR Code Generator")

qr_label = tk.LabelFrame(tab3, text="Enter the intended text then click Generate QR Code", padx=10, pady=0,
                         labelanchor="n")
qr_label.grid(row=0, column=0, columnspan=12, padx=10, pady=5)
qr_text_entry = tk.Text(qr_label, height=3, width=55, font=("Helvetica", 9))
qr_text_entry.grid(row=1, column=0, columnspan=12, padx=3, pady=5)

qr_warning_label = tk.Label(tab3, text=f"Make sure to copy the intended text correctly."
                                       "\nWatch for unnecessary spaces, mistakes may lead to serious losses."
                                       "\nFor added privacy, QR code and text will be cleared after 1 minute of generation.", fg="red")
qr_warning_label.grid(row=2, column=0, columnspan=11, padx=10, pady=0)

generate_qr_button = tk.Button(tab3, text="Generate QR Code", command=generate_qr_code)
generate_qr_button.grid(row=6, column=0, columnspan=11, padx=10, pady=10)

qr_code_label = tk.Label(tab3)
qr_code_label.grid(row=7, column=0, columnspan=11)

continue_button.config(state="disabled")
result_label.config(text=f"The 'Generate Keys & Addresses' button is temporarily disabled. \nGenerate dice numbers to enable.")
on_entropy_mnemonic_select()
on_entropy_dice_select()
root.mainloop()
