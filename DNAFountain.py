import logging
import random
from random import Random
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Ensure that the standard output encoding is UTF-8.


class DNAFountain:
    """
    DNAFountain implements the encoding and decoding of binary data using a droplet-based approach.
    It includes methods to split binary data into chunks, generate droplets by XORing chunks,
    map binary to DNA, and reconstruct the original binary data from DNA-encoded droplets.
    """

    DEGREE_TABLE = [
        ('0000', 2), ('0001', 2), ('0010', 1), ('0011', 1),
        ('0100', 2), ('0101', 4), ('0110', 2), ('0111', 1),
        ('1000', 6), ('1001', 1), ('1010', 1), ('1011', 2),
        ('1100', 7), ('1101', 2), ('1110', 1), ('1111', 4)
    ]

    BINARY_TO_DNA = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    DNA_TO_BINARY = {v: k for k, v in BINARY_TO_DNA.items()}

    def __init__(self, chunk_size=4):
        """
        Initialize the DNAFountain object.

        Args:
            chunk_size (int): The size (in bits) of each data chunk.
        """
        self.chunk_size = chunk_size
        self.degree_map = {seed: degree for seed, degree in self.DEGREE_TABLE}
        logging.debug("=== DNAFountain Initialization ===")
        logging.debug("Chunk size: %s", self.chunk_size)
        logging.debug("Degree map: %s", self.degree_map)
        logging.debug("==================================")

    def split_into_chunks(self, binary_string):
        """
        Split the input binary string into fixed-size chunks.

        Args:
            binary_string (str): The binary data as a string.

        Returns:
            list of str: List of binary substrings (chunks) of size self.chunk_size.
        """
        logging.debug("=== SPLIT INTO CHUNKS ===")
        logging.debug("Input binary string: %s", binary_string)
        chunks = [binary_string[i:i + self.chunk_size]
                  for i in range(0, len(binary_string), self.chunk_size)]
        logging.debug("Chunks: %s", chunks)
        logging.debug("=========================")
        return chunks

    def generate_droplets_data(self, chunks):
        """
        Generate droplets by selecting random chunks and combining them using XOR.
        The droplet data payload is eventually mapped to a DNA sequence.

        Args:
            chunks (list of str): List of binary chunks.

        Returns:
            list of tuples: Each tuple contains the droplet seed (in binary) and
                            the droplet data payload (in binary form, to be mapped later).
        """
        logging.debug("=== DROPLET GENERATION START ===")
        logging.debug("Available chunks: %s", chunks)
        droplets = []
        chunk_indices = list(range(len(chunks)))
        logging.debug("Chunk indices: %s", chunk_indices)

        for droplet_seed, droplet_degree in self.degree_map.items():
            logging.debug(">> Processing droplet with seed '%s' (degree %d)", droplet_seed, droplet_degree)
            selected_indices = Random(int(droplet_seed, 2)).sample(chunk_indices, min(droplet_degree, len(chunks)))
            logging.debug("   Selected indices: %s", selected_indices)
            selected_chunks = [chunks[i] for i in selected_indices]
            logging.debug("   Selected chunks: %s", selected_chunks)
            combined_chunk = self.xor_chunks(selected_chunks)
            logging.debug("   XOR result (binary): %s", combined_chunk)
            droplets.append((droplet_seed, combined_chunk))
        logging.debug("=== DROPLET GENERATION END ===")
        logging.debug("Generated droplets (binary seed and data payload): %s", droplets)
        return droplets

    def xor_chunks(self, chunks):
        """
        Perform bitwise XOR on a list of binary string chunks.

        Args:
            chunks (list of str): List of binary string chunks.

        Returns:
            str: The resulting binary string after XOR.
        """
        logging.debug("=== XOR CHUNKS ===")
        logging.debug("Input chunks: %s", chunks)
        result = int(chunks[0], 2)
        for chunk in chunks[1:]:
            result ^= int(chunk, 2)
        result_binary = format(result, '0{}b'.format(self.chunk_size))
        logging.debug("XOR result (binary): %s", result_binary)
        logging.debug("==================")
        return result_binary

    def map_to_dna(self, binary_string):
        """
        Map a binary string to a DNA sequence using the BINARY_TO_DNA mapping.

        Args:
            binary_string (str): A binary string (length should be a multiple of 2).

        Returns:
            str: The corresponding DNA sequence.
        """
        logging.debug("=== MAP TO DNA ===")
        logging.debug("Binary input: %s", binary_string)
        dna_sequence = ''.join(
            self.BINARY_TO_DNA[binary_string[i:i+2]]
            for i in range(0, len(binary_string), 2)
        )
        logging.debug("Mapped DNA sequence: %s", dna_sequence)
        logging.debug("==================")
        return dna_sequence

    def encode_droplets(self, binary_data):
        """
        Encode binary data into droplets and convert each droplet's seed and data payload to DNA.
        (The generated droplets will be represented solely in DNA.)

        Args:
            binary_data (str): The binary data as a string.

        Returns:
            list of tuples: Each tuple contains the droplet seed (DNA) and its droplet data payload (DNA).
        """
        logging.debug("=== DROPLETS ENCODING START ===")
        logging.debug("Input binary data: %s", binary_data)
        chunks = self.split_into_chunks(binary_data)
        droplets = self.generate_droplets_data(chunks)
        dna_encoded_droplets = []
        for droplet_seed, content_binary in droplets:
            # Map both the droplet seed and droplet data payload to DNA.
            droplet_seed_dna = self.map_to_dna(droplet_seed)
            droplet_content_dna = self.map_to_dna(content_binary)
            logging.debug("Encoded droplet: Seed (binary) '%s' mapped to (DNA) '%s'; "
                          "Data Payload (binary) '%s' mapped to (DNA) '%s'",
                          droplet_seed, droplet_seed_dna, content_binary, droplet_content_dna)
            dna_encoded_droplets.append((droplet_seed_dna, droplet_content_dna))
        logging.debug("=== DROPLETS ENCODING END ===")
        logging.debug("DNA Encoded Droplets (both seed and data payload in DNA): %s", dna_encoded_droplets)
        return dna_encoded_droplets

    def encode_message_to_dna(self, binary_data):
        """
        Encode a full binary message into a single DNA string.
        The final message consists solely of DNA: both the droplet seed and droplet data payload
        are already in DNA and concatenated.

        Args:
            binary_data (str): The binary data as a string.

        Returns:
            str: The complete DNA-encoded message.
        """
        logging.debug("=== FULL MESSAGE ENCODING START ===")
        logging.debug("Input binary message: %s", binary_data)
        droplets = self.encode_droplets(binary_data)
        full_dna_message = ""
        for seed_dna, droplet_content_dna in droplets:
            full_drop = seed_dna + droplet_content_dna
            full_dna_message += full_drop
            logging.debug("Droplet encoded: Seed (DNA): '%s' | Droplet data payload (DNA): '%s'",
                          seed_dna, droplet_content_dna)
            logging.debug("Concatenated droplet (DNA): '%s'", full_drop)
        logging.debug("Full DNA Encoded Message: %s", full_dna_message)
        logging.debug("=== FULL MESSAGE ENCODING END ===")
        return full_dna_message

    def decode_droplets(self, dna_encoded_droplets, num_chunks):
        """
        Decode a list of DNA-encoded droplets back into the original binary data.
        (Here the droplets are provided as DNA representations for both seed and data payload.)

        Args:
            dna_encoded_droplets (list of tuples): Each tuple contains a droplet seed (DNA) and
                                                   droplet data payload (DNA).
            num_chunks (int): Expected number of chunks in the original binary message.

        Returns:
            str: The reconstructed binary message.
        """
        logging.debug("=== DROPLETS DECODING START ===")
        logging.debug("Expected number of chunks: %d", num_chunks)
        binary_droplets = []
        logging.debug("DNA Encoded Droplets (both seed and data payload in DNA): %s", dna_encoded_droplets)
        for droplet_seed_dna, dna_content in dna_encoded_droplets:
            # Convert both the droplet seed and droplet data payload from DNA back to binary.
            seed_binary = ''.join(self.DNA_TO_BINARY[base] for base in droplet_seed_dna)
            content_binary = ''.join(self.DNA_TO_BINARY[char] for char in dna_content)
            droplet_degree = self.degree_map[seed_binary]
            selected_indices = Random(int(seed_binary, 2)).sample(list(range(num_chunks)), min(droplet_degree, num_chunks))
            logging.debug("Droplet: Seed (DNA) '%s' -> Seed (binary) '%s' -> Indices %s | "
                          "Data Payload (DNA): '%s' -> Data Payload (binary): '%s'",
                          droplet_seed_dna, seed_binary, selected_indices, dna_content, content_binary)
            binary_droplets.append((selected_indices, content_binary))

        reconstructed = [None] * num_chunks
        logging.debug("Initial reconstructed chunks: %s", reconstructed)

        # Direct assignment for droplets that cover a single chunk.
        for indices, data in binary_droplets:
            if len(indices) == 1:
                reconstructed[indices[0]] = data
                logging.debug("Direct assignment: Chunk[%d] = %s", indices[0], data)

        # Iteratively resolve chunks with exactly one unknown per droplet.
        for iteration in range(num_chunks):
            logging.debug("Iteration %d/%d", iteration + 1, num_chunks)
            for indices, data in binary_droplets:
                known_data = [reconstructed[i] for i in indices if reconstructed[i] is not None]
                unknown_indices = [i for i in indices if reconstructed[i] is None]
                if len(unknown_indices) == 1 and known_data:
                    logging.debug("Resolving Chunk[%d] using droplet %s with data payload (binary): '%s' "
                                  "and known chunks: %s", unknown_indices[0], indices, data, known_data)
                    xor_result = self.xor_chunks([data] + known_data)
                    reconstructed[unknown_indices[0]] = xor_result
                    logging.debug("Inferred Chunk[%d] = %s", unknown_indices[0], xor_result)
        logging.debug("Reconstructed chunks: %s", reconstructed)
        result = ''.join(filter(None, reconstructed))
        logging.debug("Decoded binary message: %s", result)
        logging.debug("=== DROPLETS DECODING END ===")
        return result

    def decode_message_from_dna(self, dna_message, num_chunks):
        """
        Decode a full DNA-encoded message back into its original binary representation.
        
        The full DNA message is split into fixed-length segments, where each segment is composed of:
        - The droplet seed in DNA (e.g. 2 nucleotides representing the seed bits)
        - The droplet data payload in DNA (derived from the XOR-combined data)
        
        These segments are assembled into a list of tuples (seed_dna, droplet_dna) that is then
        passed to the decode_droplets function (which expects both values to be in DNA format).

        Args:
            dna_message (str): The complete DNA-encoded message.
            num_chunks (int): The expected number of data chunks (used during droplets decoding).

        Returns:
            str: The decoded binary data.
        """
        logging.debug("=== FULL MESSAGE DECODING START ===")
        logging.debug("Input DNA message: %s", dna_message)
        seed_len = 2  # For example, 4 bits of seed represented as 2 nucleotides.
        droplet_dna_len = self.chunk_size // 2  # Each nucleotide represents 2 bits.
        segment_length = seed_len + droplet_dna_len
        droplets = []

        for i in range(0, len(dna_message), segment_length):
            segment = dna_message[i:i+segment_length]
            if len(segment) < segment_length:
                logging.debug("Skipping incomplete segment: %s", segment)
                continue
            seed_dna = segment[:seed_len]
            droplet_dna = segment[seed_len:]
            droplets.append((seed_dna, droplet_dna))

        decoded_binary = self.decode_droplets(droplets, num_chunks)
        logging.debug("Decoded binary message: %s", decoded_binary)
        logging.debug("=== FULL MESSAGE DECODING END ===")
        return decoded_binary

