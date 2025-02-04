Here is the beautified README file with icons:

# 🧬 DNA Fountain

## 📖 Overview
This project demonstrates a simplified DNA Fountain encoding and decoding system. It encodes binary data into "droplets" (small units) using an XOR-based combination of data chunks and maps the resulting binary data to a DNA sequence using the nucleotides A, C, G, T.

## 🛠️ Key Components
- **DNAFountain**: Core class that implements the encoding and decoding routines.
- **DNAFountainTester**: Helper class that runs tests on a set of binary messages to ensure that encoding to DNA and decoding back to binary works correctly.
- **main**: Entry point for command-line execution, which configures logging and runs tests.

## ✨ Features
- **Encoding Strategy**: Uses a pre-defined "degree table" that assigns a degree (number of chunks to combine) to each droplet based on its seed value. The droplets are generated using a local random generator (seeded by the droplet's binary seed) so that the same combination of chunks can be reproduced during decoding.
- **Binary to DNA Mapping**: Maps binary data to DNA sequences and vice versa.

## 🛠️ Setup
1. Ensure you have Python 3 installed.
2. Clone the repository:
   ```sh
   git clone https://github.com/v1t3ls0n/DNA-fountain.git
   ```
3. Navigate to the project directory:
   ```sh
   cd DNA-fountain
   ```
4. Run the tests:
   ```sh
   python3 main.py
   ```

## 🚀 Usage
The main entry point for the project is the `main.py` file, which configures logging and runs tests using the `DNAFountainTester` class.

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to modify and expand this README as needed for your project.