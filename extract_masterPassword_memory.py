import re
import sys

def is_possible_password(line):
    # Define criteria for a password
    min_length = 12
    max_length = 25  # Adjust as needed
    
    # Check length
    if not (min_length <= len(line) <= max_length):
        return False

    # Check if it contains a mix of letters, numbers, or symbols
    if not re.search(r'[A-Za-z]', line) or not re.search(r'\d|\W', line):
        return False
    
    # Optional: Exclude common non-password lines (adjust as needed)
    common_exclusions = ["null", "error", "unknown", "failure"]
    if any(term in line.lower() for term in common_exclusions):
        return False

    return True

def find_repeated_passwords(file_path,repeatedWords):
    line_counts = {}

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = line.strip()
            if is_possible_password(line):
                if line in line_counts:
                    line_counts[line] += 1
                else:
                    line_counts[line] = 1
    repeated_passwords = {line: count for line, count in line_counts.items() if count > int(repeatedWords) }

    return repeated_passwords

def save_to_wordlist(wordlist_path, repeated_passwords):
    with open(wordlist_path, 'w', encoding='utf-8') as wordlist_file:
        for password in repeated_passwords:
            wordlist_file.write(password + '\n')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Ask the user for a file path if none is provided
        file_path = input("Enter the path to the text file: ").strip()
        
    wordlist_path = "wordlist.txt"
    try:
        repeatedWords = input("How much should a word be repeated in the dump file to appear in the wordlist?(0 is recomended but will create a bigger wordlist): ").strip()
        repeated_passwords = find_repeated_passwords(file_path,repeatedWords)
            # Save results to a wordlist file
        save_to_wordlist(wordlist_path, repeated_passwords)
        

        with open(wordlist_path, 'r') as fp:
            lines = len(fp.readlines())

        print(f"\nA wordlist was created and saved to {wordlist_path} and has {lines} total words")
            
    except:
        print("Error - Did you write the name of the file correctly?")

