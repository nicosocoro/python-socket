import argparse

def get_args(): 
    parser = argparse.ArgumentParser(description="Basic Socket client example")
    parser.add_argument("--socket", required=True, choices=['tcp', 'unix'], help="Socket type")
    return parser.parse_args()