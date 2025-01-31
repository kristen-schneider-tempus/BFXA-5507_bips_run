import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Create final output file to keep track of data from MYB run.')
    parser.add_argument('-u', '--unique', type=str, help='The unique set of data from GBQ search')
    parser.add_argument('-b', '--bips_input', type=str, help='The file used as input for BIPS')
    parser.add_argument('-l', '--bips_input', type=str, help='The file used as input for BIPS')
    parser.add_argument('--output', type=str, help='Output file')
    return parser.parse_args()