import hashlib

def calculate_hash(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    return sha256_hash.hexdigest()

# Example Usage
password = "mypassword123"  # Replace with your actual password
hashed_password = calculate_hash(password)
print("Hashed Password:", hashed_password)
