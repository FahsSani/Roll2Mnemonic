from common import *

# Define fixed widths for each column in headers
word_width = 25
dice_width = 15
binary_width = 15
decimal_width = 15
index_width = 18

def generate_seed_phrase(num_words):
    mnemo = Mnemonic("english")
    seed_phrase = ' '.join(mnemo.generate(num_words))
    return seed_phrase

def convert_wordlist_to_binary(wordlist):
    binary_wordlist = {}
    for i, word in enumerate(wordlist, start=1):
        binary_word = bin(i - 1)[2:].zfill(11)
        binary_wordlist[binary_word] = word
    return binary_wordlist

def word_to_binary(word, word_list):
    index = word_list.index(word)
    binary_representation = bin(index)[2:].zfill(11)
    return binary_representation

import random

def roll_dice(n):
    auto_dice_list = []
    for i in range(10000):
        auto_dice = [int(random.randint(1, 1000)) for _ in range(n)] 
        auto_dice_list.append(auto_dice)
    auto_dice = random.choice(auto_dice_list)
    auto_dice_binary = [1 if num % 2 == 0 else 0 for num in auto_dice]  # odd numbers are converted 0, even numbers are converted 1  
    return auto_dice_binary

def roll_dice_auto(num_words):
    while True:
        mnemo = Mnemonic("english")
        word_list = mnemo.wordlist
        binary_wordlist = convert_wordlist_to_binary(word_list)

        num_binary_digits = {12: 7, 15: 6, 18: 5, 21: 4, 24: 3}
        mnemonic = []
        print_list_blue = []  # Create a list to store messages for printing
        print_list = []  # Create a list to store messages for printing
        valid_words_list = []
        
        # Append the header row
        header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index & Word':<{index_width}}"
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
        last_word_binary = ''.join(map(str, binary_digits))
        row = f"           {num_words}{' ' * (word_width - 13)}{last_word_binary:<{binary_width}}"
        print_list_blue.append(row)
        print_list_blue.append("")
      

        matching_words = [word for binary_word, word in binary_wordlist.items() if binary_word.startswith(last_word_binary)]
        print_list.append(f" Fetching words that start with last word binary input.")
        print_list.append(f" Found {len(matching_words)} word(s) that start with last word binary input.")
        print_list.append(f" Fetching if any of the {len(matching_words)} word(s) has a valid checksum.")

        for word in matching_words:
            temp_matching_word = word
            temp_mnemonic = ' '.join(mnemonic[:]) + ' ' + temp_matching_word
            if is_valid_seed(temp_mnemonic):
                valid_words_list.append(temp_matching_word)

        valid_word_count = len(valid_words_list)

        print_list.append(f" Found {valid_word_count} word(s) with valid checksum, choosing a word to proceed.")

        for word in valid_words_list:
            valid_word = word
            current_mnemonic = ' '.join(mnemonic[:]) + ' ' + valid_word
                    
        if is_valid_seed(current_mnemonic):
            mnemonic.append(valid_word)
            binary = word_to_binary(valid_word, word_list)
            decimal = word_list.index(valid_word) 
            decimal_formatted = f"{decimal:04d}"
            index_num = str(decimal+1).zfill(4)
            index = f"{index_num} - {valid_word}"
            header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index & Word':<{index_width}}"
            print_list_blue.append(header)
            print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))
            row = f"           {num_words:02}{' ' * (word_width - 13)}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)

            bit_checksum = 11 - num_binary_digits[num_words]
            mnemonic_bits = (int(num_words)-1) * 11 + (11 - bit_checksum)       
            total_bits = (int(num_words)) * 11
            print()
            print_red(f" You've chosen to generate a {num_words}-word mnemonic seed phrase."
                      f"\n This requires rolling {mnemonic_bits} bits randomly and calculating {bit_checksum} bits for a valid checksum, totaling {total_bits} bits."
                      f"\n For each bit in the {mnemonic_bits} bits, a 1,000-sided dice will be roll 10,000 times and the results will be stored in a list."
                      f"\n Subsequently, a random number will be selected from the list and transformed into 0 if it's odd or 1 if it's even.")
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
    mnemo = Mnemonic("english")
    word_list = mnemo.wordlist
    binary_wordlist = convert_wordlist_to_binary(word_list)

    num_binary_digits = {12: 7, 15: 6, 18: 5, 21: 4, 24: 3}
    mnemonic = []
    print_list_blue = []  # Create a list to store messages for printing
    print_list = []  # Create a list to store messages for printing
    input_binary_list = []  # Store binary representations of words
    valid_words_list = []

    bit_checksum = 11 - num_binary_digits[num_words]
    last_word_bit = 11 - bit_checksum           
    mnemonic_bits = (int(num_words)-1) * 11 + (11 - bit_checksum)           
    total_bits = (int(num_words)) * 11
    print()
    print_red(f" You've chosen to generate a {num_words}-word mnemonic seed phrase."
              f"\n To create a {num_words}-word mnemonic, you need {total_bits} bits of entropy."
              f"\n You need {mnemonic_bits} random dice rolls or coin tosses."
              f"\n The script will calculate the last {bit_checksum} bits for a valid checksum, totaling {total_bits} bits."
              f"\n Roll the 6-sided dice {mnemonic_bits} times, record odd numbers (1, 3, 5) as 0 and even numbers (2, 4, 6) as 1."
              f"\n Furthermore, you can conduct {mnemonic_bits} coin tosses, assigning either 0 or 1 to each side and record the results."
              f"\n For each word, input 11 binary numbers, for the last word, enter {last_word_bit} binary numbers.")
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
    header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index & Word':<{index_width}}"
    print_list_blue.append(header)
    print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))

    # Print each row with corresponding decimal, index, and word
    for i, binary in enumerate(input_binary_list, start=1):
        binary = binary
        decimal = int(binary, 2)
        decimal_formatted = f"{decimal:04d}"
        index_num = str(decimal_value).zfill(4)
        word = mnemo.wordlist[decimal]
        index = f"{index_num} - {word}"

        if i == len(input_binary_list):
            row = f"           {i:02d}{' ' * (word_width - 13)}{binary:<{binary_width}}"
            print_list_blue.append(row)
        else:
            row = f"           {i:02d}{' ' * (word_width - 13)}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)
            mnemonic.append(word)

    while True:
        matching_words = [word for binary_word, word in binary_wordlist.items() if binary_word.startswith(last_word_binary)]
        print_list.append("")
        print_list.append(f" Fetching words that start with last word binary input.")
        print_list.append(f" Found {len(matching_words)} word(s) that start with last word binary input.")
        print_list.append(f" Fetching if any of the {len(matching_words)} word(s) has a valid checksum.")

        for word in matching_words:
            temp_matching_word = word
            temp_mnemonic = ' '.join(mnemonic[:]) + ' ' + temp_matching_word
            if is_valid_seed(temp_mnemonic):
                valid_words_list.append(temp_matching_word)

        valid_word_count = len(valid_words_list)

        print_list.append(f" Found {valid_word_count} word(s) with valid checksum, choosing a word to proceed.")

        for word in valid_words_list:
            valid_word = word
            current_mnemonic = ' '.join(mnemonic[:]) + ' ' + valid_word

        if is_valid_seed(current_mnemonic):
            mnemonic.append(valid_word)
            binary = word_to_binary(valid_word, word_list)
            decimal = word_list.index(valid_word) 
            decimal_formatted = f"{decimal:04d}"
            index_num = str(decimal+1).zfill(4)
            index = f"{index_num} - {valid_word}"
            header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index & Word':<{index_width}}"
            print_list_blue.append(header)
            print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))
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
    mnemo = Mnemonic("english")
    word_list = mnemo.wordlist
    binary_wordlist = convert_wordlist_to_binary(word_list)

    num_binary_digits = {12: 7, 15: 6, 18: 5, 21: 4, 24: 3}
    mnemonic = []
    print_list_blue = []  # Create a list to store messages for printing
    print_list = []  # Create a list to store messages for printing
    input_digit_list = []  # Store digits
    input_binary_list = []  # Store binary representations of words
    valid_words_list = []

    bit_checksum = 11 - num_binary_digits[num_words]
    last_word_bit = 11 - bit_checksum           
    mnemonic_bits = (int(num_words) - 1) * 11 + (11 - bit_checksum)           
    total_bits = int(num_words) * 11
    print()
    print_red(f"\n You've chosen to generate a {num_words}-word mnemonic seed phrase."
              f"\n To create a {num_words}-word mnemonic, you need {total_bits} bits of entropy."
              f"\n You need {mnemonic_bits} random dice rolls or coin tosses."
              f"\n The script will calculate the last {bit_checksum} bits for a valid checksum, totaling {total_bits} bits."
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
    header = f"{'           Word #':<{word_width}}{'Dice':<{dice_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index & Word':<{index_width}}"
    print_list_blue.append(header)
    print_list_blue.append("           " + "-" * (word_width + dice_width + binary_width + decimal_width + index_width - 10))

    # Print each row with corresponding dice, decimal, index, and word
    for i, binary in enumerate(input_binary_list, start=1):
        dice = input_digit_list[i - 1]  # Get the corresponding digit from input_digit_list
        binary = binary
        decimal = int(binary, 2)
        decimal_formatted = f"{decimal:04d}"
        word = mnemo.wordlist[decimal]
        index_num = str(decimal+1).zfill(4)
        index = f"{index_num} - {word}"
        if i == len(input_binary_list):
            row = f"           {i:02d}{' ' * (word_width - 13)}{dice:<{dice_width}}{binary:<{binary_width}}"
            print_list_blue.append(row)
        else:
            row = f"           {i:02d}{' ' * (word_width - 13)}{dice:<{dice_width}}{binary:<{binary_width}}{decimal_formatted:<{decimal_width}}{index:<{index_width}}"
            print_list_blue.append(row)
            mnemonic.append(word)

    while True:
        matching_words = [word for binary_word, word in binary_wordlist.items() if binary_word.startswith(last_word_binary)]
        print_list.append("")
        print_list.append(f" Fetching words that start with last word binary input.")
        print_list.append(f" Found {len(matching_words)} word(s) that start with last word binary input.")
        print_list.append(f" Fetching if any of the {len(matching_words)} word(s) has a valid checksum.")

        for word in matching_words:
            temp_matching_word = word
            temp_mnemonic = ' '.join(mnemonic[:]) + ' ' + temp_matching_word
            if is_valid_seed(temp_mnemonic):
                valid_words_list.append(temp_matching_word)

        valid_word_count = len(valid_words_list)

        print_list.append(f" Found {valid_word_count} word(s) with valid checksum, choosing a word to proceed.")

        for word in valid_words_list:
            valid_word = word
            current_mnemonic = ' '.join(mnemonic[:]) + ' ' + valid_word

        if is_valid_seed(current_mnemonic):
            mnemonic.append(valid_word)
            dice = "-"
            binary = word_to_binary(valid_word, word_list)
            decimal = word_list.index(valid_word) 
            decimal_formatted = f"{decimal:04d}"
            index_num = str(decimal+1).zfill(4)
            index = f"{index_num} - {valid_word}"
            header = f"{'           Word #':<{word_width}}{'Dice':<{dice_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index & Word':<{index_width}}"
            print_list_blue.append(header)
            print_list_blue.append("           " + "-" * (word_width + dice_width + binary_width + decimal_width + index_width - 10))
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
