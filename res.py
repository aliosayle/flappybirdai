from PIL import Image, ImageFilter

# Define the target size
target_size = (40, 40)

# Open the image
try:
    with Image.open("bird.png") as img:
        # Resize the image with antialiasing for smoother results
        resized_img = img.resize(target_size, resample=Image.LANCZOS)
        
        # Save the resized image with the same format as the original
        resized_img.save("bird_resized.png")
        
        print("Image resized and saved as 'bird_resized.png'")
except FileNotFoundError:
    print("Error: 'bird.png' not found. Please check the file name and path.")
except Exception as e:
    print(f"An error occurred: {e}")
