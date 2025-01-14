import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw

user="amorima"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
USERS_DIR = os.path.join(BASE_DIR, "files", "users")

def ensure_user_folder_exists(username):
    """Ensure the folder for the active user exists."""
    user_folder = os.path.join(USERS_DIR, username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        print(f"Created folder for user: {user_folder}")
    return user_folder

def crop_to_square(image_path):
    """Crop the uploaded image to a square and return the cropped image."""
    with Image.open(image_path) as img:
        width, height = img.size
        side_length = min(width, height)
        left = (width - side_length) // 2
        top = (height - side_length) // 2
        right = left + side_length
        bottom = top + side_length
        return img.crop((left, top, right, bottom))

def apply_circle_mask(image):
    """Apply a circular mask to the image and return it."""
    size = (200, 200)
    image = image.resize(size, Image.LANCZOS)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    circular_image = Image.new("RGBA", size)
    circular_image.paste(image, (0, 0), mask)
    return circular_image

def upload_and_save_image():
    """Upload an image, save the cropped version, and render it in a circular frame."""
    file_path = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        user_folder = ensure_user_folder_exists(user)
        
       
        cropped_image = crop_to_square(file_path)
        
      
        save_path = os.path.join(user_folder, "profile_picture.png")
        cropped_image.save(save_path)
        print(f"Cropped image saved at: {save_path}")
        
        # Display the circular version of the cropped image
        circular_image = apply_circle_mask(cropped_image)
        display_image(circular_image)

def display_image(image):
    """Display the circular image in the placeholder."""
    ctk_image = ctk.CTkImage(image, size=(100, 100))
    image_label.configure(image=ctk_image, text="")
    image_label.image = ctk_image


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


root = ctk.CTk()
root.title("Guardar avatar")
root.geometry("400x500")

# Circular placeholder frame
placeholder_frame = ctk.CTkFrame(master=root, width=110, height=110, corner_radius=110)
placeholder_frame.pack(pady=30)

# Label for displaying the image
image_label = ctk.CTkLabel(master=placeholder_frame, text="", width=100, height=100, bg_color="#242424")
image_label.place(relx=0.5, rely=0.5, anchor="center")

# Button for uploading the image (centered in the placeholder)
upload_button = ctk.CTkButton(
    master=placeholder_frame,
    text="Mudar",
    command=upload_and_save_image,
    font=ctk.CTkFont(size=10, weight="bold"),
    fg_color="transparent",
    bg_color="transparent",  # Transparent button background
    hover_color="#242424",    # Optional hover effect
    text_color="#FFFFFF",     # Text remains visible
    border_width=1,           # Optional border
    border_color="white",   # Border color matches the placeholder
    width=10,
    height=30
)
upload_button.place(relx=0.5, rely=0.5, anchor="center")

# Run the Tkinter event loop
root.mainloop()