import sys
def concatenate_arguments(arguments):
    concatenated_string = ''.join(arguments)
    return concatenated_string

if __name__ == "__main__":
    # Extract command-line arguments excluding the script name
    arguments = sys.argv[1:]

    # Concatenate the arguments without spaces
    result = concatenate_arguments(arguments)

    # Print the concatenated string
    print(result)
