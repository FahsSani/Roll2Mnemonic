from common import *

# Define fixed widths for each column in headers
word_width = 25
dice_width = 15
binary_width = 15
decimal_width = 15
index_width = 18

def generate_seed_phrase(num_words):
    mnemo = Mnemonic("english")
    seed_phrase = ' '.join(mnemo.generate(num_words=num_words))
    return seed_phrase

# Function to check if a seed phrase is valid
def is_valid_seed(seed_phrase):
    mnemonic = Mnemonic("english")
    words = seed_phrase.split()
    
    try:
        entropy = mnemonic.to_entropy(seed_phrase)
        return len(entropy) in [16, 32]  # Check if the entropy length is valid for 12 to 24 words
    except ValueError:
        return False

def convert_wordlist_to_binary(wordlist):
    binary_wordlist = {}
    for i, word in enumerate(wordlist, start=1):
        binary_word = bin(i - 1)[2:].zfill(11)
        binary_wordlist[binary_word] = word
    return binary_wordlist

def word_to_binary(word, word_list):
    try:
        index = word_list.index(word)
    except ValueError:
        raise ValueError("Word not found in the word list")

    binary_representation = bin(index)[2:].zfill(11)
    return binary_representation

def roll_dice(n):
    return [int(random.randint(1, 6) % 2 == 0) for _ in range(n)] # odd numbers are 0, even numbers are 1
#    return [int(random.randint(1, 6) > 3) for _ in range(n)] # You can enable this code to convert from (1, 2 or 3) to 0 and (4, 5 or 6) to 1

def roll_dice_auto(num_words):
    while True:
        mnemonic = []

        mnemo = Mnemonic("english")
        num_binary_digits = {
            12: 7,
            15: 6,
            18: 5,
            21: 4,
            24: 3
        }

        print_list_blue = []  # Create a list to store messages for printing
        print_list = []  # Create a list to store messages for printing

        # Append the header row
        header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index':<{index_width}}"
        print_list_blue.append(header)
        print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))

        for i in range(1, num_words):
            binary_digits = [roll_dice(1)[0] for _ in range(11)]
            binary_str = ''.join(map(str, binary_digits))
            decimal_value = int(binary_str, 2) + 1
            word = mnemo.wordlist[decimal_value - 1]
            binary = binary_str
            decimal = decimal_value - 1
            decimal_formatted = f"{decimal:04d}"
            index_num = str(decimal_value).zfill(4)
            index = f"{index_num} - {word}"
            row = f"           {i:02d}{' ' * (word_width - 13)}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)
            mnemonic.append(word)

        binary_digits = [roll_dice(1)[0] for _ in range(num_binary_digits[num_words])]
        binary_str = ''.join(map(str, binary_digits))
        row = f"           {num_words}{' ' * (word_width - 13)}{binary_str:<{binary_width}}"
        print_list_blue.append(row)
        print_list.append(f" Fetching valid checksum word...")
        print_list_blue.append("")

        last_word_binary = binary_str
        mnemo = Mnemonic("english")
        word_list = mnemo.wordlist
        binary_wordlist = convert_wordlist_to_binary(word_list)

        matching_words = [word for binary_word, word in binary_wordlist.items() if binary_word.startswith(last_word_binary)]

        if matching_words:
            random_matching_word = random.choice(matching_words)
            random_matching_word_binary = word_to_binary(random_matching_word, word_list)
            word_index = word_list.index(random_matching_word) 
            binary = random_matching_word_binary
            current_mnemonic = ' '.join(mnemonic[:]) + ' ' + random_matching_word

        # Append the header row
        header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index':<{index_width}}"
        print_list_blue.append(header)
        print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))

        if is_valid_seed(current_mnemonic):
            mnemonic.append(random_matching_word)
            decimal = word_index 
            decimal_formatted = f"{decimal:04d}"
            index_num = str(word_index+1).zfill(4)
            index = f"{index_num} - {random_matching_word}"
            row = f"           {num_words:02}{' ' * (word_width - 13)}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)

            bit_checksum = 11 - num_binary_digits[num_words]
            mnemonic_bits = (int(num_words)-1) * 11 + (11 - bit_checksum)           
            total_bits = (int(num_words)) * 11
            print()
            print_red(f" You've chosen to generate a {num_words}-word mnemonic seed phrase."
                      f"\n This requires rolling {mnemonic_bits} bits randomly and calculating {bit_checksum} bits for a valid checksum, totaling {total_bits} bits."
                      f"\n The dice will be rolled {mnemonic_bits} times.")
            print()
            # Print the appended messages if the seed is valid
            for msg in print_list_blue[:-3]:
                print_blue(msg)
            for msg in print_list:
                print(msg)
            print()
            for msg in print_list_blue[-3:]:
                print_blue(msg)
            return mnemonic

def roll_dice_manual_binary(num_words):
    mnemonic = []

    num_binary_digits = {
        12: 7,
        15: 6,
        18: 5,
        21: 4,
        24: 3
    }

    mnemo = Mnemonic("english")

    print_list_blue = []  # Create a list to store messages for printing
    print_list = []  # Create a list to store messages for printing
    input_binary_list = []  # Store binary representations of words
    input_words_list = []  # Store words

    bit_checksum = 11 - num_binary_digits[num_words]
    last_word_bit = 11 - bit_checksum           
    mnemonic_bits = (int(num_words)-1) * 11 + (11 - bit_checksum)           
    total_bits = (int(num_words)) * 11
    print()
    print_red(f" You've chosen to generate a {num_words}-word mnemonic seed phrase.")
    print_red(f" To create a {num_words}-word mnemonic, you need to randomly roll {mnemonic_bits} bits.")
    print_red(f" The script will calculate the last {bit_checksum} bits for checksum, totaling {total_bits} bits.")
    print_red(f" Roll the 6-sided dice{mnemonic_bits} times, record odd numbers (1, 3, 5) as 0 and even numbers (2, 4, 6) as 1.")
    print_red(f" Furthermore, you have the option to conduct {mnemonic_bits} coin tosses, assigning either 0 or 1 to each side and record the results.")
    print_red(f" For each word, input 11 binary numbers, for the last word, enter {last_word_bit} binary numbers.")
    print()

    for i in range(1, num_words):
        while True:
            binary_str = input(f" Enter 11 binary numbers (0 or 1) for Word {i:02}: [           ]\b\b\b\b\b\b\b\b\b\b\b\b")
            binary_str = binary_str.strip('[]')
            if len(binary_str) == 11 and binary_str.isdigit() and all(bit in '01' for bit in binary_str):
                input_binary_list.append(binary_str)
                break
            else:
                print(" Invalid input. Please enter 11 binary numbers (0 or 1) within the brackets.")
                
        decimal_value = int(binary_str, 2) + 1
        word = mnemo.wordlist[decimal_value - 1]

    while True:
        spaces = ' ' * num_binary_digits[num_words]
        backspaces = '\b' * len(spaces)
        binary_str = input(f" Enter {num_binary_digits[num_words]:02} binary digits for Word {num_words:02}: [{spaces}]{backspaces}\b")
        if len(binary_str) == num_binary_digits[num_words] and binary_str.isdigit() and all(bit in '01' for bit in binary_str):
            input_binary_list.append(binary_str)
            last_word_binary = binary_str
            break
        else:
            print(f" Invalid input. Please enter {num_binary_digits[num_words]} binary numbers (0 or 1) within the brackets.")

    print()
    print()


    # Append the header row
    header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index':<{index_width}}"
    print_list_blue.append(header)
    print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))

    # Print each row with corresponding decimal, index, and word
    for i, binary_word in enumerate(input_binary_list, start=1):
        decimal_value = int(binary_word, 2) + 1
        word = mnemo.wordlist[decimal_value - 1]
        binary = binary_word
        decimal = decimal_value - 1
        decimal_formatted = f"{decimal:04d}"
        index_num = str(decimal_value).zfill(4)
        index = f"{index_num} - {word}"
        if i == len(input_binary_list):
            row = f"           {i:02d}{' ' * (word_width - 13)}{binary:<{binary_width}}"
            print_list_blue.append(row)
        else:
            row = f"           {i:02d}{' ' * (word_width - 13)}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)
            mnemonic.append(word)

    print_list.append("")
    print_list.append(f" Fetching valid checksum word...")
    # Append the header row
    header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index':<{index_width}}"
    print_list_blue.append(header)
    print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))

    while True:
        mnemo = Mnemonic("english")
        word_list = mnemo.wordlist
        binary_wordlist = convert_wordlist_to_binary(word_list)

        matching_words = [word for binary_word, word in binary_wordlist.items() if binary_word.startswith(last_word_binary)]

        if matching_words:
            random_matching_word = random.choice(matching_words)
            random_matching_word_binary = word_to_binary(random_matching_word, word_list)
            word_index = word_list.index(random_matching_word)
            current_mnemonic = ' '.join(mnemonic[:]) + ' ' + random_matching_word

        if is_valid_seed(current_mnemonic):
            mnemonic.append(random_matching_word)
            binary = random_matching_word_binary
            decimal = word_index 
            decimal_formatted = f"{decimal:04d}"
            index_num = str(word_index+1).zfill(4)
            index = f"{index_num} - {random_matching_word}"
            row = f"           {num_words}{' ' * (word_width - 13)}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)
            for msg in print_list_blue[:-3]:
                print_blue(msg)
            for msg in print_list:
                print(msg)
            print()
            for msg in print_list_blue[-3:]:
                print_blue(msg)
            return mnemonic

def roll_dice_manual_num(num_words):
    mnemonic = []

    num_binary_digits = {
        12: 7,
        15: 6,
        18: 5,
        21: 4,
        24: 3
    }

    mnemo = Mnemonic("english")

    print_list_blue = []  # Create a list to store messages for printing
    print_list = []  # Create a list to store messages for printing
    input_digit_list = []  # Store digits
    input_binary_list = []  # Store binary representations of words
    input_words_list = []  # Store words

    bit_checksum = 11 - num_binary_digits[num_words]
    last_word_bit = 11 - bit_checksum           
    mnemonic_bits = (int(num_words) - 1) * 11 + (11 - bit_checksum)           
    total_bits = int(num_words) * 11
    print()
    print_red(f" You've chosen to generate a {num_words}-word mnemonic seed phrase."
              f"\n For {num_words}-word mnemonics, roll {mnemonic_bits} bits randomly."
              f"\n The script will calculate the last {bit_checksum} bits for checksum, totaling {total_bits} bits."
              f"\n The script will automatically convert odd numbers (1, 3, or 5) to 0 and even numbers (2, 4, or 6) to 1 during the process."
              f"\n Each word requires 11 binary numbers (1 to 6); for the last word, input only {last_word_bit} numbers.")
    print()

    for i in range(1, num_words):
        while True:
            digit = input(f" Enter 11 numbers between (1 and 6) for Word {i:02}: [           ]\b\b\b\b\b\b\b\b\b\b\b\b")
            digit = digit.strip('[]')
            if len(digit) == 11 and digit.isdigit() and all(digits in '123456' for digits in digit):
                binary_str = ''.join('0' if int(d) % 2 == 1 else '1' for d in digit)  # Convert each digit and join them
                input_binary_list.append(binary_str)
                input_digit_list.append(digit)
                break
            else:
                print(" Invalid input. Please enter 11  digits containing only '1,2,3,4,5 or 6' within the brackets.")

        decimal_value = int(binary_str, 2) + 1
        word = mnemo.wordlist[decimal_value - 1]

    while True:
        spaces = ' ' * num_binary_digits[num_words]
        backspaces = '\b' * len(spaces)
        digit = input(f" Enter {num_binary_digits[num_words]:02} numbers between (1 and 6) for Word {num_words:02}: [{spaces}]{backspaces}\b")
        digit = digit.strip('[]')
        if len(digit) == num_binary_digits[num_words] and digit.isdigit() and all(digits in '123456' for digits in digit):
            binary_str = ''.join('0' if int(d) % 2 == 1 else '1' for d in digit)  # Convert each digit and join them
            input_binary_list.append(binary_str)
            input_digit_list.append(digit)
            last_word_binary = binary_str
            break
        else:
            print(f" Invalid input. Please enter a number between 1 and 6.")

    print()
    print()

    # Append the header row
    header = f"{'           Word #':<{word_width}}{'Dice':<{dice_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index':<{index_width}}"
    print_list_blue.append(header)
    print_list_blue.append("           " + "-" * (word_width + dice_width + binary_width + decimal_width + index_width - 10))

    # Print each row with corresponding decimal, index, and word
    for i, binary_word in enumerate(input_binary_list, start=1):
        decimal_value = int(binary_word, 2) + 1
        word = mnemo.wordlist[decimal_value - 1]
        dice = input_digit_list[i - 1]  # Get the corresponding digit from input_digit_list
        binary = binary_word
        decimal = decimal_value - 1
        decimal_formatted = f"{decimal:04d}"
        index_num = str(decimal_value).zfill(4)
        index = f"{index_num} - {word}"
        if i == len(input_binary_list):
            row = f"           {i:02d}{' ' * (word_width - 13)}{dice:<{dice_width}}{binary:<{binary_width}}"
            print_list_blue.append(row)
        else:
            row = f"           {i:02d}{' ' * (word_width - 13)}{dice:<{dice_width}}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)
            mnemonic.append(word)

    print_list.append("")
    print_list.append(f" Fetching valid checksum word...")

    # Append the header row
    header = f"{'           Word #':<{word_width}}{'Dice':<{dice_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index':<{index_width}}"
    print_list_blue.append(header)
    print_list_blue.append("           " + "-" * (word_width + dice_width + binary_width + decimal_width + index_width - 10))

    while True:
        mnemo = Mnemonic("english")
        word_list = mnemo.wordlist
        binary_wordlist = convert_wordlist_to_binary(word_list)
        matching_words = [word for binary_word, word in binary_wordlist.items() if binary_word.startswith(last_word_binary)]

        if matching_words:
            random_matching_word = random.choice(matching_words)
            random_matching_word_binary = word_to_binary(random_matching_word, word_list)
            word_index = word_list.index(random_matching_word)
            current_mnemonic = ' '.join(mnemonic[:]) + ' ' + random_matching_word

        if is_valid_seed(current_mnemonic):
            mnemonic.append(random_matching_word)
            dice = "-"
            binary = random_matching_word_binary
            decimal = word_index 
            decimal_formatted = f"{decimal:04d}"
            index_num = str(word_index+1).zfill(4)
            index = f"{index_num} - {random_matching_word}"
            row = f"           {i:02d}{' ' * (word_width - 13)}{dice:<{dice_width}}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)
            for msg in print_list_blue[:-3]:
                print_blue(msg)
            for msg in print_list:
                print(msg)
            print()
            for msg in print_list_blue[-3:]:
                print_blue(msg)
            return mnemonic      
