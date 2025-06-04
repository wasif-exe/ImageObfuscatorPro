
# ImageObfuscatorPro

**ImageObfuscatorPro** is a Python-based image processing tool designed to apply multi-layered visual obfuscation for purposes such as privacy protection, data augmentation, or creative distortion. It combines gradient overlays, random crops, emoji placement, noise, random texture mixing, image skewing, and compression artifacts into a powerful pipeline that subtly alters images while maintaining visual coherence.

---

## ✨ Features

- 🔍 **Gradient Overlays** (top-down, bottom-up, left-right, right-left) with transparency blending
- 🖼️ **Random Crop Shifts** to simulate jitter or subtle misalignment
- 💥 **Anomaly Injection** using custom transparent PNG elements
- 😂 **Emoji Placement** with randomized position, scale, rotation, and opacity
- 🌀 **Random Image Overlays** that add distractions or blend textures
- 🌫️ **Gaussian Noise** to mimic sensor or environmental noise
- 🎨 **Image Enhancements** (color, contrast, brightness, sharpness)
- 🔄 **Image Skewing** to simulate warping or scanning artifacts
- 📸 **JPEG Compression Artifacts** to mimic quality loss
- 🧹 **EXIF Metadata Stripping** to ensure image privacy
- 📁 **Batch Processing** for all supported image formats in one go

---

## 🗂️ Folder Structure

```bash
ImageObfuscatorPro/
├── original_images/           # Input images (raw images to obfuscate)
├── modified_images/           # Output directory for obfuscated images
├── anomaly_elements/          # PNG elements to inject as "anomalies"
├── emoji_elements/            # PNG emoji icons to randomly overlay
├── random_elements/           # PNGs or JPEGs to overlay as random textures
├── assets/                    # Optional demo visuals or screenshots
├── obfuscator.py              # Main script
└── README.md                  # Project documentation
````

---

## 🛠️ Requirements

This script requires Python 3.7+ and the following Python libraries:

* `Pillow`
* `numpy`

Install them with:

```bash
pip install pillow numpy
```

---

## 🚀 How to Use

1. **Place your input images** in the `original_images/` directory. Supported formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`.

2. **Optional Assets**:

   * Put overlay emojis (PNG, transparent) in `emoji_elements/`.
   * Put "anomalies" or distractor elements (PNG) in `anomaly_elements/`.
   * Add background noise/texture images in `random_elements/`.

3. **Run the script**:

```bash
python obfuscator.py
```

4. **Interactive Prompts**:

   * Whether to add emojis? (yes/no)
   * Whether to add random textures/images? (yes/no)

5. **View results**: Obfuscated images will be saved in `modified_images/` with the prefix `obfuscated_`.

---

## 🧪 Example

> Before & After Comparison

| Original Image               | Obfuscated Image              |
| ---------------------------- | ----------------------------- |
| ![](original_images/random.jpg) | ![](modified_images/obfuscated_random.jpg) |

---

## 📝 Customization

You can tweak any of the following settings directly in the script:

* Emoji placement size/rotation range
* Skew degree and interpolation
* Compression quality range
* Noise level and Gaussian blur radius
* Opacity blending values
* Cropping offset range

All constants are grouped at the top of the script for easy access.

---

## ⚠️ Notes

* All obfuscation steps are random each time the script is run.
* Obfuscation is designed to be **subtle but irreversible**—images still look visually reasonable but lose fine detail.
* This script **does not use AI/ML**—it’s based on traditional image transformation techniques using `Pillow` and `numpy`.

---

## 📄 License

This project is open-source and licensed under the [MIT License](https://choosealicense.com/licenses/mit/). You are free to use, modify, and distribute with attribution.

---

## 🙌 Acknowledgements

Developed by **Syed M Wasif**
🌐 [Portfolio](https://wasif-exe.vercel.app/)
📧 [syedwasifzidane@gmail.com](mailto:syedwasifzidane@gmail.com)

If you use this tool in research, educational projects, or production pipelines, a credit is always appreciated!

