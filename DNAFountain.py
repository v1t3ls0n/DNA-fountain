import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

class DNAFountain:
    DEGREE_TABLE = [
        ('0000', 2), ('0001', 2), ('0010', 1), ('0011', 1),
        ('0100', 2), ('0101', 4), ('0110', 2), ('0111', 1),
        ('1000', 6), ('1001', 1), ('1010', 1), ('1011', 2),
        ('1100', 7), ('1101', 2), ('1110', 1), ('1111', 4)
    ]
    BINARY_TO_DNA = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    DNA_TO_BINARY = {v: k for k, v in BINARY_TO_DNA.items()}

    def __init__(self, chunk_size=4):
        self.chunk_size = chunk_size
        # Precompute a mapping from droplet seed to its degree.
        self.degree_map = {seed: degree for seed, degree in self.DEGREE_TABLE}
        print(f"""[DEBUG] DNAFountain initialized with chunk_size: {self.chunk_size}""")
        print(f"""[DEBUG] Precomputed degree map: {self.degree_map}""")

    def split_into_chunks(self, binary_string):
        """Splits the input binary string into chunks of the class-defined size."""
        print(f"""[DEBUG] Splitting binary string into chunks of size {self.chunk_size}.""")
        chunks = [binary_string[i:i+self.chunk_size] for i in range(0, len(binary_string), self.chunk_size)]
        print(f"""[DEBUG] Resulting chunks: {chunks}""")
        return chunks

    def generate_droplets(self, chunks):
        """
        Generates droplets using the precomputed degree map.
        For each item in the degree map, its key (a 4-bit binary string) is used as a seed for a
        local random generator to sample indices. Only the droplet's seed and the XOR result of the
        selected chunks are saved.
        """
        print(f"""[DEBUG] Generating droplets using degree map.""")
        droplets = []
        chunk_indices = list(range(len(chunks)))
        print(f"""[DEBUG] Available chunk indices: {chunk_indices}""")
        
        # Iterate directly over the degree map items.
        for droplet_seed, droplet_degree in self.degree_map.items():
            print(f"""[DEBUG] Processing droplet with seed {droplet_seed} and degree {droplet_degree}""")
            
            # Use a local random generator seeded with the droplet_seed.
            local_random = random.Random(int(droplet_seed, 2))
            selected_indices = local_random.sample(chunk_indices, min(droplet_degree, len(chunks)))
            print(f"""[DEBUG] With seed {droplet_seed}, sampled indices: {selected_indices}""")
            
            selected_chunks = [chunks[i] for i in selected_indices]
            print(f"""[DEBUG] Selected chunks: {selected_chunks}""")
            
            combined_chunk = self.xor_chunks(selected_chunks)
            print(f"""[DEBUG] Combined chunk (after XOR): {combined_chunk}""")
            
            # Save only the droplet's seed and its XOR result.
            droplets.append((droplet_seed, combined_chunk))
        
        print(f"""[DEBUG] Generated droplets: {droplets}""")
        return droplets

    def xor_chunks(self, chunks):
        """XORs multiple chunks together."""
        print(f"""[DEBUG] XORing chunks: {chunks}""")
        result = int(chunks[0], 2)
        for chunk in chunks[1:]:
            result ^= int(chunk, 2)
        # Format the result as a binary string with width equal to the chunk size.
        result_binary = format(result, '0{}b'.format(self.chunk_size))
        print(f"""[DEBUG] XOR result: {result_binary}""")
        return result_binary

    def map_to_dna(self, binary_string):
        """Maps a binary string to a DNA sequence."""
        print(f"""[DEBUG] Mapping binary string to DNA: {binary_string}""")
        dna_sequence = ''.join(
            self.BINARY_TO_DNA[binary_string[i:i+2]] 
            for i in range(0, len(binary_string), 2)
        )
        print(f"""[DEBUG] DNA sequence: {dna_sequence}""")
        return dna_sequence

    def encode_dna_fountain(self, binary_data):
        """
        Encodes binary data using the DNA Fountain algorithm.
        The input data is split into chunks, droplets are generated (each droplet holds only its seed
        and XOR result), and then each XOR result is mapped to a DNA sequence.
        """
        print(f"""[DEBUG] Encoding binary data using DNA Fountain: {binary_data}""")
        chunks = self.split_into_chunks(binary_data)
        droplets = self.generate_droplets(chunks)
        dna_encoded_droplets = []
        for droplet_seed, data in droplets:
            dna_data = self.map_to_dna(data)
            print(f"""[DEBUG] Droplet with seed {droplet_seed} encoded to DNA: {dna_data}""")
            dna_encoded_droplets.append((droplet_seed, dna_data))
        
        print(f"""[DEBUG] All DNA encoded droplets: {dna_encoded_droplets}""")
        return dna_encoded_droplets

    def decode_dna_fountain(self, dna_encoded_droplets, num_chunks):
        """
        Decodes the DNA encoded droplets. For each droplet, its seed is used to re-sample the indices of the
        original chunks. The XOR result is then used (in combination with other droplets) to iteratively
        reconstruct the original data.
        """
        print(f"""[DEBUG] Decoding DNA encoded droplets. Expected number of chunks: {num_chunks}""")
        binary_droplets = []
        
        for droplet_seed, dna in dna_encoded_droplets:
            # Convert DNA back to binary.
            binary_data = ''.join(self.DNA_TO_BINARY[char] for char in dna)
            # Use the droplet seed to re-generate the indices.
            droplet_degree = self.degree_map[droplet_seed]
            local_random = random.Random(int(droplet_seed, 2))
            selected_indices = local_random.sample(list(range(num_chunks)), min(droplet_degree, num_chunks))
            print(f"""[DEBUG] Droplet with seed {droplet_seed}: re-generated indices: {selected_indices}""")
            print(f"""[DEBUG] Converted DNA '{dna}' to binary: {binary_data}""")
            binary_droplets.append((selected_indices, binary_data))
        
        reconstructed = [None] * num_chunks
        print(f"""[DEBUG] Initial reconstructed chunks: {reconstructed}""")
        
        # First pass: directly assign droplets that affect only one chunk.
        for indices, data in binary_droplets:
            if len(indices) == 1:
                reconstructed[indices[0]] = data
                print(f"""[DEBUG] Directly assigned chunk at index {indices[0]}: {data}""")
        
        # Iterative decoding: resolve droplets with exactly one unknown chunk.
        for iteration in range(num_chunks):
            print(f"""[DEBUG] Decoding iteration {iteration + 1}/{num_chunks}""")
            for indices, data in binary_droplets:
                known_data = [reconstructed[i] for i in indices if reconstructed[i] is not None]
                unknown_indices = [i for i in indices if reconstructed[i] is None]
                
                if len(unknown_indices) == 1 and known_data:
                    print(f"""[DEBUG] Droplet {indices} with binary data {data} has one unknown index: {unknown_indices[0]} and known chunks: {known_data}""")
                    xor_result = self.xor_chunks([data] + known_data)
                    reconstructed[unknown_indices[0]] = xor_result
                    print(f"""[DEBUG] Inferred missing chunk at index {unknown_indices[0]}: {xor_result}""")
        
        print(f"""[DEBUG] Final reconstructed binary chunks: {reconstructed}""")
        # Join chunks to form the complete binary string, filtering out any None.
        result = ''.join(filter(None, reconstructed))
        print(f"""[DEBUG] Decoded binary data: {result}""")
        return result


class DNAFountainTester:
    def __init__(self):
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
        print(f"""\n[TEST] Initializing DNAFountain with chunk_size=4...""")
        self.dna_fountain = DNAFountain(chunk_size=4)
        passed = True
        
        for binary_message in self.binary_messages:
            print(f"""\n[TEST] Testing binary message: {binary_message}""")
            dna_droplets = self.dna_fountain.encode_dna_fountain(binary_message)
            num_chunks = len(self.dna_fountain.split_into_chunks(binary_message))
            decoded_binary = self.dna_fountain.decode_dna_fountain(dna_droplets, num_chunks)
            print(f"""\n[TEST] Original: {binary_message}""")
            print(f"""\n[TEST] Decoded : {decoded_binary}""")
            if decoded_binary != binary_message:
                print(f"""\n[ERROR] Decoding failed for this message.""")
                passed = False
                break
        
        if passed:
            print(f"""\n✅ All tests passed!""")
        else:
            print(f"""\n❌ Some tests failed.""")

if __name__ == "__main__":
    tester = DNAFountainTester()
    tester.run_tests()
