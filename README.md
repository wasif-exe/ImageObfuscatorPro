# ImageObfuscatorPro

**ImageObfuscatorPro** is a powerful Python tool designed to apply layered obfuscation to images for data augmentation, privacy preservation, or creative distortion. It performs subtle transformations like cropping, gradient overlays, emoji insertion, noise addition, skewing, JPEG artifact simulation, and more.

---

## ✨ Features

- 🔍 **Subtle Gradient Overlays** in multiple directions
- 🎯 **Random Crop Shifts** to simulate slight misalignments
- 💥 **Anomaly Injection** (custom elements)
- 😂 **Emoji Placement** with random rotation, scale, and opacity
- 🎨 **Random Image Overlays** as textures or distractions
- 🌫️ **Gaussian Noise** for realistic imperfections
- 🎚️ **Color, Contrast, Brightness, and Sharpness Tweaks**
- 🔄 **Minor Skew Transformations**
- 📸 **JPEG Compression Artifacts Simulation**
- ❌ **EXIF Metadata Stripping**
- 📁 Batch Processing of Multiple Images

---

## 🗂️ Folder Structure

```bash
ImageObfuscatorPro/
├── original_images/           # Input images (to be obfuscated)
├── modified_images/           # Output directory for obfuscated images
├── anomaly_elements/          # PNG elements to inject as "anomalies"
├── emoji_elements/            # PNG emojis to overlay randomly
├── random_elements/           # PNG backgrounds/textures/images to mix in
├── obfuscator.py              # Main obfuscation script
└── README.md
