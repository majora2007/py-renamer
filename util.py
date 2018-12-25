# Global variables controlled by Flags
global verbose
verbose = False

def print_info(msg):
    if verbose:
        print(msg)