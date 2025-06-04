from PIL import Image, ImageDraw, ImageOps, ImageEnhance
import os
import random
import numpy as np
import tempfile

# --- Configuration ---
INPUT_DIR = "original_images"
OUTPUT_DIR = "modified_images"
ANOMALY_ELEMENTS_DIR = "anomaly_elements"
EMOJI_ELEMENTS_DIR = "emoji_elements"
RANDOM_IMAGE_ELEMENTS_DIR = "random_elements"

# Increased intensity for existing methods
MIN_CROP_PIXELS = 5
MAX_CROP_PIXELS = 15
GRADIENT_MIN_OPACITY = 0.10
GRADIENT_MAX_OPACITY = 0.25

# Increased intensity for anomaly insertion
ANOMALY_MIN_SCALE_FACTOR = 0.10
ANOMALY_MAX_SCALE_FACTOR = 0.30
ANOMALY_MIN_OPACITY = 0.20
ANOMALY_MAX_OPACITY = 0.40
ANOMALY_ADD_CHANCE = 0.8
MAX_ANOMALIES_PER_IMAGE = 3

# Configuration for noise/grain
NOISE_MIN_STRENGTH = 0.01
NOISE_MAX_STRENGTH = 0.04

# Configuration for emojis (Increased visibility and added one more)
EMOJI_MIN_SCALE_FACTOR = 0.03
EMOJI_MAX_SCALE_FACTOR = 0.15
EMOJI_MIN_OPACITY = 0.50
EMOJI_MAX_OPACITY = 0.90
EMOJI_ADD_CHANCE = 1
MAX_EMOJIS_PER_IMAGE = 3

# Configuration for new random image elements
RANDOM_IMAGE_MIN_SCALE_FACTOR = 0.15
RANDOM_IMAGE_MAX_SCALE_FACTOR = 0.70
RANDOM_IMAGE_MIN_OPACITY = 0.05
RANDOM_IMAGE_MAX_OPACITY = 0.20
RANDOM_IMAGE_ADD_CHANCE = 1
MAX_RANDOM_IMAGES_PER_IMAGE = 1

# New configurations for additional obfuscation methods
COLOR_ADJUST_CHANCE = 0.6
HUE_SAT_BRIGHT_MAX_FACTOR = 0.05
SHARPNESS_MAX_FACTOR = 0.05

SKEW_ADD_CHANCE = 0.4
MAX_SKEW_ANGLE = 0.02

COMPRESSION_ARTIFACT_CHANCE = 0.7
JPEG_MIN_QUALITY = 75
JPEG_MAX_QUALITY = 85

# New: Configuration for element placement margin
ELEMENT_PLACEMENT_MARGIN_FACTOR = 0.15 # 15% margin from edges (e.g., place in central 70% of image)
# --- End Configuration ---

def apply_subtle_gradient(image):
    """Applies a random subtle gradient overlay to an image."""
    img_rgba = image.convert("RGBA")
    width, height = img_rgba.size
    gradient_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient_layer)

    base_color = random.randint(180, 240)
    color1 = (base_color, base_color, base_color, 0)
    color2 = (random.randint(max(0, base_color - 30), min(255, base_color + 30)),
              random.randint(max(0, base_color - 30), min(255, base_color + 30)),
              random.randint(max(0, base_color - 30), min(255, base_color + 30)), 0)

    direction = random.choice(['horizontal', 'vertical', 'diagonal_down', 'diagonal_up'])

    for i in range(max(width, height)):
        alpha_val = int(random.uniform(GRADIENT_MIN_OPACITY, GRADIENT_MAX_OPACITY) * 255)
        
        r = int(color1[0] + (color2[0] - color1[0]) * i / max(width, height))
        g = int(color1[1] + (color2[1] - color1[1]) * i / max(width, height))
        b = int(color1[2] + (color2[2] - color1[2]) * i / max(width, height))
        
        current_fill = (r, g, b, alpha_val)

        if direction == 'horizontal':
            if i < width: draw.line(((i, 0), (i, height)), fill=current_fill)
        elif direction == 'vertical':
            if i < height: draw.line(((0, i), (width, i)), fill=current_fill)
        elif direction == 'diagonal_down':
            if i < width: draw.line(((i, 0), (0, i)), fill=current_fill)
            if i < height: draw.line(((width, i), (i, height)), fill=current_fill)
        elif direction == 'diagonal_up':
            if i < width: draw.line(((i, height), (0, height - i)), fill=current_fill)
            if i < height: draw.line(((width, height - i), (i, 0)), fill=current_fill)

    return Image.alpha_composite(img_rgba, gradient_layer)

def apply_minor_crop_shift(image):
    """Crops the image randomly inward from all sides."""
    width, height = image.size
    pixels_to_crop = random.randint(MIN_CROP_PIXELS, MAX_CROP_PIXELS)

    new_width = width - 2 * pixels_to_crop
    new_height = height - 2 * pixels_to_crop

    if new_width <= 0 or new_height <= 0:
        print(f"Warning: Image {width}x{height} too small for crop of {pixels_to_crop} pixels. Skipping crop.")
        return image

    left = pixels_to_crop
    top = pixels_to_crop
    right = width - pixels_to_crop
    bottom = height - pixels_to_crop

    return image.crop((left, top, right, bottom))

def add_subtle_element(main_image, element_path, min_scale, max_scale, min_opacity, max_opacity):
    """Adds a subtle element (anomaly, emoji, or random image) to the main image."""
    try:
        element_image = Image.open(element_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Element image not found: {element_path}. Skipping insertion.")
        return main_image

    main_width, main_height = main_image.size
    element_original_width, element_original_height = element_image.size

    scale_factor = random.uniform(min_scale, max_scale)
    new_element_width = int(main_width * scale_factor)

    if element_original_width == 0:
        print(f"Warning: Element image '{element_path}' has zero width. Skipping insertion.")
        return main_image

    new_element_height = int(element_original_height * (new_element_width / element_original_width))

    if new_element_width <= 0 or new_element_height <= 0:
        print(f"Warning: Element image '{element_path}' became too small after scaling. Skipping insertion.")
        return main_image

    element_image = element_image.resize((new_element_width, new_element_height), Image.Resampling.LANCZOS)
    rotation_angle = random.uniform(-180, 180)
    element_image = element_image.rotate(rotation_angle, expand=True, resample=Image.Resampling.BICUBIC)

    alpha_channel = element_image.getchannel('A')
    alpha_data = list(alpha_channel.getdata())
    opacity_factor = random.uniform(min_opacity, max_opacity)
    new_alpha_data = [int(p * opacity_factor) for p in alpha_data]
    alpha_channel.putdata(new_alpha_data)
    element_image.putalpha(alpha_channel)

    # Calculate valid placement range based on margin
    min_x = int(main_width * ELEMENT_PLACEMENT_MARGIN_FACTOR)
    max_x = int(main_width * (1 - ELEMENT_PLACEMENT_MARGIN_FACTOR)) - element_image.width

    min_y = int(main_height * ELEMENT_PLACEMENT_MARGIN_FACTOR)
    max_y = int(main_height * (1 - ELEMENT_PLACEMENT_MARGIN_FACTOR)) - element_image.height

    # Ensure bounds are valid (element isn't larger than the allowed placement area)
    if max_x < min_x: max_x = min_x # Clamp if element is too wide
    if max_y < min_y: max_y = min_y # Clamp if element is too tall

    paste_x = random.randint(min_x, max_x)
    paste_y = random.randint(min_y, max_y)

    temp_layer = Image.new("RGBA", main_image.size, (0, 0, 0, 0))
    temp_layer.paste(element_image, (paste_x, paste_y), element_image)

    return Image.alpha_composite(main_image.convert("RGBA"), temp_layer)

def add_random_noise(image):
    """Adds subtle random (Gaussian) noise to the image."""
    img_np = np.array(image.convert("RGB"))
    noise_strength = random.uniform(NOISE_MIN_STRENGTH, NOISE_MAX_STRENGTH)
    noise = np.random.normal(0, noise_strength * 255, img_np.shape)
    noisy_img_np = img_np + noise
    noisy_img_np = np.clip(noisy_img_np, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img_np)

def apply_color_manipulation(image):
    """Applies subtle random adjustments to color, brightness, contrast, and sharpness."""
    if random.random() < COLOR_ADJUST_CHANCE:
        # Randomly adjust Color
        color_factor = 1.0 + random.uniform(-HUE_SAT_BRIGHT_MAX_FACTOR, HUE_SAT_BRIGHT_MAX_FACTOR)
        image = ImageEnhance.Color(image).enhance(color_factor)

        # Randomly adjust Brightness
        brightness_factor = 1.0 + random.uniform(-HUE_SAT_BRIGHT_MAX_FACTOR, HUE_SAT_BRIGHT_MAX_FACTOR)
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)

        # Randomly adjust Contrast
        contrast_factor = 1.0 + random.uniform(-HUE_SAT_BRIGHT_MAX_FACTOR, HUE_SAT_BRIGHT_MAX_FACTOR)
        image = ImageEnhance.Contrast(image).enhance(contrast_factor)
        
        # Randomly adjust Sharpness
        sharpness_factor = 1.0 + random.uniform(-SHARPNESS_MAX_FACTOR, SHARPNESS_MAX_FACTOR)
        image = ImageEnhance.Sharpness(image).enhance(sharpness_factor)

    return image

def apply_minor_skew(image):
    """Applies a subtle random skew to the image."""
    if random.random() < SKEW_ADD_CHANCE:
        width, height = image.size
        skew_direction = random.choice(['x', 'y'])
        skew_angle = random.uniform(-MAX_SKEW_ANGLE, MAX_SKEW_ANGLE)

        if skew_direction == 'x':
            transform_matrix = (1, skew_angle, 0, 0, 1, 0)
        else:
            transform_matrix = (1, 0, 0, skew_angle, 1, 0)
        
        image = image.transform(image.size, Image.AFFINE, transform_matrix, resample=Image.Resampling.BICUBIC)

    return image

def introduce_compression_artifacts(image):
    """Temporarily saves as JPEG with lower quality to introduce artifacts, then re-opens."""
    if random.random() < COMPRESSION_ARTIFACT_CHANCE:
        temp_fd, temp_path = tempfile.mkstemp(suffix=".jpg")
        os.close(temp_fd)

        try:
            quality = random.randint(JPEG_MIN_QUALITY, JPEG_MAX_QUALITY)
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            image.save(temp_path, quality=quality, optimize=True)
            
            image = Image.open(temp_path).copy()

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    return image

def strip_exif_data(image):
    """Removes EXIF data from an image."""
    data = list(image.getdata())
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(data)
    return new_image

def process_images(add_emojis, add_random_images):
    """Main function to process images."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    anomaly_files = []
    if os.path.exists(ANOMALY_ELEMENTS_DIR):
        anomaly_files = [os.path.join(ANOMALY_ELEMENTS_DIR, f)
                         for f in os.listdir(ANOMALY_ELEMENTS_DIR)
                         if f.lower().endswith(('.png'))]

    emoji_files = []
    if add_emojis and os.path.exists(EMOJI_ELEMENTS_DIR):
        emoji_files = [os.path.join(EMOJI_ELEMENTS_DIR, f)
                       for f in os.listdir(EMOJI_ELEMENTS_DIR)
                       if f.lower().endswith(('.png'))]

    random_image_files = []
    if add_random_images and os.path.exists(RANDOM_IMAGE_ELEMENTS_DIR):
        random_image_files = [os.path.join(RANDOM_IMAGE_ELEMENTS_DIR, f)
                              for f in os.listdir(RANDOM_IMAGE_ELEMENTS_DIR)
                              if f.lower().endswith(('.png'))]


    if not anomaly_files:
        print(f"Warning: No PNG anomaly elements found in '{ANOMALY_ELEMENTS_DIR}'. Anomaly insertion will be skipped.")
    if add_emojis and not emoji_files:
        print(f"Warning: No PNG emoji elements found in '{EMOJI_ELEMENTS_DIR}'. Emoji insertion will be skipped.")
    if add_random_images and not random_image_files:
        print(f"Warning: No PNG random image elements found in '{RANDOM_IMAGE_ELEMENTS_DIR}'. Random image insertion will be skipped.")

    for filename in os.listdir(INPUT_DIR):
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.isfile(filepath) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            try:
                img = Image.open(filepath)
                print(f"Processing '{filename}'...")

                # Step 1: Apply Minor Crop Shift
                img = apply_minor_crop_shift(img)
                
                # Step 2: Apply Subtle Gradient Overlay
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                img = apply_subtle_gradient(img)

                # Step 3: Add Multiple Subtle Anomalies (randomly)
                if anomaly_files:
                    num_anomalies_to_add = random.randint(0, MAX_ANOMALIES_PER_IMAGE)
                    for _ in range(num_anomalies_to_add):
                        if random.random() < ANOMALY_ADD_CHANCE:
                            chosen_anomaly = random.choice(anomaly_files)
                            img = add_subtle_element(img, chosen_anomaly,
                                                     ANOMALY_MIN_SCALE_FACTOR, ANOMALY_MAX_SCALE_FACTOR,
                                                     ANOMALY_MIN_OPACITY, ANOMALY_MAX_OPACITY)

                # Step 4: Add Random Emojis
                if add_emojis and emoji_files:
                    num_emojis_to_add = random.randint(0, MAX_EMOJIS_PER_IMAGE)
                    for _ in range(num_emojis_to_add):
                        if random.random() < EMOJI_ADD_CHANCE:
                            chosen_emoji = random.choice(emoji_files)
                            img = add_subtle_element(img, chosen_emoji,
                                                     EMOJI_MIN_SCALE_FACTOR, EMOJI_MAX_SCALE_FACTOR,
                                                     EMOJI_MIN_OPACITY, EMOJI_MAX_OPACITY)

                # Step 5: Add Random Images
                if add_random_images and random_image_files:
                    num_random_images_to_add = random.randint(0, MAX_RANDOM_IMAGES_PER_IMAGE)
                    for _ in range(num_random_images_to_add):
                        if random.random() < RANDOM_IMAGE_ADD_CHANCE:
                            chosen_random_image = random.choice(random_image_files)
                            img = add_subtle_element(img, chosen_random_image,
                                                     RANDOM_IMAGE_MIN_SCALE_FACTOR, RANDOM_IMAGE_MAX_SCALE_FACTOR,
                                                     RANDOM_IMAGE_MIN_OPACITY, RANDOM_IMAGE_MAX_OPACITY)

                # Step 6: Add Random Noise/Grain
                img = add_random_noise(img)

                # Step 7: Apply Color Manipulation
                img = apply_color_manipulation(img)

                # Step 8: Apply Minor Skew
                img = apply_minor_skew(img)

                # Step 9: Introduce Compression Artifacts
                img = introduce_compression_artifacts(img)
                
                # Step 10: Strip EXIF data
                img = strip_exif_data(img)

                # Determine output format and filename
                base_name, ext = os.path.splitext(filename)
                output_ext = ".png" if img.mode == 'RGBA' else ext.lower()
                output_filepath = os.path.join(OUTPUT_DIR, f"obfuscated_{base_name}{output_ext}")

                # Save the modified image
                if output_ext in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(output_filepath)
                print(f"Saved modified '{filename}' to '{output_filepath}'")

            except Exception as e:
                print(f"Error processing '{filename}': {e}")
        else:
            print(f"Skipping non-image file or directory: '{filename}'")

# --- Run the program ---
if __name__ == "__main__":
    print("Starting image obfuscation...")
    add_emojis_input = input("Do you want to add random emojis to the images? (yes/no): ").lower()
    add_emojis = (add_emojis_input == 'yes' or add_emojis_input == 'y')

    add_random_images_input = input("Do you want to add random background/texture images? (yes/no): ").lower()
    add_random_images = (add_random_images_input == 'yes' or add_random_images_input == 'y')

    process_images(add_emojis, add_random_images)
    print("Image obfuscation complete.")