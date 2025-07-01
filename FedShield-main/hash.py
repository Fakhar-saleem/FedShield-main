import hashlib

def calculate_hash(statement):
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the statement
    sha256_hash.update(statement.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_statement = sha256_hash.hexdigest()
    return hashed_statement
def calculate_txt_hash(file_path):
    # Initialize the hash object based on the specified algorithm

    hash_object = hashlib.sha256()

    # Open the file and read it in binary mode
    try:
        with open(file_path, 'rb') as file:
            # Read the file in chunks to avoid loading the entire file into memory
            while chunk := file.read(8192):
                hash_object.update(chunk)
    except FileNotFoundError:
        print("File not found.")
        return None

    # Get the hexadecimal representation of the hash
    file_hash = hash_object.hexdigest()
    return file_hash

