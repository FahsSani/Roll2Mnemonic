from common import *

# Function to get a valid number of child keys between 1 and 25
def get_valid_num_child_keys():
    while True:
        try:
            input_value = input(" Enter the number of child keys to generate for each script type (1-25), leave empty for the default value (5): ")
            if not input_value:
                return 5  # Default to 5 if no value is entered
            num_child_keys = int(input_value)
            if 1 <= num_child_keys <= 25:
                return num_child_keys
            else:
                print(" Invalid input. Please enter a number between 1 and 25 or leave it empty for the default value 5.")
        except ValueError:
            print(" Invalid input. Please enter a number between 1 and 25 or leave it empty for the default value 5.")

# Define constants
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

# Function to generate P2WPKH address
def generate_p2pkh_address(public_key):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(hashlib.sha256(public_key).digest())
    hashed_public_key = ripemd160.digest()

    version = b"\x00"  # P2PKH address starts with '1'
    payload = version + hashed_public_key
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

    # Decode the byte string to a regular string and return it
    return base58.b58encode(payload + checksum).decode()

# Function to generate P2SH-P2WPKH address
def generate_p2sh_p2wpkh_address(public_key):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(hashlib.sha256(public_key).digest())
    hashed_public_key = ripemd160.digest()

    redeem_script = b"\x00\x14" + hashed_public_key  # OP_0 + 20-byte hashed public key
    ripemd160_redeem_script = hashlib.new("ripemd160")
    ripemd160_redeem_script.update(hashlib.sha256(redeem_script).digest())
    hashed_redeem_script = ripemd160_redeem_script.digest()

    version = b"\x05"  # P2SH-P2WPKH address starts with '3'
    payload = version + hashed_redeem_script
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

    return base58.b58encode(payload + checksum).decode()

# Function to generate bech32 address
def generate_bech32_address(public_key):
    witness_version = 0
    witness_program = hashlib.new("ripemd160")
    witness_program.update(hashlib.sha256(public_key).digest())
    hashed_public_key = witness_program.digest()
    hrp = "bc"  # Mainnet prefix for native SegWit addresses
    address = bech32.encode(hrp, witness_version, hashed_public_key)
    return address

# Function to generate taproot address
def generate_taproot_address(public_key_bytes):
    witness_version = 1  # Use 1 for Taproot addresses
    witness_program = hashlib.sha256(public_key_bytes).digest()
    hrp = "bc"  # Your desired prefix for Taproot addresses
    address = bech32.encode(hrp, witness_version, witness_program).decode()

    return address

# Function to generate wif / private key
def generate_wif(private_key, is_compressed=True):
    prefix = b"\x80" if is_compressed else b"\x00"  # 0x80 for compressed, 0x00 for uncompressed
    payload = private_key + (b"\x01" if is_compressed else b"")  # Add 0x01 for compressed keys
    checksum = hashlib.sha256(hashlib.sha256(prefix + payload).digest()).digest()[:4]
    wif = base58.b58encode(prefix + payload + checksum).decode()
    return wif

# Functions to convert xprv and xpub
def decode_xprv_root_key(key):
    decoded_key = base58.b58decode_check(key)
    return decoded_key

def encode_yprv_root_key(key_data):
    yprv_prefix = bytes.fromhex("049d7878")  # Change prefix to '049d7878' for yprv
    encoded_key = base58.b58encode_check(yprv_prefix + key_data)
    return encoded_key.decode()

def encode_zprv_root_key(key_data):
    zprv_prefix = bytes.fromhex("04b2430c")  # Change prefix to '04b2430c' for zprv
    encoded_key = base58.b58encode_check(zprv_prefix + key_data)
    return encoded_key.decode()

def decode_xpub_ext_key(key):
    decoded_key = base58.b58decode_check(key)
    return decoded_key

def encode_ypub_ext_key(key_data):
    ypub_prefix = bytes.fromhex("049d7cb2")  # Change prefix to '049d7cb2' for ypub
    encoded_key = base58.b58encode_check(ypub_prefix + key_data)
    return encoded_key.decode()

def encode_zpub_ext_key(key_data):
    zpub_prefix = bytes.fromhex("04b24746")  # Change prefix to '04b24746' for zpub
    encoded_key = base58.b58encode_check(zpub_prefix + key_data)
    return encoded_key.decode()

# Function to generate Bitcoin addresses
def generate_bitcoin_addresses(seed_phrase, num_child_keys, passphrase=""):
    seed = Mnemonic("english").to_seed(seed_phrase, passphrase=passphrase)
    root_key = BIP32Key.fromEntropy(seed)

    # BIP32 Root Key
    bip39_root_key = root_key.ExtendedKey() #Legacy BIP32 Root Key
    xprv_root_key = bip39_root_key #Legacy BIP32 Root Key
    decoded_key = decode_xprv_root_key(xprv_root_key)
    yprv_root_key = encode_yprv_root_key(decoded_key[4:]) #Native BIP32 Root Key
    zprv_root_key = encode_zprv_root_key(decoded_key[4:]) #Nested BIP32 Root Key

    account_legacy = root_key.ChildKey(44 + 2 ** 31).ChildKey(0 + 2 ** 31).ChildKey(0 + 2 ** 31)
    account_nested = root_key.ChildKey(49 + 2 ** 31).ChildKey(0 + 2 ** 31).ChildKey(0 + 2 ** 31)
    account_native = root_key.ChildKey(84 + 2 ** 31).ChildKey(0 + 2 ** 31).ChildKey(0 + 2 ** 31)
    account_taproot = root_key.ChildKey(86 + 2 ** 31).ChildKey(0 + 2 ** 31).ChildKey(0 + 2 ** 31)
    
    # Account Extended Public Keys xpubs
    legacy_acc_ext_xpub_key = account_legacy.ExtendedKey(private=False)
    nested_acc_ext_xpub_key = account_nested.ExtendedKey(private=False)
    native_acc_ext_xpub_key = account_native.ExtendedKey(private=False)
    taproot_acc_ext_xpub_key = account_taproot.ExtendedKey(private=False)

    # Account Extended Public Keys ypubs
    decoded_key = decode_xpub_ext_key(nested_acc_ext_xpub_key)
    nested_acc_ext_ypub_key = encode_ypub_ext_key(decoded_key[4:])

    # Account Extended Public Keys zpubs
    decoded_key = decode_xpub_ext_key(native_acc_ext_xpub_key)
    native_acc_ext_zpub_key = encode_zpub_ext_key(decoded_key[4:])
    
    addresses = {
        "LegacyR": [],
        "LegacyC": [],
        "Nested SegWitR": [],
        "Nested SegWitC": [],
        "Native SegWitR": [],
        "Native SegWitC": [],
        "TaprootR": [],
        "TaprootC": [],
        "Legacy xprv": xprv_root_key,
        "Legacy xpub": legacy_acc_ext_xpub_key,
        "Nested yprv": yprv_root_key,
        "Nested xpub": nested_acc_ext_xpub_key,
        "Nested ypub": nested_acc_ext_ypub_key,
        "Native zprv": zprv_root_key,
        "Native xpub": native_acc_ext_xpub_key,
        "Native zpub": native_acc_ext_zpub_key,
        "Taproot xprv": xprv_root_key,
        "Taproot xpub": taproot_acc_ext_xpub_key,
    }

    for x in range(num_child_keys):
        # Generate addresses for the specified number of child keys
        address_key_legacyR = account_legacy.ChildKey(0).ChildKey(x)
        address_key_legacyC = account_legacy.ChildKey(1).ChildKey(x)
        address_key_nestedR = account_nested.ChildKey(0).ChildKey(x)
        address_key_nestedC = account_nested.ChildKey(1).ChildKey(x)
        address_key_nativeR = account_native.ChildKey(0).ChildKey(x)
        address_key_nativeC = account_native.ChildKey(1).ChildKey(x)
        address_key_taprootR = account_taproot.ChildKey(0).ChildKey(x)
        address_key_taprootC = account_taproot.ChildKey(1).ChildKey(x)

        #WIF / Private Keys
        LegacyWIFR = generate_wif(address_key_legacyR.PrivateKey())
        LegacyWIFC = generate_wif(address_key_legacyC.PrivateKey())
        NestedWIFR = generate_wif(address_key_nestedR.PrivateKey())
        NestedWIFC = generate_wif(address_key_nestedC.PrivateKey())
        NativeWIFR = generate_wif(address_key_nativeR.PrivateKey())
        NativeWIFC = generate_wif(address_key_nativeC.PrivateKey())
        TaprootWIFR = generate_wif(address_key_taprootR.PrivateKey())
        TaprootWIFC = generate_wif(address_key_taprootC.PrivateKey())

        #Get pubic addresses
        LegacyR = generate_p2pkh_address(address_key_legacyR.PublicKey())
        LegacyC = generate_p2pkh_address(address_key_legacyC.PublicKey())
        NestedR = generate_p2sh_p2wpkh_address(address_key_nestedR.PublicKey())
        NestedC = generate_p2sh_p2wpkh_address(address_key_nestedC.PublicKey())
        NativeR = generate_bech32_address(address_key_nativeR.PublicKey())
        NativeC = generate_bech32_address(address_key_nativeC.PublicKey())

        #Get Taproot Addresses
        setup("mainnet")
        TaprootR = PrivateKey(TaprootWIFR).get_public_key().get_taproot_address().to_string()
        TaprootC = PrivateKey(TaprootWIFC).get_public_key().get_taproot_address().to_string()

        #Append addresses & WIFs to addresses lists
        addresses["LegacyR"].append((LegacyR, LegacyWIFR))
        addresses["LegacyC"].append((LegacyC, LegacyWIFC))
        addresses["Nested SegWitR"].append((NestedR, NestedWIFR))
        addresses["Nested SegWitC"].append((NestedC, NestedWIFC))
        addresses["Native SegWitR"].append((NativeR, NativeWIFR))
        addresses["Native SegWitC"].append((NativeC, NativeWIFC))
        addresses["TaprootR"].append((TaprootR, TaprootWIFR))
        addresses["TaprootC"].append((TaprootC, TaprootWIFC))

    return addresses, bip39_root_key

# Function to generate wallets
def generate_wallet(seed_phrase):
    passphrase = input(" Enter an optional passphrase or leave empty for none: ").strip()
    num_child_keys = get_valid_num_child_keys()  # Ask for the number of child keys
    seed = Mnemonic("english").to_seed(seed_phrase, passphrase=passphrase)  # Include passphrase
    hex_seed = binascii.hexlify(seed).decode('utf-8')

    # Format Information box
    childkeys_info = f"Child Keys          : {num_child_keys:,.0f}"
    creator_info = f"Created By          : Sani Fahs"
    twitter_info = f"Twitter             : @SaniExp"
    github_info = f"GitHub              : https://github.com/FahsSani"
    lightning_info = f"Lightning Donations : sani@walletofsatoshi.com"
    max_info_length = max( len(childkeys_info),len(creator_info), len(twitter_info),len(github_info), len(lightning_info))
    box_width = max_info_length + 4  # Adjust the box width based on the max info length
    info_box = " " + "+" + "-" * (box_width - 2) + "+"
    info_box += f"\n | {childkeys_info.ljust(max_info_length)} |"
    info_box += f"\n | {creator_info.ljust(max_info_length)} |"
    info_box += f"\n | {twitter_info.ljust(max_info_length)} |"
    info_box += f"\n | {github_info.ljust(max_info_length)} |"
    info_box += f"\n | {lightning_info.ljust(max_info_length)} |"
    info_box += "\n +" + "-" * (box_width - 2) + "+"

    bitcoin_addresses, bip39_root_key = generate_bitcoin_addresses(seed_phrase, num_child_keys, passphrase=passphrase)

    # Clear terminal
    clear_terminal()
    
    # Print title
    text3 = "* ROLL   TO   MNEMONIC *"
    print_centered_art_text(text3,5)

    # Print data
    print_bright_orange(info_box)
    print()
    print_red(" Mnemonic Seed Phrase:", seed_phrase)
    print_red(" Passphrase          :", passphrase)
    print_red(" Seed Hex            :", hex_seed)
    print()
    print_blue(" Script Type - Legacy (P2SH):")
    print_green(f"   Root Key  : {bitcoin_addresses['Legacy xprv']}")
    print_green(f"   Public Key: {bitcoin_addresses['Legacy xpub']}")
    print_purple("     Receive Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(39), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 112)
    for index, (address, wif) in enumerate(bitcoin_addresses["LegacyR"]):
        path = f" m/44'/0'/0'/0/{index}".ljust(17)
        address = address.ljust(36)
        print(f"      {path}    {address}    {wif}")
    print()
    print_purple("     Change Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(39), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 112)
    for index, (address, wif) in enumerate(bitcoin_addresses["LegacyC"]):
        path = f" m/44'/0'/0'/1/{index}".ljust(17)
        address = address.ljust(36)
        print(f"      {path}    {address}    {wif}")
    print()
    print()
    print_blue(" Script Type - Nested SegWit (P2SH-P2WSH):")
    print_green(f"   Root Key  : {bitcoin_addresses['Nested yprv']}")
    print_green(f"   Public Key: {bitcoin_addresses['Nested xpub']}")
    print_green(f"   Public Key: {bitcoin_addresses['Nested ypub']}")
    print_purple("     Receive Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(39), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 112)
    for index, (address, wif) in enumerate(bitcoin_addresses["Nested SegWitR"]):
        path = f" m/49'/0'/0'/0/{index}".ljust(17)
        address = address.ljust(36)
        print(f"      {path}    {address}    {wif}")
    print()
    print_purple("     Change Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(39), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 112)
    for index, (address, wif) in enumerate(bitcoin_addresses["Nested SegWitC"]):
        path = f" m/49'/0'/0'/1/{index}".ljust(17)
        address = address.ljust(36)
        print(f"      {path}    {address}    {wif}")
    print()
    print()
    print_blue(" Script Type - Native SegWit (P2WSH):")
    print_green(f"   Root Key  : {bitcoin_addresses['Native zprv']}")
    print_green(f"   Public Key: {bitcoin_addresses['Native xpub']}")
    print_green(f"   Public Key: {bitcoin_addresses['Native zpub']}")
    print_purple("     Receive Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(47), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 120)
    for index, (address, wif) in enumerate(bitcoin_addresses["Native SegWitR"]):
        path = f" m/84'/0'/0'/0/{index}".ljust(17)
        address = address.ljust(44)
        print(f"      {path}    {address}    {wif}")
    print()
    print_purple("     Change Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(47), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 120)
    for index, (address, wif) in enumerate(bitcoin_addresses["Native SegWitC"]):
        path = f" m/84'/0'/0'/1/{index}".ljust(17)
        address = address.ljust(44)
        print(f"      {path}    {address}    {wif}")
    print()
    print()
    print_blue(" Script Type - Taproot (P2TR):")
    print_green(f"   Root Key  : {bitcoin_addresses['Taproot xprv']}")
    print_green(f"   Public Key: {bitcoin_addresses['Taproot xpub']}")
    print_purple("     Receive Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(67), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 140)
    for index, (address, wif) in enumerate(bitcoin_addresses["TaprootR"]):
        path = f" m/86'/0'/0'/0/{index}".ljust(17)
        address = address.ljust(64)
        print(f"      {path}    {address}    {wif}")
    print()
    print_purple("     Change Addresses:")
    print_Cyan("       Derivation Path".ljust(26), "Bitcoin Address".ljust(67), "Private Key / WIF (Wallet Import Format)")
    print_Cyan(" " + "      " + "-" * 140)
    for index, (address, wif) in enumerate(bitcoin_addresses["TaprootC"]):
        path = f" m/86'/0'/0'/0/{index}".ljust(17)
        address = address.ljust(64)
        print(f"      {path}    {address}    {wif}")
    print()
    print()
    print(" You can verify the data using the following link: https://iancoleman.io/bip39/")
    print()
    print()
