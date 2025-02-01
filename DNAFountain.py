#!/usr/bin/env python3
"""
DNA Fountain Project
--------------------

This project demonstrates a simplified DNA Fountain encoding and decoding system.
It encodes binary data into "droplets" (small units) using an XOR-based combination
of data chunks and maps the resulting binary data to a DNA sequence (using the nucleotides A, C, G, T).

Key Components:
- DNAFountain: Core class that implements the encoding and decoding routines.
- DNAFountainTester: Helper class that runs tests on a set of binary messages to ensure
  that encoding to DNA and decoding back to binary works correctly.
- main: Entry point for command-line execution, which configures logging and runs tests.

The encoding strategy uses a pre-defined "degree table" that assigns a degree (number of chunks
to combine) to each droplet based on its seed value. The droplets are generated using a local
random generator (seeded by the droplet's binary seed) so that the same combination of chunks
can be reproduced during decoding.
"""

import logging
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Ensure that the standard output encoding is UTF-8.
import argparse


class DNAFountain:
    """
    DNAFountain class implements the encoding and decoding of binary data using a droplet-based approach.
    It includes methods to split binary data into chunks, generate droplets by XORing chunks, map binary to DNA,
    and reconstruct the original binary data from DNA-encoded droplets.
    """

    # Pre-defined degree table for droplets.
    # Each tuple contains a binary seed (4 bits as a string) and its associated degree (number of chunks to combine).
    DEGREE_TABLE = [
        ('0000', 2), ('0001', 2), ('0010', 1), ('0011', 1),
        ('0100', 2), ('0101', 4), ('0110', 2), ('0111', 1),
        ('1000', 6), ('1001', 1), ('1010', 1), ('1011', 2),
        ('1100', 7), ('1101', 2), ('1110', 1), ('1111', 4)
    ]

    # Mapping from 2-bit binary string to DNA nucleotide.
    BINARY_TO_DNA = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    # Reverse mapping from DNA nucleotide back to 2-bit binary string.
    DNA_TO_BINARY = {v: k for k, v in BINARY_TO_DNA.items()}

    def __init__(self, chunk_size=4):
        """
        Initialize the DNAFountain object.

        Args:
            chunk_size (int): The size (in bits) of each data chunk.
        """
        self.chunk_size = chunk_size

        # Precompute a mapping from droplet seed to its degree using the DEGREE_TABLE.
        self.degree_map = {seed: degree for seed, degree in self.DEGREE_TABLE}

        logging.debug("DNAFountain initialized with chunk_size: {}".format(self.chunk_size))
        logging.debug("Precomputed degree map: {}".format(self.degree_map))

    def split_into_chunks(self, binary_string):
        """
        Split the input binary string into fixed-size chunks.

        Args:
            binary_string (str): The binary data as a string.

        Returns:
            list of str: List containing binary substrings (chunks) of size self.chunk_size.
        """
        logging.debug("Splitting binary string into chunks of size {}.".format(self.chunk_size))
        # Create chunks by slicing the binary string.
        chunks = [binary_string[i:i + self.chunk_size] for i in range(0, len(binary_string), self.chunk_size)]
        logging.debug("Resulting chunks: {}".format(chunks))
        return chunks

    def generate_droplets(self, chunks):
        """
        Generate droplets by selecting random chunks and combining them using XOR.

        For each droplet seed defined in the degree map:
            - A local random generator is seeded with the droplet's binary seed.
            - The generator randomly selects indices of chunks (the number is determined by the droplet's degree).
            - The selected chunks are combined (XORed together) to form the droplet data.

        Args:
            chunks (list of str): List of binary chunks.

        Returns:
            list of tuples: Each tuple contains the droplet seed and the XOR combined binary data.
        """
        logging.debug("Generating droplets using degree map.")
        droplets = []
        # Create a list of indices corresponding to the chunks.
        chunk_indices = list(range(len(chunks)))
        logging.debug("Available chunk indices: {}".format(chunk_indices))

        # Iterate over each droplet seed and its degree.
        for droplet_seed, droplet_degree in self.degree_map.items():
            logging.debug("Processing droplet with seed {} and degree {}".format(droplet_seed, droplet_degree))
            # Use a local random generator seeded with the integer conversion of the droplet seed.
            local_random = random.Random(int(droplet_seed, 2))
            # Randomly select indices from the available chunks (do not select more than the number of available chunks).
            selected_indices = local_random.sample(chunk_indices, min(droplet_degree, len(chunks)))
            logging.debug("With seed {}, sampled indices: {}".format(droplet_seed, selected_indices))

            # Retrieve the corresponding chunks based on the selected indices.
            selected_chunks = [chunks[i] for i in selected_indices]
            logging.debug("Selected chunks: {}".format(selected_chunks))

            # XOR the selected chunks together.
            combined_chunk = self.xor_chunks(selected_chunks)
            logging.debug("Combined chunk (after XOR): {}".format(combined_chunk))

            # Append the droplet seed and its combined data to the list of droplets.
            droplets.append((droplet_seed, combined_chunk))

        logging.debug("Generated droplets: {}".format(droplets))
        return droplets

    def xor_chunks(self, chunks):
        """
        Perform bitwise XOR on a list of binary strings (chunks).

        Args:
            chunks (list of str): List of binary string chunks.

        Returns:
            str: The resulting binary string after performing XOR on all input chunks.
        """
        logging.debug("XORing chunks: {}".format(chunks))
        # Convert the first chunk from binary string to an integer.
        result = int(chunks[0], 2)
        # Perform XOR with the remaining chunks.
        for chunk in chunks[1:]:
            result ^= int(chunk, 2)
        # Format the result back into a binary string with leading zeros to match chunk_size.
        result_binary = format(result, '0{}b'.format(self.chunk_size))
        logging.debug("XOR result: {}".format(result_binary))
        return result_binary

    def map_to_dna(self, binary_string):
        """
        Map a binary string to a DNA sequence using the BINARY_TO_DNA mapping.

        Each pair of binary digits (2 bits) is converted to a corresponding DNA nucleotide.

        Args:
            binary_string (str): A binary string where the length should be a multiple of 2.

        Returns:
            str: The resulting DNA sequence.
        """
        logging.debug("Mapping binary string to DNA: {}".format(binary_string))
        # Convert every 2-bit segment to its corresponding nucleotide.
        dna_sequence = ''.join(
            self.BINARY_TO_DNA[binary_string[i:i+2]]
            for i in range(0, len(binary_string), 2)
        )
        logging.debug("DNA sequence: {}".format(dna_sequence))
        return dna_sequence

    def droplets_encode(self, binary_data):
        """
        Encode binary data into droplets and convert the droplet data to DNA sequences.

        Process:
            1. Split binary data into fixed-size chunks.
            2. Generate droplets by XORing a subset of chunks.
            3. Map each droplet's binary data to a DNA sequence.

        Args:
            binary_data (str): The binary data as a string.

        Returns:
            list of tuples: Each tuple contains the droplet seed and its DNA-encoded data.
        """
        logging.debug("Encoding binary data using DNA Fountain: {}".format(binary_data))
        # Split the binary data into chunks.
        chunks = self.split_into_chunks(binary_data)
        # Generate droplets from the chunks.
        droplets = self.generate_droplets(chunks)
        dna_encoded_droplets = []
        # Process each droplet to map its binary data to DNA.
        for droplet_seed, data in droplets:
            dna_data = self.map_to_dna(data)
            logging.debug("Droplet with seed {} encoded to DNA: {}".format(droplet_seed, dna_data))
            dna_encoded_droplets.append((droplet_seed, dna_data))

        logging.debug("All DNA encoded droplets: {}".format(dna_encoded_droplets))
        return dna_encoded_droplets

    def droplets_decode(self, dna_encoded_droplets, num_chunks):
        """
        Decode a list of DNA-encoded droplets back into the original binary data.

        The method:
            1. Converts each droplet's DNA back to binary.
            2. Regenerates the indices of chunks used (based on the droplet seed).
            3. Attempts to reconstruct the original chunks by direct assignment (when only one unknown)
               and iterative XOR resolution.

        Args:
            dna_encoded_droplets (list of tuples): Each tuple contains a droplet seed (binary string)
                                                   and its DNA-encoded data.
            num_chunks (int): The expected number of chunks in the original binary message.

        Returns:
            str: The decoded binary data as a concatenated string.
        """
        logging.debug("Decoding DNA encoded droplets. Expected number of chunks: {}".format(num_chunks))
        binary_droplets = []

        # Convert each DNA-encoded droplet back to binary and determine its selected chunk indices.
        for droplet_seed, dna in dna_encoded_droplets:
            # Convert the DNA string back to its binary representation.
            binary_data = ''.join(self.DNA_TO_BINARY[char] for char in dna)
            # Get the degree for this droplet using the degree map.
            droplet_degree = self.degree_map[droplet_seed]
            # Re-seed the random generator with the droplet seed to obtain the same indices.
            local_random = random.Random(int(droplet_seed, 2))
            selected_indices = local_random.sample(list(range(num_chunks)), min(droplet_degree, num_chunks))
            logging.debug("Droplet with seed {}: re-generated indices: {}".format(droplet_seed, selected_indices))
            logging.debug("Converted DNA '{}' to binary: {}".format(dna, binary_data))
            binary_droplets.append((selected_indices, binary_data))

        # Initialize a list to hold reconstructed chunks (initially all are unknown, represented as None).
        reconstructed = [None] * num_chunks
        logging.debug("Initial reconstructed chunks: {}".format(reconstructed))

        # First pass: assign chunks that are directly determined by droplets that only cover one chunk.
        for indices, data in binary_droplets:
            if len(indices) == 1:
                reconstructed[indices[0]] = data
                logging.debug("Directly assigned chunk at index {}: {}".format(indices[0], data))

        # Iteratively resolve unknown chunks using droplets that have exactly one unknown chunk.
        for iteration in range(num_chunks):
            logging.debug("Decoding iteration {}/{}".format(iteration + 1, num_chunks))
            for indices, data in binary_droplets:
                # Collect already known data from the droplets.
                known_data = [reconstructed[i] for i in indices if reconstructed[i] is not None]
                # Identify the index (if any) that is still unknown.
                unknown_indices = [i for i in indices if reconstructed[i] is None]

                # If exactly one chunk is unknown and at least one known exists, we can solve for it.
                if len(unknown_indices) == 1 and known_data:
                    logging.debug(
                        "Droplet {} with binary data {} has one unknown index: {} and known chunks: {}"
                        .format(indices, data, unknown_indices[0], known_data)
                    )
                    # XOR the droplet's binary data with all known chunks to infer the missing chunk.
                    xor_result = self.xor_chunks([data] + known_data)
                    reconstructed[unknown_indices[0]] = xor_result
                    logging.debug("Inferred missing chunk at index {}: {}".format(unknown_indices[0], xor_result))

        logging.debug("Final reconstructed binary chunks: {}".format(reconstructed))
        # Concatenate the chunks that have been reconstructed to form the final binary data.
        result = ''.join(filter(None, reconstructed))
        logging.debug("Decoded binary data: {}".format(result))
        return result

    def encode_message_to_dna(self, binary_data):
        """
        Encode a full binary message into a single DNA string.

        Process:
            1. Encode the binary data into droplets (each droplet contains a seed and XOR result).
            2. Convert both the droplet seed and droplet data to DNA.
            3. Concatenate the DNA representations to form a full DNA encoded message.

        Args:
            binary_data (str): The binary data as a string.

        Returns:
            str: A DNA string representing the full encoded message.
        """
        logging.debug("Encoding full message to a single DNA string.")
        # First, obtain the droplets (seed and binary data) for the given binary message.
        droplets = self.droplets_encode(binary_data)
        full_dna_message = ""
        # Convert each droplet's seed and data to DNA and append them.
        for seed, droplet_dna in droplets:
            seed_dna = self.map_to_dna(seed)
            # Concatenate the seed DNA and droplet data DNA.
            full_dna_message += seed_dna + droplet_dna
            logging.debug("Droplet seed {} -> DNA '{}', droplet data -> DNA '{}'"
                          .format(seed, seed_dna, droplet_dna))
        logging.debug("Full DNA encoded message: {}".format(full_dna_message))
        return full_dna_message

    def decode_message_from_dna(self, dna_message, num_chunks):
        """
        Decode a full DNA encoded message back to its original binary representation.

        The method:
            1. Splits the DNA message into segments, each containing the seed and droplet data.
            2. Converts the seed and droplet parts back to binary.
            3. Uses the droplets decoding method to reconstruct the full binary data.

        Args:
            dna_message (str): The full DNA encoded message.
            num_chunks (int): The expected number of chunks (used during droplets decoding).

        Returns:
            str: The decoded binary data.
        """
        logging.debug("Decoding full DNA message back to binary data.")
        # Determine the length of the DNA representation for the droplet seed.
        seed_len = 2  # 4 bits of seed are represented as 2 nucleotides.
        # Determine the length of the DNA representation for the droplet data.
        droplet_dna_len = self.chunk_size // 2  # Each nucleotide represents 2 bits.
        # The total length of one segment (seed + droplet data).
        segment_length = seed_len + droplet_dna_len
        droplets = []
        # Process each segment of the full DNA message.
        for i in range(0, len(dna_message), segment_length):
            segment = dna_message[i:i+segment_length]
            if len(segment) < segment_length:
                # If the segment is shorter than expected, skip it.
                continue
            # Extract the seed and droplet data parts.
            seed_dna = segment[:seed_len]
            droplet_dna = segment[seed_len:]
            # Convert the seed from DNA to binary.
            seed_binary = ''.join(self.DNA_TO_BINARY[base] for base in seed_dna)
            droplets.append((seed_binary, droplet_dna))
            logging.debug("Parsed segment: seed DNA '{}' -> binary '{}', droplet DNA '{}'"
                          .format(seed_dna, seed_binary, droplet_dna))
        # Decode the binary droplets to reconstruct the original binary message.
        decoded_binary = self.droplets_decode(droplets, num_chunks)
        return decoded_binary


class DNAFountainTester:
    """
    DNAFountainTester class is used to run a series of tests on the DNAFountain encoding and decoding process.
    It contains a list of predefined binary messages and verifies that each message can be correctly encoded to DNA
    and decoded back to its original binary form using both the droplets approach and the full DNA string approach.
    """

    def __init__(self, chunk_size=4):
        """
        Initialize the tester with a fixed chunk size and a list of binary messages.

        Args:
            chunk_size (int): The size (in bits) of each data chunk for the DNAFountain.
        """
        self.chunk_size = chunk_size
        # Predefined set of binary messages for testing.
        self.binary_messages = [
            "01010011110001001110011001001001",
            "01111000010010100110110001001110",
            "10001101110111100111000000111100",
            "11111110110010010001010110011110",
            "10001000100001011011111011101011",
            "01011010010100001110000110110110",
            "11101000111011000001001101001100",
            "01101110000100001110000001110101",
            "00100110011110010110101100100010",
            "10001010111101010000001001001011",
            "01010111010110011011001101010010",
        ]

    def run_tests(self):
        """
        Run tests on all predefined binary messages.

        For each message, perform two tests:
            1. Use the droplets approach (encode and then decode) and verify correctness.
            2. Encode the message to a full DNA string, then decode it back, verifying correctness.

        Logs and prints the results of each test.
        """
        msg = "[TEST] Initializing DNAFountain with chunk_size={}...".format(self.chunk_size)
        print(msg)
        logging.info(msg)

        # Create a DNAFountain object with the specified chunk size.
        self.dna_fountain = DNAFountain(chunk_size=self.chunk_size)
        passed = True

        # Iterate over each test message.
        for binary_message in self.binary_messages:
            msg = "[TEST] Testing binary message: {}".format(binary_message)
            print(msg)
            logging.info(msg)

            # Ensure that the message length is a multiple of the chunk size.
            if len(binary_message) % self.chunk_size != 0:
                msg = "[ERROR] Message length is not a multiple of chunk size. Skipping this message."
                print(msg)
                logging.info(msg)
                continue

            # Test using the droplets approach.
            dna_droplets = self.dna_fountain.droplets_encode(binary_message)
            decoded_binary = self.dna_fountain.droplets_decode(dna_droplets, len(binary_message) // self.chunk_size)

            msg = "[TEST] Original (droplets): {}".format(binary_message)
            print(msg)
            logging.info(msg)

            msg = "[TEST] Decoded  (droplets): {}".format(decoded_binary)
            print(msg)
            logging.info(msg)

            if decoded_binary != binary_message:
                msg = "[ERROR] Decoding failed for this message (droplets approach)."
                print(msg)
                logging.info(msg)
                passed = False
                break

            # Test using the full DNA string encoding.
            full_dna_message = self.dna_fountain.encode_message_to_dna(binary_message)
            decoded_binary_from_full = self.dna_fountain.decode_message_from_dna(
                full_dna_message,
                len(binary_message) // self.chunk_size
            )

            msg = "[TEST] Full DNA encoded message: {}".format(full_dna_message)
            print(msg)
            logging.info(msg)

            msg = "[TEST] Decoded from full DNA: {}".format(decoded_binary_from_full)
            print(msg)
            logging.info(msg)

            if decoded_binary_from_full != binary_message:
                msg = "[ERROR] Decoding failed for this message (full DNA string approach)."
                print(msg)
                logging.info(msg)
                passed = False
                break

        # Report overall test results.
        if passed:
            msg = "[TEST] ✅ All tests passed!"
            print(msg)
            logging.info(msg)
        else:
            msg = "[TEST] ❌ Some tests failed."
            print(msg)
            logging.info(msg)


def main():
    """
    Main entry point for the DNA Fountain Tester.

    This function:
      - Parses command-line arguments (for example, the desired logging level).
      - Configures logging.
      - Instantiates the DNAFountainTester.
      - Runs the tests.
    """
    # Set up argument parsing for the log level.
    parser = argparse.ArgumentParser(description='DNA Fountain Tester')
    parser.add_argument('--log-level', default='DEBUG',
                        help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    args = parser.parse_args()

    # Convert the log level string to the corresponding numeric level.
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {args.log_level}")

    print(f"Logging level set to: {args.log_level}")
    # Configure logging settings: output to a file with a specific format and encoding.
    logging.basicConfig(
        level=numeric_level,
        encoding='utf-8',
        format="[%(levelname)s] %(message)s",
        filename='output.log',
        filemode='w'
    )

    # Initialize the tester with a given chunk size.
    tester = DNAFountainTester(chunk_size=4)
    tester.run_tests()


# Ensure that the main function is only executed when the script is run directly.
if __name__ == "__main__":
    main()
