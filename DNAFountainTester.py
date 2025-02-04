import logging
from DNAFountain import DNAFountain

class DNAFountainTester:
    """
    DNAFountainTester runs tests on the DNAFountain encoding and decoding process.
    It uses predefined binary messages to verify that encoding to DNA and decoding back to binary works.
    """

    def __init__(self, chunk_size=4):
        """
        Initialize the tester with a fixed chunk size and a list of binary messages.

        Args:
            chunk_size (int): The size (in bits) of each data chunk.
        """
        self.chunk_size = chunk_size
        self.binary_messages = [
            "01000001101011110000010110100101",
            # "01010011110001001110011001001001",
            # "01111000010010100110110001001110",
            # "10001101110111100111000000111100",
            # "11111110110010010001010110011110",
            # "10001000100001011011111011101011",   
            # "01011010010100001110000110110110",
            # "11101000111011000001001101001100",
            # "01101110000100001110000001110101",
            # "00100110011110010110101100100010",
            # "10001010111101010000001001001011",
            # "01010111010110011011001101010010",
        ]

    def run_tests(self):
        """
        Run tests on all predefined binary messages by encoding them into DNA and decoding back.
        Logs detailed information for each step.
        """
        msg = "[TEST] Initializing DNAFountain with chunk_size={}...".format(self.chunk_size) + "\n"
        print(msg)
        logging.info(msg)

        self.dna_fountain = DNAFountain(chunk_size=self.chunk_size)
        passed = True

        for binary_message in self.binary_messages:
            msg = "[TEST] Testing binary message: {}".format(binary_message)
            print(msg)
            logging.info(msg)

            if len(binary_message) % self.chunk_size != 0:
                msg = "[ERROR] Message length is not a multiple of chunk size. Skipping this message."
                print(msg)
                logging.error(msg)
                continue

            full_dna_message = self.dna_fountain.encode_message_to_dna(binary_message)
            decoded_binary_from_full = self.dna_fountain.decode_message_from_dna(
                full_dna_message,
                len(binary_message) // self.chunk_size
            )

            msg = "[TEST] Full DNA encoded message: {}".format(full_dna_message)
            print(msg)
            logging.info(msg)

            msg = "[TEST] Decoded binary message: {}".format(decoded_binary_from_full)
            print(msg)
            logging.info(msg)

            if decoded_binary_from_full != binary_message:
                msg = "[ERROR] Decoding failed for this message (full DNA string approach)."
                print(msg)
                logging.error(msg)
                passed = False
                break


        if passed:
            msg = "[TEST] ✅ All tests passed!"
            print(msg)
            logging.info(msg)
        else:
            msg = "[TEST] ❌ Some tests failed."
            print(msg)
            logging.error(msg)
