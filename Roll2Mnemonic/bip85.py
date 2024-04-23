from Roll2Mnemonic.common import *

def _decorate_path(path):
    return path.replace("m/", "").replace("'", "p")

def _get_k_from_node(node):
    return to_bytes_32(node.secret_exponent())

def _hmac_sha512(message_k):
    return hmac.new(key=b'bip-entropy-from-k', msg=message_k, digestmod=hashlib.sha512).digest()

def _derive_k(path, xprv):
    path = _decorate_path(path)
    node = xprv.subkey_for_path(path)
    return _get_k_from_node(node)

def bip32_xprv_to_entropy(path, xprv_string):
    xprv = BTC.parse(xprv_string)
    if xprv is None:
        raise ValueError('ERROR: Invalid xprv')
    return _hmac_sha512(_derive_k(path, xprv))

def derive_child_key(xprv_string, words, index):
    path = f"83696968p/39p/0p/{words}p/{index}p"

    entropy = bip32_xprv_to_entropy(path, xprv_string)

    m = Mnemonic("english")
    return m.to_mnemonic(entropy[: words * 4 // 3])

def bip85_generator(parent_seed_phrase, parent_passphrase, num_words, index_type, index_specific, indices_start, indices_end):
    child_indices = []
    parent_bip39_seed = bip39.to_seed(parent_seed_phrase, passphrase=parent_passphrase)
    parent_bip32_root_key = BTC.keys.bip32_seed(parent_bip39_seed).hwif(as_private=True)
    
    try:
        if index_type == 'Specific':
            index = int(index_specific)
            if 0 <= index <= 2147483647:
                child_indices = [index]
            else:
                return " Index must be between 0 and 2,147,483,647."
            
        elif index_type == 'Range':
            start_index = int(indices_start)
            end_index = int(indices_end)

            if 0 <= start_index <= end_index <= 2147483647:
                child_indices = list(range(start_index, end_index + 1))
            else:
                return "\nInvalid range. Both start and end indices must be between 0 and 2,147,483,647." \
                               "\nStart index should be less than or equal to the end index."                

    except Exception as e:
        return "Invalid index, only integers are allowed."

    print_red(f" Parent Mnemonic Seed Phrase: {parent_seed_phrase}")
    print_red(f" Parent Passphrase          : {parent_passphrase}")
    print_red(f" Parent BIP39 Seed          : {binascii.hexlify(parent_bip39_seed).decode('utf-8')}")
    print_red(f" Parent BIP32 Root Key      : {parent_bip32_root_key}")
    for index in child_indices:
        child_key = derive_child_key(parent_bip32_root_key, num_words, index)
        print()
        print_blue(f"  BIP85 Index Number: {index:,.0f}")
        print_blue(f"  BIP85 Child Key   : {child_key}")

    print()
    print()
    print_red(" To verify the data above, visit: https://iancoleman.io/bip39/")
    print()

    return "BIP85 Child Keys have Been Generated Successfully."
