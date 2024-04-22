import bcrypt
import time

# Prompt for the token (password)
password = input("Please enter your password: ").encode()

# Generate a salt with a specific cost factor
# Typical cost factors range from 10 to 14 (default is 12)
cost_factor = 4
salt = bcrypt.gensalt(rounds=cost_factor)

# Measure the time taken to hash the password
start_time = time.time()
hashed_password = bcrypt.hashpw(password, salt)
end_time = time.time()

print(f"Hashed password: {hashed_password}")
print(f"Time taken to hash: {end_time - start_time:.4f} seconds")