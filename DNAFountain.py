import logging
import random
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Configure the logging module.
logging.basicConfig(
    # level=logging.DEBUG, 
    level=logging.INFO, 
    format="""[%(levelname)s] %(message)s""",
    filemode='w',
    filename='out.log'
)

class DNAFountain:
    DEGREE_TABLE = [
        ('0000', 2), ('0001', 2), ('0010', 1), ('0011', 1),
        ('0100', 2), ('0101', 4), ('0110', 2), ('0111', 1),
        ('1000', 6), ('1001', 1), ('1010', 1), ('1011', 2),
        ('1100', 7), ('1101', 2), ('1110', 1), ('1111', 4)
    ]
    BINARY_TO_DNA = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    DNA_TO_BINARY = {v: k for k, v in BINARY_TO_DNA.items()}

    def __init__(self, chunk_size=4, log_level="DEBUG"):
        self.chunk_size = chunk_size
        # Set the logger's level based on the provided log_level.
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError("""Invalid log level: {}""".format(log_level))
        logging.getLogger().setLevel(numeric_level)
        # Precompute a mapping from droplet seed to its degree.
        self.degree_map = {seed: degree for seed, degree in self.DEGREE_TABLE}
        logging.debug("""[DEBUG] DNAFountain initialized with chunk_size: {}""".format(self.chunk_size))
        logging.debug("""[DEBUG] Precomputed degree map: {}""".format(self.degree_map))

    def split_into_chunks(self, binary_string):
        logging.debug("""[DEBUG] Splitting binary string into chunks of size {}.""".format(self.chunk_size))
        chunks = [binary_string[i:i+self.chunk_size] for i in range(0, len(binary_string), self.chunk_size)]
        logging.debug("""[DEBUG] Resulting chunks: {}""".format(chunks))
        return chunks

    def generate_droplets(self, chunks):
        logging.debug("""[DEBUG] Generating droplets using degree map.""")
        droplets = []
        chunk_indices = list(range(len(chunks)))
        logging.debug("""[DEBUG] Available chunk indices: {}""".format(chunk_indices))
        
        for droplet_seed, droplet_degree in self.degree_map.items():
            logging.debug("""[DEBUG] Processing droplet with seed {} and degree {}""".format(droplet_seed, droplet_degree))
            # Use a local random generator seeded with droplet_seed.
            local_random = random.Random(int(droplet_seed, 2))
            selected_indices = local_random.sample(chunk_indices, min(droplet_degree, len(chunks)))
            logging.debug("""[DEBUG] With seed {}, sampled indices: {}""".format(droplet_seed, selected_indices))
            
            selected_chunks = [chunks[i] for i in selected_indices]
            logging.debug("""[DEBUG] Selected chunks: {}""".format(selected_chunks))
            
            combined_chunk = self.xor_chunks(selected_chunks)
            logging.debug("""[DEBUG] Combined chunk (after XOR): {}""".format(combined_chunk))
            
            droplets.append((droplet_seed, combined_chunk))
        
        logging.debug("""[DEBUG] Generated droplets: {}""".format(droplets))
        return droplets

    def xor_chunks(self, chunks):
        logging.debug("""[DEBUG] XORing chunks: {}""".format(chunks))
        result = int(chunks[0], 2)
        for chunk in chunks[1:]:
            result ^= int(chunk, 2)
        result_binary = format(result, '0{}b'.format(self.chunk_size))
        logging.debug("""[DEBUG] XOR result: {}""".format(result_binary))
        return result_binary

    def map_to_dna(self, binary_string):
        logging.debug("""[DEBUG] Mapping binary string to DNA: {}""".format(binary_string))
        dna_sequence = ''.join(
            self.BINARY_TO_DNA[binary_string[i:i+2]]
            for i in range(0, len(binary_string), 2)
        )
        logging.debug("""[DEBUG] DNA sequence: {}""".format(dna_sequence))
        return dna_sequence

    def encode_dna_fountain(self, binary_data):
        logging.debug("""[DEBUG] Encoding binary data using DNA Fountain: {}""".format(binary_data))
        chunks = self.split_into_chunks(binary_data)
        droplets = self.generate_droplets(chunks)
        dna_encoded_droplets = []
        for droplet_seed, data in droplets:
            dna_data = self.map_to_dna(data)
            logging.debug("""[DEBUG] Droplet with seed {} encoded to DNA: {}""".format(droplet_seed, dna_data))
            dna_encoded_droplets.append((droplet_seed, dna_data))
        
        logging.debug("""[DEBUG] All DNA encoded droplets: {}""".format(dna_encoded_droplets))
        return dna_encoded_droplets

    def decode_dna_fountain(self, dna_encoded_droplets, num_chunks):
        logging.debug("""[DEBUG] Decoding DNA encoded droplets. Expected number of chunks: {}""".format(num_chunks))
        binary_droplets = []
        
        for droplet_seed, dna in dna_encoded_droplets:
            binary_data = ''.join(self.DNA_TO_BINARY[char] for char in dna)
            droplet_degree = self.degree_map[droplet_seed]
            local_random = random.Random(int(droplet_seed, 2))
            selected_indices = local_random.sample(list(range(num_chunks)), min(droplet_degree, num_chunks))
            logging.debug("""[DEBUG] Droplet with seed {}: re-generated indices: {}""".format(droplet_seed, selected_indices))
            logging.debug("""[DEBUG] Converted DNA '{}' to binary: {}""".format(dna, binary_data))
            binary_droplets.append((selected_indices, binary_data))
        
        reconstructed = [None] * num_chunks
        logging.debug("""[DEBUG] Initial reconstructed chunks: {}""".format(reconstructed))
        
        for indices, data in binary_droplets:
            if len(indices) == 1:
                reconstructed[indices[0]] = data
                logging.debug("""[DEBUG] Directly assigned chunk at index {}: {}""".format(indices[0], data))
        
        for iteration in range(num_chunks):
            logging.debug("""[DEBUG] Decoding iteration {}/{}""".format(iteration + 1, num_chunks))
            for indices, data in binary_droplets:
                known_data = [reconstructed[i] for i in indices if reconstructed[i] is not None]
                unknown_indices = [i for i in indices if reconstructed[i] is None]
                
                if len(unknown_indices) == 1 and known_data:
                    logging.debug("""[DEBUG] Droplet {} with binary data {} has one unknown index: {} and known chunks: {}""".format(indices, data, unknown_indices[0], known_data))
                    xor_result = self.xor_chunks([data] + known_data)
                    reconstructed[unknown_indices[0]] = xor_result
                    logging.debug("""[DEBUG] Inferred missing chunk at index {}: {}""".format(unknown_indices[0], xor_result))
        
        logging.debug("""[DEBUG] Final reconstructed binary chunks: {}""".format(reconstructed))
        result = ''.join(filter(None, reconstructed))
        logging.debug("""[DEBUG] Decoded binary data: {}""".format(result))
        return result

    def encode_message_to_dna(self, binary_data):
        logging.debug("""[DEBUG] Encoding full message to a single DNA string.""")
        droplets = self.encode_dna_fountain(binary_data)
        full_dna_message = ""
        for seed, droplet_dna in droplets:
            seed_dna = self.map_to_dna(seed)
            full_dna_message += seed_dna + droplet_dna
            logging.debug("""[DEBUG] Droplet seed {} -> DNA '{}', droplet data -> DNA '{}'""".format(seed, seed_dna, droplet_dna))
        logging.debug("""[DEBUG] Full DNA encoded message: {}""".format(full_dna_message))
        return full_dna_message

    def decode_message_from_dna(self, dna_message, num_chunks):
        logging.debug("""[DEBUG] Decoding full DNA message back to binary data.""")
        seed_len = 2  # 4 bits of seed -> 2 nucleotides.
        droplet_dna_len = self.chunk_size // 2  # droplet XOR result: chunk_size bits -> chunk_size/2 nucleotides.
        segment_length = seed_len + droplet_dna_len
        droplets = []
        for i in range(0, len(dna_message), segment_length):
            segment = dna_message[i:i+segment_length]
            if len(segment) < segment_length:
                continue
            seed_dna = segment[:seed_len]
            droplet_dna = segment[seed_len:]
            seed_binary = ''.join(self.DNA_TO_BINARY[base] for base in seed_dna)
            droplets.append((seed_binary, droplet_dna))
            logging.debug("""[DEBUG] Parsed segment: seed DNA '{}' -> binary '{}', droplet DNA '{}'""".format(seed_dna, seed_binary, droplet_dna))
        decoded_binary = self.decode_dna_fountain(droplets, num_chunks)
        return decoded_binary

class DNAFountainTester:
    def __init__(self, chunk_size=4):
        """Initialize the tester with a fixed chunk size and a list of binary messages."""
        self.chunk_size = chunk_size
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
        print("""[TEST] Initializing DNAFountain with chunk_size={}...""".format(self.chunk_size))
        self.dna_fountain = DNAFountain(chunk_size=self.chunk_size, log_level="DEBUG")
        passed = True
        
        for binary_message in self.binary_messages:
            num_chunks = len(binary_message) // self.chunk_size
            print("""[TEST] Testing binary message: {}""".format(binary_message))
            
            # Test using the droplets approach.
            dna_droplets = self.dna_fountain.encode_dna_fountain(binary_message)
            decoded_binary = self.dna_fountain.decode_dna_fountain(dna_droplets, num_chunks)
            print("""[TEST] Original (droplets): {}""".format(binary_message))
            print("""[TEST] Decoded  (droplets): {}""".format(decoded_binary))
            
            if decoded_binary != binary_message:
                print("""[ERROR] Decoding failed for this message (droplets approach).""")
                passed = False
                break

            # Test using the full DNA string encoding.
            full_dna_message = self.dna_fountain.encode_message_to_dna(binary_message)
            decoded_binary_from_full = self.dna_fountain.decode_message_from_dna(full_dna_message, num_chunks)
            print("""[TEST] Full DNA encoded message: {}""".format(full_dna_message))
            print("""[TEST] Decoded from full DNA: {}""".format(decoded_binary_from_full))
            
            if decoded_binary_from_full != binary_message:
                print("""[ERROR] Decoding failed for this message (full DNA string approach).""")
                passed = False
                break
        
        if passed:
            print("""[TEST] ✅ All tests passed!""")
        else:
            print("""[TEST] ❌ Some tests failed.""")

if __name__ == "__main__":
    tester = DNAFountainTester()
    tester.run_tests()
