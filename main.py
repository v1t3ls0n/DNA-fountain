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

import argparse
import logging
from DNAFountainTester import DNAFountainTester

def main():
    """
    Main entry point for the DNA Fountain Tester.
    Parses command-line arguments, configures logging, instantiates the tester, and runs tests.
    """
    parser = argparse.ArgumentParser(description='DNA Fountain Tester')
    parser.add_argument('--log-level', default='DEBUG',
                        help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    args = parser.parse_args()

    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {args.log_level}")

    print(f"Logging level set to: {args.log_level}")
    logging.basicConfig(
        level=numeric_level,
        encoding='utf-8',
        format="[%(levelname)s] %(message)s",
        filename='output.log',
        filemode='w'
    )

    tester = DNAFountainTester(chunk_size=4)
    tester.run_tests()


if __name__ == "__main__":
    main()
