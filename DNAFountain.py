import random

class DNAFountain:
    DEGREE_TABLE = [
        ('0000', 2), ('0001', 2), ('0010', 1), ('0011', 1),
        ('0100', 2), ('0101', 4), ('0110', 2), ('0111', 1),
        ('1000', 6), ('1001', 1), ('1010', 1), ('1011', 2),
        ('1100', 7), ('1101', 2), ('1110', 1), ('1111', 4)
    ]
    
    BINARY_TO_DNA = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    DNA_TO_BINARY = {v: k for k, v in BINARY_TO_DNA.items()}

    def __init__(self, seed=42):
        self.degree_table = self.DEGREE_TABLE
        random.seed(seed)  # Set the seed for reproducibility

    def split_into_chunks(self, binary_string, chunk_size=4):
        """Splits the input binary string into chunks of specified size."""
        return [binary_string[i:i+chunk_size] for i in range(0, len(binary_string), chunk_size)]

    def generate_droplets(self, chunks):
        """Generates droplets using the given degree table."""
        droplets = []
        chunk_indices = list(range(len(chunks)))
        
        for row in self.degree_table:
            degree = row[1]  # Degree from the table
            selected_indices = random.sample(chunk_indices, min(degree, len(chunks)))
            combined_chunk = self.xor_chunks([chunks[i] for i in selected_indices])
            droplets.append((selected_indices, combined_chunk))
        
        return droplets

    def xor_chunks(self, chunks):
        """XORs multiple chunks together."""
        result = int(chunks[0], 2)
        for chunk in chunks[1:]:
            result ^= int(chunk, 2)
        return format(result, '04b')

    def map_to_dna(self, binary_string):
        """Maps a binary string to a DNA sequence."""
        return ''.join(self.BINARY_TO_DNA[binary_string[i:i+2]] for i in range(0, len(binary_string), 2))

    def encode_dna_fountain(self, binary_data):
        """Encodes binary data using the DNA Fountain algorithm with a given degree table."""
        chunks = self.split_into_chunks(binary_data, 4)
        
        droplets = self.generate_droplets(chunks)
        dna_encoded_droplets = [(indices, self.map_to_dna(data)) for indices, data in droplets]
        
        return dna_encoded_droplets

    def decode_dna_fountain(self, dna_encoded_droplets, num_chunks):
        binary_droplets = [(indices, ''.join(self.DNA_TO_BINARY[char] for char in dna)) for indices, dna in dna_encoded_droplets]
        reconstructed = [None] * num_chunks
        
        for indices, data in binary_droplets:
            if len(indices) == 1:
                reconstructed[indices[0]] = data
        
        for _ in range(num_chunks):
            for indices, data in binary_droplets:
                known_data = [reconstructed[i] for i in indices if reconstructed[i] is not None]
                unknown_indices = [i for i in indices if reconstructed[i] is None]
                
                if len(unknown_indices) == 1 and known_data:
                    xor_result = self.xor_chunks([data] + known_data)
                    reconstructed[unknown_indices[0]] = xor_result
        
        return ''.join(filter(None, reconstructed))



class DNAFountainTester:
    def __init__(self, seed=42):
        self.dna_fountain = DNAFountain(seed)
        self.binary_messages = [
            "01000001101111110000110110100101",
            "11010010101100011100101010101010",
            "10101010111100001111000010101010",
            "00001111000011110000111100001111",
            "11110000111100001111000011110000"
        ]
    
    def run_tests(self):
        for binary_message in self.binary_messages:
            dna_droplets = self.dna_fountain.encode_dna_fountain(binary_message)
            decoded_binary = self.dna_fountain.decode_dna_fountain(dna_droplets, len(self.dna_fountain.split_into_chunks(binary_message, 4)))
            assert decoded_binary == binary_message, f"Test failed! Expected {binary_message}, got {decoded_binary}"
        print("All tests passed! Decoded messages match original.")

if __name__ == "__main__":
    tester = DNAFountainTester()
    tester.run_tests()
