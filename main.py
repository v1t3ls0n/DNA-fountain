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
