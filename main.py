from Roll2Mnemonic.common import *
from Roll2Mnemonic.diceroll_auto import dr_auto
from Roll2Mnemonic.diceroll_binary import dr_binary
from Roll2Mnemonic.diceroll_numeric import dr_numeric
from Roll2Mnemonic.mccmainnet import generate_mainnet_wallet
from Roll2Mnemonic.mcctestnet import generate_testnet_wallet
from Roll2Mnemonic.bip85 import bip85_generator

global seed_phrase, passphrase

def enable_buttons():
    t1_start_dice_button.config(state="normal")
    tab1_generate_keys_button.config(state="normal")
    tab2_generate_keys_button.config(state="normal")

def disable_buttons():
    t1_start_dice_button.config(state="disabled")
    tab1_generate_keys_button.config(state="disabled")
    tab2_generate_keys_button.config(state="disabled")

def on_own_dice_select():
    t1f3_dice_choice_binary.config(state="normal")
    t1f3_dice_choice_dice.config(state="normal")

def on_entropy_dice_select():
    t1f3_dice_choice_binary.config(state="disabled")
    t1f3_dice_choice_dice.config(state="disabled")

def on_entropy_mnemonic_select():
    tab2_f2.grid_remove()
    tab2_f3.grid()
    tab2_f4.grid()
    tab2_message.config(text="")

def on_own_mnemonic_select():
    tab2_f2.grid()
    tab2_f3.grid_remove()
    tab2_f4.grid_remove()
    tab2_message.config(text="")

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
        value = int(t2f4_entropy_entry.get().replace(',', ''))
        formatted_value = format_with_thousand_separator(value)
        t2f4_entropy_entry.delete(0, tk.END)
        t2f4_entropy_entry.insert(0, formatted_value)
    except ValueError:
        pass

def on_entry_change_indices(event):
    def format_and_set_entry(entry, value):
        formatted_value = format_with_thousand_separator(value)
        entry.delete(0, tk.END)
        entry.insert(0, formatted_value)

    try:
        value_indices = int(t3f4_index_specific_entry.get().replace(',', ''))
        format_and_set_entry(t3f4_index_specific_entry, value_indices)
    except ValueError:
        t3f4_index_specific_entry.delete(0, tk.END)
        t3f4_index_specific_entry.insert(0, "0")  # Set a default value or display an error message
        tab3_message.config(text="Invalid Child Index. Value has been reset.")

    try:
        value_start = int(t3f4_index_range_start_entry.get().replace(',', ''))
        format_and_set_entry(t3f4_index_range_start_entry, value_start)
    except ValueError:
        t3f4_index_range_start_entry.delete(0, tk.END)
        t3f4_index_range_start_entry.insert(0, "0")  # Set a default value or display an error message
        tab3_message.config(text="Invalid Indices Start. Value has been reset.")

    try:
        value_end = int(t3f4_index_range_end_entry.get().replace(',', ''))
        format_and_set_entry(t3f4_index_range_end_entry, value_end)
    except ValueError:
        t3f4_index_range_end_entry.delete(0, tk.END)
        t3f4_index_range_end_entry.insert(0, "5")  # Set a default value or display an error message
        tab3_message.config(text="Invalid Indices End. Value has been reset.")

def on_indices_change():
    selected_value = t3f4_child_index_type.get()
    if selected_value == "Specific":
        t3f4_index_specific_entry.grid()  # Allow entry for specific index
        t3f4_index_range_start_entry.grid_remove()  # Hide index start entry
        t3f4_index_range_end_entry.grid_remove()    # Hide index end entry
    elif selected_value == "Range":
        t3f4_index_specific_entry.grid_remove()  # Disable entry for range
        t3f4_index_range_start_entry.grid()  # Display index start entry
        t3f4_index_range_end_entry.grid()    # Display index end entry

def start_dice():
    global seed_phrase
    main()
    dice = t1f1_dice_type.get()
    num_words = int(t1f2_num_words_var.get())

    if dice == "Entropy":
        mnemonic_seed = dr_auto(num_words)
        tab1_generate_keys_button.config(state="normal")
        tab1_message.config(text="")

    elif dice == "Own":
        disable_buttons()
        choice = t1f3_dice_choice_var.get()
        if choice == "Binary":
            mnemonic_seed = dr_binary(num_words)
            enable_buttons()
        else:
            mnemonic_seed = dr_numeric(num_words)
            enable_buttons()

    seed_phrase = ' '.join(mnemonic_seed)
    print_green(f"\n Mnemonic Seed Phrase: {seed_phrase}")
    foot_note()
    tab1_message.config(text="Dice Roll Completed Successfully.")
     
def generate_dice_seed():
    global seed_phrase, passphrase
    passphrase = t1f4_passphrase.get().strip()
    list_type = t1f6_address_list_type_var.get()
    try:
        num_child_keys = int(t1f5_child_keys.get())
        if 1 <= num_child_keys <= 25:
            network_type = t1f7_network_type_var.get()
            tab1_message.config(text="Mnemonic Seed Phrase Generated Successfully.")
            if network_type == "Mainnet":
                generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
            elif network_type == "Testnet":
                generate_testnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
#            tab1_generate_keys_button.config(state="disabled") ##########################################################################
            tab1_continue_to_bip85_button.config(state="normal")
        else:
            tab1_message.config(text="Invalid number of child keys. Must be between 1 and 25.")
    except ValueError:
        tab1_message.config(text="Invalid number of child keys. Must be an integer.")

def generate_seed():
    global seed_phrase, passphrase
    main()
    passphrase = t2f5_passphrase.get().strip()
    num_words = int(t2f3_num_words_var.get())
    t2f1_mnemonic_choice_value = t2f1_mnemonic_choice.get()
    list_type = t2f7_address_list_type_var.get()

    if t2f1_mnemonic_choice_value == "Entropy":
        try:
            num_child_keys = int(t2f6_child_keys.get())
            if 1 <= num_child_keys <= 25:
                try:
                    entropy_generation = int(t2f4_entropy_entry.get().replace(',', ''))
                    if 1000 <= entropy_generation <= 10000000:
                        entropy_lengths = {"12": 128, "15": 160, "18": 192, "21": 224, "24": 256}
                        entropy_bytes = entropy_lengths.get(str(num_words))

                        random_data_list = [os.urandom(entropy_bytes // 8) for _ in range(entropy_generation)]
                        print(f"\n Generating a list of {entropy_generation:,} random Hex entropies.")
                        entropy_display = t2f4_display_entropy.get()
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
                                tab2_message.config(text="Mnemonic Seed Phrase Generated Successfully.")
                                tab2_continue_to_bip85_button.config(state="normal")
                                network_type = t2f8_network_type_var.get()
                                if network_type == "Mainnet":
                                    generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                                elif network_type == "Testnet":
                                    generate_testnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                                return
                    else:
                        tab2_message.config(text="Invalid number of entropies, must be between 10,000 and 10,000,000.")
                except ValueError:
                    tab2_message.config(text="Invalid number of entropies, must be an integer.")
            else:
                tab2_message.config(text="Invalid number of child keys, must be between 1 and 25.")
        except ValueError:
            tab2_message.config(text="Invalid number of child keys, must be an integer.")

    else:
        seed_phrase = t2f2_mnemonic_entry.get("1.0", "end-1c")
        try:
            num_child_keys = int(t2f6_child_keys.get())
            if 1 <= num_child_keys <= 25:
                try:
                    if is_valid_seed(seed_phrase):
                        tab2_message.config(text="Mnemonic Seed Phrase Generated Successfully.")
                        tab2_continue_to_bip85_button.config(state="normal")
                        network_type = t2f8_network_type_var.get()
                        if network_type == "Mainnet":
                            generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                        elif network_type == "Testnet":
                            generate_testnet_wallet(seed_phrase, num_child_keys, passphrase, list_type)
                    else:
                        tab2_message.config(text="Invalid Mnemonic Seed Phrase, make sure that the seed phrase is valid"
                                                  "\nand that there are no spaces before or after the seed phrase.")
                except Exception as e:
                    tab2_message.config(text=f"An error occurred while generating the wallet: {str(e)}")
            else:
                tab2_message.config(text="Invalid number of child keys, must be between 1 and 25.")
        except ValueError:
            tab2_message.config(text="Invalid number of child keys, must be an integer.")
    

def bip85_child_keys():
    main()
    print()
    print()

    parent_seed_phrase = tab3_f1_parent_mnemonic.get("1.0", "end-1c")
    if not is_valid_seed(parent_seed_phrase):
        tab3_message.config(text="Invalid Parent Mnemonic Seed Phrase, make sure that the seed phrase is valid")
        return

    parent_passphrase = t3f2_parent_passphrase.get().strip()
    num_words = int(t3f3_num_words_var.get())
    index_type = t3f4_child_index_type.get()
    index_specific = t3f4_index_specific_entry.get().replace(',', '')
    indices_start = t3f4_index_range_start_entry.get().replace(',', '')
    indices_end = t3f4_index_range_end_entry.get().replace(',', '')

    result = bip85_generator(parent_seed_phrase, parent_passphrase, num_words, index_type, index_specific, indices_start, indices_end)
    tab3_message.config(text=f"{result}")

def transfer_to_bip85(seed_phrase, passphrase):
    tab3_f1_parent_mnemonic.delete("1.0", tk.END)
    tab3_f1_parent_mnemonic.insert("1.0", seed_phrase)

    t3f2_parent_passphrase.delete(0, tk.END)
    t3f2_parent_passphrase.insert(0, passphrase)

    notebook.select(tab3)
    tab1_continue_to_bip85_button.config(state="disabled")
    tab2_continue_to_bip85_button.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("Roll2Mnemonic")
root.geometry("450x480")

# Create tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both')

# Create tab 1: Dice Roll
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Dice Roll")

tab1_f1 = tk.LabelFrame(tab1, text="Dice Roll Type", labelanchor="n")
tab1_f1.grid(row=0, column=0, columnspan=12, padx=10, pady=5)
t1f1_dice_type = tk.StringVar()
t1f1_dice_type.set("Entropy")
t1f1_dice_type_entropy = tk.Radiobutton(tab1_f1, text="Generate From Entropy", variable=t1f1_dice_type, value="Entropy")
t1f1_dice_type_own = tk.Radiobutton(tab1_f1, text="Enter Your Own Numbers", variable=t1f1_dice_type, value="Own")
t1f1_dice_type_entropy.grid(row=0, column=0, padx=10, pady=0)
t1f1_dice_type_own.grid(row=0, column=1, padx=10, pady=0)
t1f1_dice_type_own.bind("<Button-1>", lambda event: on_own_dice_select())
t1f1_dice_type_entropy.bind("<Button-1>", lambda event: on_entropy_dice_select())

tab1_f2 = tk.LabelFrame(tab1, text="Mnemonic Seed Phrase Word Count", labelanchor="n")
tab1_f2.grid(row=1, column=0, columnspan=12, padx=10, pady=5)
t1f2_num_words_var = tk.IntVar()
t1f2_num_words_var.set(12)
t1f2_mnemonic_words = [12, 15, 18, 21, 24]
for i, t1f2_word_count in enumerate(t1f2_mnemonic_words):
    t1f2_num_words_button = tk.Radiobutton(tab1_f2, text=str(t1f2_word_count) + " Words", variable=t1f2_num_words_var, value=t1f2_word_count,
                                      command=lambda count=t1f2_word_count: t1f2_num_words_var.set(count))
    t1f2_num_words_button.grid(row=0, column=i + 2, padx=4, pady=0)

tab1_f3 = tk.LabelFrame(tab1, text="Choose Input Type", padx=10, pady=0, labelanchor="n")
tab1_f3.grid(row=2, column=0, columnspan=12, padx=10, pady=5)
t1f3_dice_choice_var = tk.StringVar()
t1f3_dice_choice_var.set("Binary")
t1f3_dice_choice_binary = tk.Radiobutton(tab1_f3, text="Binary/Coin Toss", variable=t1f3_dice_choice_var, value="Binary")
t1f3_dice_choice_dice = tk.Radiobutton(tab1_f3, text="6-sided Dice Roll", variable=t1f3_dice_choice_var, value="Dice")
t1f3_dice_choice_binary.grid(row=0, column=0, padx=4, pady=0)
t1f3_dice_choice_dice.grid(row=0, column=1, padx=4, pady=0)

t1_start_dice_button = tk.Button(tab1, text="Start Dice Roll", command=start_dice)
t1_start_dice_button.grid(row=3, column=0, columnspan=12, padx=10, pady=5)

tab1_f4 = tk.LabelFrame(tab1, text="Passphrase (Optional)", padx=10, pady=5, labelanchor="n")
tab1_f4.grid(row=4, column=0, columnspan=1, padx=26, pady=0)
t1f4_passphrase = tk.Entry(tab1_f4, justify="center")
t1f4_passphrase.grid(row=0, column=1)
t1f4_passphrase.config(width=25)

tab1_f5 = tk.LabelFrame(tab1, text="Number Of Child Keys (1-25)", padx=10, pady=5, labelanchor="n")
tab1_f5.grid(row=4, column=1, columnspan=1, padx=10, pady=10)
t1f5_child_keys = tk.Entry(tab1_f5, justify="center")
t1f5_child_keys.insert(0, "5")
t1f5_child_keys.grid(row=0, column=1)
t1f5_child_keys.config(width=25)

tab1_f6 = tk.LabelFrame(tab1, text="Addresses Details", padx=10, pady=0, labelanchor="n")
tab1_f6.grid(row=5, column=0, columnspan=12, padx=10, pady=0)
t1f6_address_list_type_var = tk.StringVar()
t1f6_address_list_type_var.set("AddMain")
t1f6_address_list_type_addmain = tk.Radiobutton(tab1_f6, text="Addresses & Private Keys", variable=t1f6_address_list_type_var, value="AddMain")
t1f6_address_list_type_addfull = tk.Radiobutton(tab1_f6, text="Addresses & Public/Private Keys", variable=t1f6_address_list_type_var, value="AddFull")
t1f6_address_list_type_addmain.grid(row=0, column=0, padx=5, pady=0)
t1f6_address_list_type_addfull.grid(row=0, column=1, padx=5, pady=0)

tab1_f7 = tk.LabelFrame(tab1, text="Choose Network Type", padx=10, pady=0, labelanchor="n")
tab1_f7.grid(row=6, column=0, columnspan=12, padx=10, pady=10)
t1f7_network_type_var = tk.StringVar()
t1f7_network_type_var.set("Mainnet")
t1f7_network_type_mainnet = tk.Radiobutton(tab1_f7, text="Mainnet", variable=t1f7_network_type_var, value="Mainnet")
t1f7_network_type_testnet = tk.Radiobutton(tab1_f7, text="Testnet", variable=t1f7_network_type_var, value="Testnet")
t1f7_network_type_mainnet.grid(row=0, column=0, padx=5, pady=0)
t1f7_network_type_testnet.grid(row=0, column=1, padx=5, pady=0)

tab1_generate_keys_button = tk.Button(tab1, text="Generate Keys & Addresses", command=generate_dice_seed)
tab1_generate_keys_button.grid(row=7, column=0, columnspan=1, padx=0, pady=5)

tab1_continue_to_bip85_button = tk.Button(tab1, text="Transfer To BIP85 Generator", command=lambda: transfer_to_bip85(seed_phrase, passphrase))
tab1_continue_to_bip85_button.grid(row=7, column=1, columnspan=1, padx=20, pady=5)

tab1_message = tk.Label(tab1, text="", padx=10, pady=5, fg="red")
tab1_message.grid(row=8, column=0, columnspan=12)

# Create tab 2: Mnemonic Code Converter
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="Mnemonic Converter")

tab2_f1 = tk.LabelFrame(tab2, text="Mnemonic Seed Phrase", labelanchor="n")
tab2_f1.grid(row=0, column=0, columnspan=12, padx=10, pady=5)
t2f1_mnemonic_choice = tk.StringVar()
t2f1_mnemonic_choice.set("Entropy")
t2f1_mnemonic_choice_entropy = tk.Radiobutton(tab2_f1, text="Generate From Entropy", variable=t2f1_mnemonic_choice, value="Entropy")
t2f1_mnemonic_choice_own = tk.Radiobutton(tab2_f1, text="Enter Your Own Seed", variable=t2f1_mnemonic_choice, value="Own")
t2f1_mnemonic_choice_entropy.grid(row=0, column=0, padx=10, pady=0)
t2f1_mnemonic_choice_own.grid(row=0, column=1, padx=10, pady=0)
t2f1_mnemonic_choice_entropy.bind("<Button-1>", lambda event: on_entropy_mnemonic_select())
t2f1_mnemonic_choice_own.bind("<Button-1>", lambda event: on_own_mnemonic_select())

tab2_f2 = tk.LabelFrame(tab2, text="Mnemonic Seed Phrase (12, 15, 18, 21, 24 Words Only)", padx=10, pady=5, labelanchor="n")
tab2_f2.grid(row=2, column=0, columnspan=12, padx=11, pady=5)
t2f2_mnemonic_entry = tk.Text(tab2_f2, height=7, width=54, font=("Helvetica", 9))
t2f2_mnemonic_entry.grid(row=0, column=0, padx=10, pady=0)
t2f2_mnemonic_entry.insert("1.0", "Word1 Word2 Word3 .....")

tab2_f3 = tk.LabelFrame(tab2, text="Mnemonic Seed Phrase Word Count", labelanchor="n")
tab2_f3.grid(row=2, column=0, columnspan=12, padx=10, pady=5)
t2f3_num_words_var = tk.IntVar()
t2f3_num_words_var.set(12)
t2f3_mnemonic_words = [12, 15, 18, 21, 24]
for i, t2f3_word_count in enumerate(t2f3_mnemonic_words):
    t2f3_num_words_button = tk.Radiobutton(tab2_f3, text=str(t2f3_word_count) + " Words", variable=t2f3_num_words_var, value=t2f3_word_count,
                                      command=lambda count=t2f3_word_count: t2f3_num_words_var.set(count))
    t2f3_num_words_button.grid(row=0, column=i + 2, padx=4, pady=0)

tab2_f4 = tk.LabelFrame(tab2, text="Number Of Hex Entropies To Generate (1,000 - 10,000,000)", padx=10, pady=6, labelanchor="n")
tab2_f4.grid(row=3, column=0, columnspan=12, padx=10, pady=6)
t2f4_entropy_entry = tk.Entry(tab2_f4, justify="center")
t2f4_entropy_entry.insert(0, "1,000,000")
t2f4_entropy_entry.grid(row=0, column=0, columnspan=6, padx=5, pady=0)
t2f4_entropy_entry.config(width=30)
t2f4_entropy_entry.bind("<FocusOut>", on_entry_change)

t2f4_display_entropy = tk.StringVar()
t2f4_display_entropy.set("Hide")
t2f4_display_entropy_yes = tk.Radiobutton(tab2_f4, text="Display Entropy", variable=t2f4_display_entropy, value="Display")
t2f4_display_entropy_no = tk.Radiobutton(tab2_f4, text="Hide Entropy", variable=t2f4_display_entropy, value="Hide")
t2f4_display_entropy_yes.grid(row=0, column=10)
t2f4_display_entropy_no.grid(row=0, column=11)

t2f4_display_entropy_warning = tk.Label(tab2_f4, text="Displaying a long list of entropies may take a significant amount of time", fg="red")
t2f4_display_entropy_warning.grid(row=1, column=0, columnspan=12)

tab2_f5 = tk.LabelFrame(tab2, text="Passphrase (optional)", padx=10, pady=5, labelanchor="n")
tab2_f5.grid(row=5, column=0, columnspan=6, padx=10, pady=5)
t2f5_passphrase = tk.Entry(tab2_f5, justify="center")
t2f5_passphrase.grid(row=0, column=1)
t2f5_passphrase.config(width=25)

tab2_f6 = tk.LabelFrame(tab2, text="Number Of Child Keys (1-25)", padx=10, pady=5, labelanchor="n")
tab2_f6.grid(row=5, column=6, columnspan=6, padx=10, pady=5)
t2f6_child_keys = tk.Entry(tab2_f6, justify="center")
t2f6_child_keys.insert(0, "5")
t2f6_child_keys.grid(row=0, column=1)
t2f6_child_keys.config(width=25)

tab2_f7 = tk.LabelFrame(tab2, text="Addresses Details", padx=10, pady=0, labelanchor="n")
tab2_f7.grid(row=7, column=0, columnspan=12, padx=10, pady=6)
t2f7_address_list_type_var = tk.StringVar()
t2f7_address_list_type_var.set("AddMain")
t2f7_address_list_type_addmain = tk.Radiobutton(tab2_f7, text="Addresses & Private Keys", variable=t2f7_address_list_type_var, value="AddMain")
t2f7_address_list_type_addfull = tk.Radiobutton(tab2_f7, text="Addresses & Public/Private Keys", variable=t2f7_address_list_type_var, value="AddFull")
t2f7_address_list_type_addmain.grid(row=0, column=0, padx=5, pady=0)
t2f7_address_list_type_addfull.grid(row=0, column=1, padx=5, pady=0)

tab2_f8 = tk.LabelFrame(tab2, text="Choose Network Type", padx=10, pady=0, labelanchor="n")
tab2_f8.grid(row=8, column=0, columnspan=12, padx=10, pady=6)
t2f8_network_type_var = tk.StringVar()
t2f8_network_type_var.set("Mainnet")
t2f8_network_type_mainnet = tk.Radiobutton(tab2_f8, text="Mainnet", variable=t2f8_network_type_var, value="Mainnet")
t2f8_network_type_testnet = tk.Radiobutton(tab2_f8, text="Testnet", variable=t2f8_network_type_var, value="Testnet")
t2f8_network_type_mainnet.grid(row=0, column=0, padx=5, pady=0)
t2f8_network_type_testnet.grid(row=0, column=1, padx=5, pady=0)

tab2_generate_keys_button = tk.Button(tab2, text="Generate Keys & Addresses", command=generate_seed)
tab2_generate_keys_button.grid(row=9, column=0, columnspan=6, padx=0, pady=6)

tab2_continue_to_bip85_button = tk.Button(tab2, text="Transfer To BIP85 Generator", command=lambda: transfer_to_bip85(seed_phrase, passphrase))
tab2_continue_to_bip85_button.grid(row=9, column=6, columnspan=6, padx=20, pady=6)

tab2_message = tk.Label(tab2, text="", padx=10, pady=3, fg="red")
tab2_message.grid(row=10, column=0, columnspan=12)

# Create tab 3: BIP85 Generator
tab3 = tk.Frame(notebook)
notebook.add(tab3, text="BIP85 Generator")

tab3_f1 = tk.LabelFrame(tab3, text="Parent Mnemonic Seed Phrase (12, 15, 18, 21, 24 Words Only)", padx=10, pady=5, labelanchor="n")
tab3_f1.grid(row=0, column=0, columnspan=12, padx=11, pady=5)
tab3_f1_parent_mnemonic = tk.Text(tab3_f1, height=7, width=54, font=("Helvetica", 9))
tab3_f1_parent_mnemonic.grid(row=0, column=0, padx=10, pady=0)
tab3_f1_parent_mnemonic.insert("1.0", "Word1 Word2 Word3 .....")

tab3_f2 = tk.LabelFrame(tab3, text="Parent Passphrase (Optional)", padx=10, pady=5, labelanchor="n")
tab3_f2.grid(row=1, column=0, columnspan=12, padx=11, pady=5)
t3f2_parent_passphrase = tk.Entry(tab3_f2, justify="center")
t3f2_parent_passphrase.grid(row=0, column=0)
t3f2_parent_passphrase.config(width=50)

tab3_f3 = tk.LabelFrame(tab3, text="BIP85 Child Mnemonic Seed Phrase Word Count", labelanchor="n")
tab3_f3.grid(row=2, column=0, columnspan=12, padx=10, pady=5)
t3f3_num_words_var = tk.IntVar()
t3f3_num_words_var.set(12)
t3f3_mnemonic_words_child = [12, 15, 18, 21, 24]
for i, t3f3_word_count in enumerate(t3f3_mnemonic_words_child):
    t3f3_num_words_child_button = tk.Radiobutton(tab3_f3, text=str(t3f3_word_count) + " Words", variable=t3f3_num_words_var,
                                                 value=t3f3_word_count, command=lambda count=t3f3_word_count: t3f3_num_words_var.set(count))
    t3f3_num_words_child_button.grid(row=0, column=i + 2, padx=4, pady=0)

tab3_f4 = tk.LabelFrame(tab3, text="Enter Number Of BIP85 Indices ( 0 - 2,147,483,647 )", padx=10, pady=6, labelanchor="n", width=66)
tab3_f4.grid(row=3, column=0, columnspan=12, padx=10, pady=6)

t3f4_child_index_type = tk.StringVar()
t3f4_child_index_type.set("Specific")

t3f4_child_index_type_specific = tk.Radiobutton(tab3_f4, text="Specific Index", variable=t3f4_child_index_type, value="Specific", command=on_indices_change)
t3f4_child_index_type_range = tk.Radiobutton(tab3_f4, text="Range Indices", variable=t3f4_child_index_type, value="Range", command=on_indices_change)
t3f4_child_index_type_specific.grid(row=0, column=0, padx=20, pady=0)
t3f4_child_index_type_range.grid(row=0, column=1, padx=20, pady=0)

t3f4_index_specific_entry = tk.Entry(tab3_f4, justify="center")
t3f4_index_specific_entry.insert(0, "0")
t3f4_index_specific_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=0)
t3f4_index_specific_entry.config(width=30)
t3f4_index_specific_entry.bind("<FocusOut>", on_entry_change_indices)

t3f4_index_range_start_entry = tk.Entry(tab3_f4, justify="center", state=tk.NORMAL)
t3f4_index_range_start_entry.insert(0, "0")
t3f4_index_range_start_entry.grid(row=1, column=0, padx=5, pady=0)
t3f4_index_range_start_entry.bind("<FocusOut>", on_entry_change_indices)
t3f4_index_range_end_entry = tk.Entry(tab3_f4, justify="center", state=tk.NORMAL)
t3f4_index_range_end_entry.insert(0, "5")
t3f4_index_range_end_entry.grid(row=1, column=1, padx=5, pady=0)
t3f4_index_range_end_entry.bind("<FocusOut>", on_entry_change_indices)

tab3_bip85_button = tk.Button(tab3, text="Generate BIP85 Child Keys", command=bip85_child_keys)
tab3_bip85_button.grid(row=4, column=0, columnspan=12, padx=10, pady=6)

tab3_message = tk.Label(tab3, text="", padx=10, pady=3, fg="red")
tab3_message.grid(row=5, column=0, columnspan=12)

# Create tab 4: QR Code Generator
tab4 = tk.Frame(notebook)
notebook.add(tab4, text="QR Code Generator")

qr_label = tk.LabelFrame(tab4, text="Enter the intended text then click Generate QR Code", padx=10, pady=0,
                         labelanchor="n")
qr_label.grid(row=0, column=0, columnspan=12, padx=10, pady=5)
qr_text_entry = tk.Text(qr_label, height=3, width=55, font=("Helvetica", 9))
qr_text_entry.grid(row=1, column=0, columnspan=12, padx=3, pady=5)

qr_warning_label = tk.Label(tab4, text=f"Make sure to copy the intended text correctly."
                                       "\nWatch for unnecessary spaces, mistakes may lead to serious losses."
                                       "\nFor added privacy, QR code and text will be cleared after 1 minute of generation.", fg="red")
qr_warning_label.grid(row=2, column=0, columnspan=11, padx=10, pady=0)

generate_qr_button = tk.Button(tab4, text="Generate QR Code", command=generate_qr_code)
generate_qr_button.grid(row=6, column=0, columnspan=11, padx=10, pady=10)

qr_code_label = tk.Label(tab4)
qr_code_label.grid(row=7, column=0, columnspan=11)

if __name__ == "__main__":
    maximize_window()
    disclaimer()
    tab1_generate_keys_button.config(state="disabled")
    tab1_continue_to_bip85_button.config(state="disabled")
    tab2_continue_to_bip85_button.config(state="disabled")
    tab1_message.config(text=f"Buttons are temporarily disabled. \nStart dice roll to enable.")
    on_entropy_mnemonic_select()
    on_entropy_dice_select()
    on_indices_change()
    root.mainloop()
