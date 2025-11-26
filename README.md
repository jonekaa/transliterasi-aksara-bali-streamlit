# 🔤 Transliterasi Aksara Bali

A Streamlit web application that uses deep learning to automatically transliterate Balinese script (Aksara Bali) from images into Latin characters. This project leverages YOLO object detection to recognize individual Balinese characters and applies custom transliteration rules to convert them into readable Latin text.

![Balinese Script](https://img.shields.io/badge/Script-Balinese-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-green)

## ✨ Features

- **📸 Image Upload**: Support for JPG, PNG, and JPEG image formats
- **🤖 AI-Powered Detection**: Uses YOLOv8 for accurate character detection
- **🔍 Object Detection Visualization**: View detected characters with bounding boxes
- **📝 Automatic Transliteration**: Converts Balinese script to Latin characters
- **🎯 Smart Character Recognition**: Handles complex Balinese script rules including:
  - Vowel modifiers (taleng, ulu, suku, pepet)
  - Consonant clusters (gantungan)
  - Special characters (adeg-adeg, cecek, surang, bisah, tedong)
  - Line-by-line text processing
- **🖥️ User-Friendly Interface**: Clean and intuitive Streamlit web interface

## 🚀 Demo

1. Upload an image containing Balinese script
2. Click "Transliterate" button
3. View the detected characters with bounding boxes
4. Read the transliterated Latin text output

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- A trained YOLO model file (`best.pt`) in the `models/` directory

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/jonekaa/transliterasi-aksara-bali-streamlit.git
   cd transliterasi-aksara-bali-streamlit
   ```

2. **Install required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the model file exists**

   Make sure you have the trained YOLO model file at:

   ```
   models/best.pt
   ```

## 📦 Dependencies

- **streamlit**: Web application framework
- **ultralytics**: YOLO implementation for object detection
- **opencv-python-headless**: Image processing
- **copy**: Deep copying utilities
- **numpy**: Numerical operations
- **Pillow**: Image handling

## 🎮 Usage

1. **Start the Streamlit application**

   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**

   Open your browser and navigate to:

   ```
   http://localhost:8501
   ```

3. **Upload and transliterate**
   - Click "Browse files" to upload an image containing Balinese script
   - Click the "Transliterate" button
   - View the original image, detected objects, and transliterated text

## 🏗️ Project Structure

```
transliterasi-aksara-bali-streamlit/
├── app.py                    # Main Streamlit application
├── models/
│   └── best.pt              # Trained YOLO model
├── requirements.txt          # Python dependencies
├── .gitattributes           # Git configuration
└── README.md                # Project documentation
```

## 🧠 How It Works

### 1. **Character Detection**

The application uses a YOLOv8 model trained to detect individual Balinese characters in images. Each character is identified with a bounding box and classified into one of many character classes.

### 2. **Line Grouping**

Detected characters are grouped into lines based on their vertical positions using a configurable line tolerance parameter.

### 3. **Sorting & Ordering**

Characters within each line are sorted from left to right, with special handling for diacritical marks (gantungan) that may appear above or below base characters.

### 4. **Transliteration Rules**

The application applies comprehensive transliteration rules to convert Balinese script to Latin characters:

- **Base Characters**: Direct mapping (e.g., `na-rambat` → `na`)
- **Vowel Modifiers**:
  - `taleng` → é/o modifications
  - `ulu` → i modification
  - `suku` → u modification
  - `pepet` → e modification
- **Consonant Clusters**: Gantungan characters insert consonants into the previous syllable
- **Special Markers**:
  - `adeg-adeg` → word separator
  - `cecek-ng-` → ng ending
  - `surang-r-` → r ending
  - `bisah-h-` → h ending
  - `tedong` → double consonant
  - `end` → line break

### 5. **Output Generation**

The transliterated text is displayed line by line in the web interface.

## 🎯 Supported Balinese Characters

The model recognizes various Balinese script elements including:

- **Aksara Wianjana** (consonants): ka, ga, nga, ca, ja, nya, ta, da, na, pa, ba, ma, ya, ra, la, wa, sa, ha
- **Aksara Suara** (vowels): a, i, u, e, o
- **Pangangge Suara** (vowel diacritics): taleng, ulu, suku, pepet
- **Pangangge Tengenan** (medial consonants): gantungan series
- **Adeg-adeg**: syllable terminator
- **Cecek, Surang, Bisah**: final consonant markers
- **Tedong**: consonant doubling marker

## 🔧 Configuration

### Model Parameters

- **IOU Threshold**: 0.5 (configured in `app.py`)
- **Line Tolerance**: 75 pixels (for grouping characters into lines)
- **X Tolerance**: 1 pixel (for sorting characters)

### Customization

You can modify these parameters in `app.py`:

```python
results = model.predict(image, iou=0.5)  # Adjust IOU threshold
line_tolerance=75  # Adjust line grouping sensitivity
x_tolerance=1  # Adjust horizontal sorting sensitivity
```

## 🐛 Error Handling

The application includes error handling for:

- Invalid or corrupted images
- Images without detectable Balinese script
- Transliteration failures

When an error occurs, a user-friendly error message is displayed: "Maaf, gambar tidak bisa di transliterasi!" (Sorry, the image cannot be transliterated!)

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Improve the model**: Train with more diverse Balinese script samples
2. **Enhance transliteration rules**: Add support for more complex character combinations
3. **UI improvements**: Enhance the Streamlit interface
4. **Documentation**: Improve code comments and documentation
5. **Bug fixes**: Report and fix bugs

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available for educational and research purposes.

## 🙏 Acknowledgments

- **Balinese Script**: Traditional writing system of the Balinese language
- **Ultralytics YOLO**: State-of-the-art object detection framework
- **Streamlit**: Excellent framework for building ML web applications
- **OpenCV**: Powerful computer vision library

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

## 🔮 Future Enhancements

- [ ] Support for batch image processing
- [ ] Export transliteration results to text files
- [ ] Real-time camera input support
- [ ] Mobile-responsive design
- [ ] Multi-language interface (Indonesian/English)
- [ ] Confidence scores for each detected character
- [ ] Alternative transliteration suggestions
- [ ] Support for more Balinese script variations
- [ ] API endpoint for integration with other applications

---

**Made with ❤️ for preserving and digitizing Balinese cultural heritage**
