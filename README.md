Table Of Contents
=================
1. [Roll2Mnemonic](#roll2mnemonic)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Online Usage](#online-usage)
6. [Offline Usage](#offline-usage)
7. [Demo Video](#demo-video)
8. [Support and Feedback](#support-and-feedback)
9. [Donations](#donations)
10. [Disclaimer](#disclaimer)
11. [License](#license)

# Roll2Mnemonic

This multifaceted tool empowers you to effortlessly create secure mnemonic seed phrases using either manual dice rolls, coin tosses or seed phrases. It then goes a step further by generating corresponding private keys and public addresses for all available Bitcoin script types. Whether you prefer manual or automated methods, this tool has you covered.

## Features

- **Dice Roll To Mnemonic:**
    1. Physical Dice or Coin Toss: You have the flexibility to roll physical dice or conduct a coin toss and input the resulting data as either binary (1 or 0) or numbers (1 to 6). This method ensures absolute randomness for generating your mnemonic seed phrase.
    2. Dice Roll From Entropy: For a quicker approach, the program can generate random dice rolls for you. The automated dice roll function guarantees the essential randomness needed for a secure seed phrase.
    3. Mnemonic Seed Generation: After collecting the dice roll data, the program seamlessly proceeds to generate a valid checksum and creates a BIP39 mnemonic seed phrase. This seed phrase forms the cornerstone for generating Bitcoin private keys and public addresses.
    4. Mnemonic Code Converter: The generated mnemonic seed phrase is then processed through the Mnemonic Code Converter, capable of generating BIP39 private keys and public addresses for all script types: Legacy (P2PKH), Nested SegWit (P2SH-P2WPKH), Native SegWit (P2WPKH), and Taproot (P2TR).
- **Seed To Mnemonic:**
    1. Generate Hex Seed From Entropy: The program can generate a Hex seed from entropy. The automated function guarantees the essential randomness required for secure seed generation.
    2. Mnemonic Seed Generation: After collecting the Hex seed, the program seamlessly proceeds to generate a valid checksum and creates a BIP39 mnemonic seed phrase.
    3. Own Mnemonic Seed Phrase: You have the option to enter your own mnemonic seed phrase into the program.
    4. Mnemonic Code Converter: The generated mnemonic seed phrase is then processed through the Mnemonic Code Converter, capable of generating BIP39 private keys and public addresses for all script types: Legacy (P2PKH), Nested SegWit (P2SH-P2WPKH), Native SegWit (P2WPKH), and Taproot (P2TR).
- **QR Code Generator:** A built in QR code generator from text.


## Prerequisites

Before using the Mnemonic Code Converter, ensure you have the following prerequisites installed on your system:

- Python 3.11.x
- Required Python libraries: Mnemonic, bip32utils, base58, bech32, in addition to more libraries which can be found in requirements.txt


## Installation

You can clone this repository to your local machine using the following method:

### HTTPS

To clone the repository using HTTPS, open your terminal or command prompt and run the following command:

```bash
git clone https://github.com/FahsSani/Roll2Mnemonic.git
```

### Direct Download 

Download and extract the following file:

```bash
https://github.com/FahsSani/Roll2Mnemonic/archive/refs/heads/main.zip
```


## Online Usage

Follow these steps to use the Roll2Mnemonic:

1. Clone or download this repository to your local machine.
2. Ensure you have Python 3.11.x  or above installed.
3. Install the necessary Python libraries listed in requirements.txt
4. Launch start.py to initiate the code.


## Offline Usage:

To set up Python in an offline environment you must download the packages by using an internet-enabled computer, and then transfer the files to the offline computer.
Ensure target machine is the same architecture, OS, and Python version as the original device.

1. Download latest version of python from:

```bash
https://www.python.org/downloads/
```

2. Download latest version of pip, if you don't have it on ur current computer or offline computer and follow instructions from:

```bash
https://pip.pypa.io/en/stable/installation/
```

3. Clone or download the repository (Make sure you have the latest release), and extract it.

4. Cloning dependencies, same method for all operating systems:

   a. In a terminal, navigate to the Roll2Mnemonic directory:

     ```bash
     cd C:\Roll2Mnemonic
     ```

   b. Create a subdirectory named wheelhouse:

     ```bash
     mkdir wheelhouse
     ```

   c. Run the following command to download the required dependencies to the subdirectory:

     ```bash
     pip download -r requirements.txt -d wheelhouse
     ```

   d. Copy the Python and pip packages you downloaded earlier and the folder Roll2Mnemonic, which contains the repository and the subfolder Wheelhouse, into a USB stick and transfer them to your offline computer.

   e. Install the Python and pip packages then, in a terminal, navigate to the Roll2Mnemonic folder:

     ```bash
     cd C:\Roll2Mnemonic
     ```

   f. Run the following to install the dependencies:

     ```bash
     pip install -r requirements.txt --no-index --find-links wheelhouse
     ```

   g. If you encounter installation errors you can try this alternative method to install the dependencies. Otherwise, you need to retrieve the failed dependencies manually:

     - Windows (Command Prompt):

       ```bash
       for %i in ("C:\path\to\folder with spaces\*") do pip install "%i"
       ```

     - Linux/Mac (Command Prompt):

       ```bash
       for package in "/path/to/folder with spaces"/*; do
           pip install "$package"
       done
       ```

Now your offline device should have all the required dependencies to run offline.


## Demo Video

  [![Video](http://img.youtube.com/vi/zpM8gb1_vQQ/0.jpg)](https://www.youtube.com/watch?v=zpM8gb1_vQQ)

## Support and Feedback

If you have any questions, encounter issues, or want to provide feedback, please open an issue in this repository or provide feedback through twitter @SaniExp.

## Donations

If you find this project useful and would like to support its development, you can make a donation to help keep it going. Your contributions are greatly appreciated!

- Bitcoin lightning address (Wallet Of Satoshi): sani@walletofsatoshi.com
- Bitcoin lightning address (Blink): sani@blink.sv

## Disclaimer

This tool should only be employed within a secure environment. When running the script, we strongly advise reading the disclaimer message to gain a comprehensive understanding of the risks associated with using such tools on unsecured devices.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
