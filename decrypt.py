import cv2
import os

# Load the encrypted image
image_path = "encrypted.png"
if not os.path.exists(image_path):
    print(f"Error: Encrypted image '{image_path}' not found.")
    exit()

img = cv2.imread(image_path)
if img is None:
    print(f"Error: Unable to load image '{image_path}'.")
    exit()

# Read stored password
password_file = "password.txt"
if not os.path.exists(password_file):
    print("Error: Password file not found. Encryption may not have been performed.")
    exit()

with open(password_file, "r") as file:
    correct_password = file.read().strip()

# Get passcode from user
pas = input("Enter passcode for Decryption: ")

if pas == correct_password:
    # Extract message length (3-byte encoding)
    msg_length = int(img[0, 0][0]) * 65536 + int(img[0, 0][1]) * 256 + int(img[0, 0][2])

    # Extract message
    message = ""
    index = 0
    for i in range(1, img.shape[0]):  # Start from (1,0)
        for j in range(img.shape[1]):
            if index < msg_length:
                message += chr(int(img[i, j, 0]))  # Read char from Red channel
                index += 1
            else:
                break
        if index >= msg_length:
            break

    print("Decrypted message:", message)
else:
    print("ERROR: Incorrect passcode. Decryption failed.")
