import bcrypt
import os

# Create a subfolder named 'auth_data' if it doesn't already exist
auth_data_path = 'auth_data'
os.makedirs(auth_data_path, exist_ok=True)

# Prompt for the token
token = input("Please enter the secure token: ").encode()

# Generate a salt and hash the token
salt = bcrypt.gensalt(rounds=4)
hashed_token = bcrypt.hashpw(token, salt)

# Store the hashed token and salt in the 'auth_data' folder
hashed_token_path = os.path.join(auth_data_path, 'hashed_token.txt')
salt_path = os.path.join(auth_data_path, 'salt.txt')

with open(hashed_token_path, 'wb') as f:
    f.write(hashed_token)

with open(salt_path, 'wb') as f:
    f.write(salt)
