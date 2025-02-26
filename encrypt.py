import cv2
import os

# Load the original image
image_path = "mypic.jfif"  # Ensure the image exists
if not os.path.exists(image_path):
    print(f"Error: Image '{image_path}' not found.")
    exit()

img = cv2.imread(image_path)
if img is None:
    print(f"Error: Unable to load image '{image_path}'.")
    exit()

# Get message and passcode from user
msg = input("Enter secret message: ")
password = input("Enter a passcode for decryption: ")

# Save password to a file
with open("password.txt", "w") as file:
    file.write(password)

# Convert message length into three separate bytes
msg_length = len(msg)
if msg_length > 16777215:  # Max value for 3 bytes (24-bit encoding)
    print("Error: Message is too long for this image!")
    exit()

# Store message length in the first pixel
img[0, 0] = [msg_length // 65536, (msg_length // 256) % 256, msg_length % 256]

# Embed the message in the red channel of pixels
index = 0
for i in range(1, img.shape[0]):  # Start embedding from (1,0)
    for j in range(img.shape[1]):
        if index < msg_length:
            img[i, j, 0] = ord(msg[index])  # Store character in Red channel
            index += 1
        else:
            break
    if index >= msg_length:
        break

# Save and display the steganographic image
cv2.imwrite("encrypted.png", img)
os.system("start encrypted.png")  # Opens the image (Windows)
print("Message successfully embedded in 'encrypted.png'.")
