from Roll2Mnemonic.common import *

# Function to generate P2SH-P2WPKH address
def generate_p2sh_p2wpkh_address(public_key):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(hashlib.sha256(public_key).digest())
    hashed_public_key = ripemd160.digest()

    redeem_script = b"\x00\x14" + hashed_public_key
    ripemd160_redeem_script = hashlib.new("ripemd160")
    ripemd160_redeem_script.update(hashlib.sha256(redeem_script).digest())
    hashed_redeem_script = ripemd160_redeem_script.digest()

    version = b"\x05"  
    payload = version + hashed_redeem_script
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

    return base58.b58encode(payload + checksum).decode()

# Functions to convert xprv and xpub
def decode_xprv_root_key(key):
    decoded_key = base58.b58decode_check(key)
    return decoded_key

def encode_yprv_root_key(key_data):
    yprv_prefix = bytes.fromhex("049d7878")  
    encoded_key = base58.b58encode_check(yprv_prefix + key_data)
    return encoded_key.decode()

def encode_zprv_root_key(key_data):
    zprv_prefix = bytes.fromhex("04b2430c")  
    encoded_key = base58.b58encode_check(zprv_prefix + key_data)
    return encoded_key.decode()

def decode_xpub_ext_key(key):
    decoded_key = base58.b58decode_check(key)
    return decoded_key

def encode_ypub_ext_key(key_data):
    ypub_prefix = bytes.fromhex("049d7cb2")  
    encoded_key = base58.b58encode_check(ypub_prefix + key_data)
    return encoded_key.decode()

def encode_zpub_ext_key(key_data):
    zpub_prefix = bytes.fromhex("04b24746") 
    encoded_key = base58.b58encode_check(zpub_prefix + key_data)
    return encoded_key.decode()

# Function to generate Bitcoin addresses
def generate_mainnet_addresses(seed_phrase, num_child_keys, passphrase):
    seed = Mnemonic("english").to_seed(seed_phrase, passphrase)
    root_key = BIP32Key.fromEntropy(seed)

    # BIP32 Root Key
    bip39_root_key = root_key.ExtendedKey()  
    xprv_root_key = bip39_root_key 
    decoded_key = decode_xprv_root_key(xprv_root_key)
    yprv_root_key = encode_yprv_root_key(decoded_key[4:]) 
    zprv_root_key = encode_zprv_root_key(decoded_key[4:])  

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

        # Public Keys
        setup("mainnet")
        LegacyPKR = PrivateKey(LegacyWIFR).get_public_key().to_hex(compressed=True)
        LegacyPKC = PrivateKey(LegacyWIFC).get_public_key().to_hex(compressed=True)
        NestedPKR = binascii.hexlify(address_key_nestedR.PublicKey()).decode('utf-8')
        NestedPKC = binascii.hexlify(address_key_nestedC.PublicKey()).decode('utf-8')
        NativePKR = PrivateKey(NativeWIFR).get_public_key().to_hex(compressed=True)
        NativePKC = PrivateKey(NativeWIFC).get_public_key().to_hex(compressed=True)
        TaprootPKR = PrivateKey(TaprootWIFR).get_public_key().to_hex(compressed=True)
        TaprootPKC = PrivateKey(TaprootWIFC).get_public_key().to_hex(compressed=True)

        # Pubic addresses
        LegacyAddR = PublicKey(LegacyPKR).get_address().to_string()
        LegacyAddC = PublicKey(LegacyPKC).get_address().to_string()
        NestedAddR = generate_p2sh_p2wpkh_address(address_key_nestedR.PublicKey())  
        NestedAddC = generate_p2sh_p2wpkh_address(address_key_nestedC.PublicKey())  
        NativeAddR = PublicKey(NativePKR).get_segwit_address().to_string()
        NativeAddC = PublicKey(NativePKC).get_segwit_address().to_string()
        TaprootAddR = PublicKey(TaprootPKR).get_taproot_address().to_string()
        TaprootAddC = PublicKey(TaprootPKC).get_taproot_address().to_string()

        # Append keys, addresses & WIFs to addresses lists
        addresses["Legacy (P2PKH)R"].append((xprv_root_key, legacy_acc_ext_xpub_key, "", "44", LegacyAddR, LegacyPKR, LegacyWIFR))
        addresses["Legacy (P2PKH)C"].append(("44", LegacyAddC, LegacyPKC, LegacyWIFC))
        addresses["Nested SegWit (P2SH-P2WPKH)R"].append((yprv_root_key, nested_acc_ext_xpub_key, nested_acc_ext_ypub_key, "49", NestedAddR, NestedPKR, NestedWIFR))
        addresses["Nested SegWit (P2SH-P2WPKH)C"].append(("49", NestedAddC, NestedPKC, NestedWIFC))
        addresses["Native SegWit (P2WPKH)R"].append((zprv_root_key, native_acc_ext_xpub_key, native_acc_ext_zpub_key, "84", NativeAddR, NativePKR, NativeWIFR))
        addresses["Native SegWit (P2WPKH)C"].append(("84", NativeAddC, NativePKC, NativeWIFC))
        addresses["Taproot (P2TR)R"].append((xprv_root_key, taproot_acc_ext_xpub_key, "", "86", TaprootAddR, TaprootPKR, TaprootWIFR))
        addresses["Taproot (P2TR)C"].append(("86", TaprootAddC, TaprootPKC, TaprootWIFC))

    return addresses, bip39_root_key

def print_address_details(script_type, addresses, is_full):
    print()
    print()
    
    if script_type == "Legacy (P2PKH)":
        print_bright_orange(" BITCOIN - MAINNET:")
        print_bright_orange(" " + "-" * 18)
        
    print_blue(f"   Script Type - {script_type}:")

    # Extract root key and extended public keys
    rootkey, extpubkey1, extpubkey2, *_ = addresses[f'{script_type}R'][0]

    print_green(f"     BIP32 Root Key    : {rootkey}")
    print_green(f"     Acc. Ext. Pub. Key: {extpubkey1}")
    if extpubkey2 != "":
        print_green(f"     Acc. Ext. Pub. Key: {extpubkey2}")

    format_info = {
        "Legacy (P2PKH)": (37, 111) if not is_full else (38, 182),
        "Nested SegWit (P2SH-P2WPKH)": (37, 111) if not is_full else (38, 182),
        "Native SegWit (P2WPKH)": (45, 119) if not is_full else (46, 190),
        "Taproot (P2TR)": (65, 139) if not is_full else (66, 210)
    }

    if script_type in format_info:
        address_width, line_width = format_info[script_type]           
        header_template = f"         Derivation Path".ljust(28)
        address_template = "Bitcoin Address".ljust(address_width)
        wif_template = "Private Key / WIF (Wallet Import Format)"
        pk_template = "Public Key".ljust(70) if is_full else ""

        print_purple("       Receive Addresses:")
        print_cyan(f"{header_template} {address_template} {pk_template} {wif_template}")
        print_cyan(f"         " + "-" * line_width)

        for index, (rootkey, extpubkey1, extpubkey2, BIP, address, PK, wif) in enumerate(addresses[f'{script_type}R']):
            path = f" m/{BIP}'/0'/0'/0/{index}".ljust(20)
            address = address.ljust(address_width)
            pk = PK.ljust(70) if is_full else ""        
            print(f"        {path} {address} {pk} {wif}")

        print()
        print_purple("       Change Addresses:")
        print_cyan(f"{header_template} {address_template} {pk_template} {wif_template}")
        print_cyan(f"         " + "-" * line_width)

        for index, (BIP, address, PK, wif) in enumerate(addresses[f'{script_type}C']):
            path = f" m/{BIP}'/0'/0'/1/{index}".ljust(20)
            address = address.ljust(address_width)
            pk = PK.ljust(70) if is_full else ""        
            print(f"        {path} {address} {pk} {wif}")

# Function to generate wallets
def generate_mainnet_wallet(seed_phrase, num_child_keys, passphrase, list_type):
    if is_valid_seed(seed_phrase): 
        seed = Mnemonic("english").to_seed(seed_phrase, passphrase=passphrase)
        hex_seed = binascii.hexlify(seed).decode('utf-8')

        addresses, bip39_root_key = generate_mainnet_addresses(seed_phrase, num_child_keys, passphrase=passphrase)

        print_red(f"\n Mnemonic Seed Phrase: {seed_phrase}")
        print_red(f" Passphrase          : {passphrase}")
        print_red(" BIP39 Seed Hex      :", hex_seed)

        for script_type in ["Legacy (P2PKH)", "Nested SegWit (P2SH-P2WPKH)", "Native SegWit (P2WPKH)", "Taproot (P2TR)"]:
            if list_type == "AddMain":
                print_address_details(script_type, addresses, is_full=False)
            else:
                print_address_details(script_type, addresses, is_full=True)
        print()
        print()
        print_red(" To verify the data above, visit: https://iancoleman.io/bip39/")
        print()
