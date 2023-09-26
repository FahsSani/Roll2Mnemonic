from common import *

# Function to generate P2SH-P2WPKH address
def generate_p2sh_p2wpkh_address(public_key):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(hashlib.sha256(public_key).digest())
    hashed_public_key = ripemd160.digest()

    redeem_script = b"\x00\x14" + hashed_public_key  # OP_0 + 20-byte hashed public key
    ripemd160_redeem_script = hashlib.new("ripemd160")
    ripemd160_redeem_script.update(hashlib.sha256(redeem_script).digest())
    hashed_redeem_script = ripemd160_redeem_script.digest()

    version = b"\xc4"  # P2SH-P2WPKH address starts with '2' on testnet
    payload = version + hashed_redeem_script
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

    return base58.b58encode(payload + checksum).decode()

# Functions to convert tprv and tpub
def decode_tprv_root_key(key):
    decoded_key = base58.b58decode_check(key)
    return decoded_key

def encode_uprv_root_key(key_data):
    uprv_prefix = bytes.fromhex("044a4e28")  # Change prefix to '044a4e28' for uprv
    encoded_key = base58.b58encode_check(uprv_prefix + key_data)
    return encoded_key.decode()

def encode_vprv_root_key(key_data):
    vprv_prefix = bytes.fromhex("045f18bc")  # Change prefix to '045f18bc' for vprv
    encoded_key = base58.b58encode_check(vprv_prefix + key_data)
    return encoded_key.decode()

def decode_tpub_ext_key(key):
    decoded_key = base58.b58decode_check(key)
    return decoded_key

def encode_upub_ext_key(key_data):
    upub_prefix = bytes.fromhex("044a5262")  # Change prefix to '044a5262' for upub
    encoded_key = base58.b58encode_check(upub_prefix + key_data)
    return encoded_key.decode()

def encode_vpub_ext_key(key_data):
    vpub_prefix = bytes.fromhex("045f1cf6")  # Change prefix to '045f1cf6' for vpub
    encoded_key = base58.b58encode_check(vpub_prefix + key_data)
    return encoded_key.decode()

# Function to generate Bitcoin testnet addresses
def generate_testnet_addresses(seed_phrase, num_child_keys, passphrase):
    seed = Mnemonic("english").to_seed(seed_phrase, passphrase)
    root_key = BIP32Key.fromEntropy(seed, testnet=True)  # Use testnet=True

    # BIP32 Root Key
    bip39_root_key = root_key.ExtendedKey()  # Legacy BIP32 Root Key
    tprv_root_key = bip39_root_key  # Legacy BIP32 Root Key
    decoded_key = decode_tprv_root_key(tprv_root_key)
    uprv_root_key = encode_uprv_root_key(decoded_key[4:])  # Native BIP32 Root Key
    vprv_root_key = encode_vprv_root_key(decoded_key[4:])  # Nested BIP32 Root Key

    account_legacy = root_key.ChildKey(44 + 2 ** 31).ChildKey(1 + 2 ** 31).ChildKey(0 + 2 ** 31)  
    account_nested = root_key.ChildKey(49 + 2 ** 31).ChildKey(1 + 2 ** 31).ChildKey(0 + 2 ** 31)  
    account_native = root_key.ChildKey(84 + 2 ** 31).ChildKey(1 + 2 ** 31).ChildKey(0 + 2 ** 31) 
    account_taproot = root_key.ChildKey(86 + 2 ** 31).ChildKey(1 + 2 ** 31).ChildKey(0 + 2 ** 31)

    # Account Extended Public Keys tpubs
    legacy_acc_ext_tpub_key = account_legacy.ExtendedKey(private=False)
    nested_acc_ext_tpub_key = account_nested.ExtendedKey(private=False)
    native_acc_ext_tpub_key = account_native.ExtendedKey(private=False)
    taproot_acc_ext_tpub_key = account_taproot.ExtendedKey(private=False)

    # Account Extended Public Keys upubs
    decoded_key = decode_tpub_ext_key(nested_acc_ext_tpub_key)
    nested_acc_ext_upub_key = encode_upub_ext_key(decoded_key[4:])

    # Account Extended Public Keys vpubs
    decoded_key = decode_tpub_ext_key(native_acc_ext_tpub_key)
    native_acc_ext_vpub_key = encode_vpub_ext_key(decoded_key[4:])

    addresses = {
        "Legacy (P2PKH)R": [],
        "Legacy (P2PKH)C": [],
        "Nested SegWit (P2SH-P2WPKH)R": [],
        "Nested SegWit (P2SH-P2WPKH)C": [],
        "Native SegWit (P2WPKH)R": [],
        "Native SegWit (P2WPKH)C": [],
        "Taproot (P2TR)R": [],
        "Taproot (P2TR)C": [],
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

        # WIF / Private Keys
        LegacyWIFR = address_key_legacyR.WalletImportFormat()
        LegacyWIFC = address_key_legacyC.WalletImportFormat()
        NestedWIFR = address_key_nestedR.WalletImportFormat()
        NestedWIFC = address_key_nestedC.WalletImportFormat()
        NativeWIFR = address_key_nativeR.WalletImportFormat()
        NativeWIFC = address_key_nativeC.WalletImportFormat()
        TaprootWIFR = address_key_taprootR.WalletImportFormat()
        TaprootWIFC = address_key_taprootC.WalletImportFormat()

        # Pubic addresses
        setup("testnet")  # Use testnet setup
        LegacyR = PrivateKey(LegacyWIFR).get_public_key().get_address().to_string()
        LegacyC = PrivateKey(LegacyWIFC).get_public_key().get_address().to_string()
        NestedR = generate_p2sh_p2wpkh_address(address_key_nestedR.PublicKey())
        NestedC = generate_p2sh_p2wpkh_address(address_key_nestedC.PublicKey())
        NativeR = PrivateKey(NativeWIFR).get_public_key().get_segwit_address().to_string()
        NativeC = PrivateKey(NativeWIFC).get_public_key().get_segwit_address().to_string()
        TaprootR = PrivateKey(TaprootWIFR).get_public_key().get_taproot_address().to_string()
        TaprootC = PrivateKey(TaprootWIFC).get_public_key().get_taproot_address().to_string()

        # Append keys, addresses & WIFs to addresses lists
        addresses["Legacy (P2PKH)R"].append((tprv_root_key, legacy_acc_ext_tpub_key, "", "44", LegacyR, LegacyWIFR))
        addresses["Legacy (P2PKH)C"].append(("44", LegacyC, LegacyWIFC))
        addresses["Nested SegWit (P2SH-P2WPKH)R"].append((uprv_root_key, nested_acc_ext_tpub_key, nested_acc_ext_upub_key, "49", NestedR, NestedWIFR))
        addresses["Nested SegWit (P2SH-P2WPKH)C"].append(("49", NestedC, NestedWIFC))
        addresses["Native SegWit (P2WPKH)R"].append((vprv_root_key, native_acc_ext_tpub_key, native_acc_ext_vpub_key, "84", NativeR, NativeWIFR))
        addresses["Native SegWit (P2WPKH)C"].append(("84", NativeC, NativeWIFC))
        addresses["Taproot (P2TR)R"].append((tprv_root_key, taproot_acc_ext_tpub_key, "", "86", TaprootR, TaprootWIFR))
        addresses["Taproot (P2TR)C"].append(("86", TaprootC, TaprootWIFC))

    return addresses, bip39_root_key

def print_address_details(script_type, addresses):
    print()
    print()

    if script_type == "Legacy (P2PKH)":
        print_bright_orange(" BITCOIN - TESTNET:")
        print_bright_orange(" " + "-" * 18)
        
    print_blue(f"   Script Type - {script_type}:")

    # Extract root key and extended public keys
    rootkey, extpubkey1, extpubkey2, *_ = addresses[f'{script_type}R'][0]

    print_green(f"     BIP32 Root Key    : {rootkey}")
    print_green(f"     Acc. Ext. Pub. Key: {extpubkey1}")
    if extpubkey2 != "":
        print_green(f"     Acc. Ext. Pub. Key: {extpubkey2}")

    format_info = {
        "Legacy (P2PKH)": (38, 111),
        "Nested SegWit (P2SH-P2WPKH)": (38, 111),
        "Native SegWit (P2WPKH)": (46, 119),
        "Taproot (P2TR)": (66, 139)
    }

    if script_type in format_info:
        address_width, line_width = format_info[script_type]
        header_template = f"         Derivation Path".ljust(28)
        address_template = "Bitcoin Address".ljust(address_width)
        wif_template = "Private Key / WIF (Wallet Import Format)"

        print_purple("       Receive Addresses:")
        print_cyan(f"{header_template} {address_template} {wif_template}")
        print_cyan(f"         " + "-" * line_width)

        for index, (rootkey, extpubkey1, extpubkey2, BIP, address, wif) in enumerate(addresses[f'{script_type}R']):
            path = f" m/{BIP}'/1'/0'/0/{index}".ljust(20)
            address = address.ljust(address_width)
            print(f"        {path} {address} {wif}")

        print()
        print_purple("       Change Addresses:")
        print_cyan(f"{header_template} {address_template} {wif_template}")
        print_cyan(f"         " + "-" * line_width)

        for index, (BIP, address, wif) in enumerate(addresses[f'{script_type}C']):
            path = f" m/{BIP}'/1'/0'/1/{index}".ljust(20)
            address = address.ljust(address_width)
            print(f"        {path} {address} {wif}")

# Function to generate testnet wallets
def generate_testnet_wallet(seed_phrase, num_child_keys, passphrase):
    if is_valid_seed(seed_phrase): #Recheck if the mnemonic seed phrase is valid
        seed = Mnemonic("english").to_seed(seed_phrase, passphrase=passphrase)
        hex_seed = binascii.hexlify(seed).decode('utf-8')

        # Format Information box
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

        addresses, bip39_root_key = generate_testnet_addresses(seed_phrase, num_child_keys, passphrase=passphrase)

        # Clear terminal
        clear_terminal()

        # Print title
        text3 = "* ROLL   TO   MNEMONIC *"
        print_centered_art_text(text3, 5, "Standard")

        # Print data
        print_bright_orange(info_box)
        print()
        print_red(" Mnemonic Seed Phrase:", seed_phrase)
        print_red(" Passphrase          :", passphrase)
        print_red(" BIP39 Seed Hex      :", hex_seed)

        for script_type in ["Legacy (P2PKH)", "Nested SegWit (P2SH-P2WPKH)", "Native SegWit (P2WPKH)", "Taproot (P2TR)"]:
            print_address_details(script_type, addresses)

        print()
        print_red(" To verify the mnemonic seed phrase, keys and addresses, visit: https://iancoleman.io/bip39/")
        print()     
