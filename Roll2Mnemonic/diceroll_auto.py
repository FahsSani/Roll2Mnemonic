from Roll2Mnemonic.common import *

# Define fixed widths for each column in headers
word_width = 25
dice_width = 15
binary_width = 15
decimal_width = 15
index_width = 18

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

def roll_dice(n, num_rolls):  # n is the dice side numbers, num_rolls how many times to roll each number
    auto_dice_list = []
    auto_dice = [random.randint(1, n) for _ in range(num_rolls)] 
    auto_dice_list.append(auto_dice)
    return auto_dice_list

def dr_auto(num_words):
    while True:
        mnemo = Mnemonic("english")
        word_list = mnemo.wordlist
        binary_wordlist = convert_wordlist_to_binary(word_list)
        num_binary_digits = {12: 7, 15: 6, 18: 5, 21: 4, 24: 3}

        # Create a list to store messages for printing
        mnemonic = []
        print_list_blue = [] 
        print_list = []  
        valid_words_list = []
        
        # Append the header row
        header = f"{'           Word #':<{word_width}}{'Binary':<{binary_width}}{'Decimal':<{decimal_width}}{'Index & Word':<{index_width}}"
        print_list_blue.append(header)
        print_list_blue.append("           " + "-" * (word_width + binary_width + decimal_width + index_width - 10))

        for i in range(1, num_words):
            numeric_list = []
            for x in range(0, 11):
                start = random.choice(random.choice(roll_dice(10000, 1000)))
                numeric_list.append(start)
            binary_digits = [1 if num % 2 == 0 else 0 for num in numeric_list]  # odd numbers are converted 0, even numbers are converted 1  
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

        numeric_list = []
        for x in range(0, num_binary_digits[num_words]):
            start = random.choice(random.choice(roll_dice(10000, 10)))
            numeric_list.append(start)
        binary_digits = [1 if num % 2 == 0 else 0 for num in numeric_list]  # odd numbers are converted 0, even numbers are converted 1  
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
                      f"\n For each bit in the {mnemonic_bits} bits, a 10,000-sided dice will be rolled 1,000 times and the results will be stored in a special list."
                      f"\n Subsequently, for each bit a random number will be selected from the list and transformed into 0 if it's odd or 1 if it's even.")
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
