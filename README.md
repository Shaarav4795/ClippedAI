# 🎬 ClippedAI - AI-Powered YouTube Shorts Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

**🚀 Open-source alternative to OpusClip** - Transform long-form videos into engaging YouTube Shorts automatically using AI-powered transcription, clip detection, and viral title generation. Built on the powerful [clipsai](https://github.com/Zulko/clipsai) library.

## ✨ Features

- 🎯 **Smart Clip Detection**: AI identifies the most engaging moments in your videos
- 🎨 **Auto-Resize**: Automatically crops videos to 9:16 aspect ratio for YouTube Shorts
- 📝 **Animated Subtitles**: Clean, bold subtitles with smart styling (white text, yellow for numbers/currency)
- 🚀 **Viral Title Generation**: AI generates catchy, emoji-rich titles optimized for engagement
- 💾 **Transcription Caching**: Save time by reusing existing transcriptions
- 🎪 **Multiple Video Support**: Process multiple videos in one session
- 📊 **Engagement Scoring**: Intelligent clip selection based on content engagement metrics

## 🆚 Why Choose ClippedAI Over OpusClip?

| Feature | ClippedAI | OpusClip |
|---------|-----------|----------|
| **Cost** | 🆓 100% Free | 💰 $39/month |
| **Privacy** | 🔒 Local processing | ☁️ Cloud-based |
| **Customization** | ⚙️ Fully customizable | 🎛️ Limited options |
| **API Keys** | 🆓 Free (HuggingFace + Groq) | 💳 Paid subscriptions |
| **Offline Use** | ✅ Works offline | ❌ Requires internet |
| **Source Code** | 🔓 Open source | 🔒 Proprietary |
| **Model Control** | 🎯 Choose your own models | 🎲 Fixed models |
| **Transcription Caching** | 💾 Save time & money | ❌ No caching |

**💡 Perfect for:** Content creators, developers, and anyone who wants professional video editing capabilities without the monthly subscription costs!

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.11 recommended for best performance)
- **FFmpeg** installed and available in PATH
- **8GB+ RAM** (16GB+ recommended for large models)
- **GPU** (optional but recommended for faster processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shaarav4795/ClippedAI.git
   cd ClippedAI
   ```

2. **Create and activate virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv env
   source env/bin/activate
   
   # On Windows
   python -m venv env
   env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   ```bash
   # macOS (using Homebrew)
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # Windows (using Chocolatey)
   choco install ffmpeg
   
   # Or download from https://ffmpeg.org/download.html
   ```

5. **Configure API Keys**
   ```bash
   # Edit main.py and replace these placeholders:
   HUGGINGFACE_TOKEN = 'your_huggingface_token_here'
   groq_api_key = "your_groq_api_key_here"
   ```

### API Keys Setup

#### HuggingFace Token (Required) - **100% FREE**
1. **Sign up for HuggingFace**
   - Go to [HuggingFace](https://huggingface.co/join) and create a free account

2. **Request access to Pyannote models**
   - Visit [pyannote/speaker-diarization](https://huggingface.co/pyannote/speaker-diarization)
   - Click "Access repository" and accept the terms
   - Visit [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
   - Click "Access repository" and accept the terms
   - Visit [pyannote/segmentation](https://huggingface.co/pyannote/segmentation)
   - Click "Access repository" and accept the terms

3. **Create your API token**
   - Go to [HuggingFace Settings > Access Tokens](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Give it a name (e.g., "ClippedAI")
   - Select "Read" role (minimum required)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again)

4. **Add the token to your code**
   - Replace `'YOUR API KEY HERE'` in `main.py` with your actual token
   - Example: `HUGGINGFACE_TOKEN = 'hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'`

**Note**: The first time you run the script, it will download the Pyannote models (~2GB). This may take several minutes depending on your internet connection.

#### Groq API Key (Required for viral titles) - **100% FREE**
1. Sign up at [Groq](https://console.groq.com/) (free tier available)
2. Get your API key from the dashboard
3. Replace `"YOUR API KEY HERE"` in the `get_viral_title` function

**💰 Cost**: Both API keys are completely free to use!

## 🎯 Choosing the Right Transcription Model

The script uses Whisper models via `clipsai`. Choose based on your hardware:

### Model Size Comparison

| Model | Size | Speed | Accuracy | RAM Usage | Best For |
|-------|------|-------|----------|-----------|----------|
| `tiny` | Very Small | ⚡⚡⚡⚡⚡ | ⭐⭐ | 1GB | Quick testing, basic accuracy |
| `base` | Small | ⚡⚡⚡⚡ | ⭐⭐⭐ | 1GB | Good balance, most users |
| `small` | Medium | ⚡⚡⚡ | ⭐⭐⭐⭐ | 2GB | Better accuracy, recommended |
| `medium` | Large | ⚡⚡ | ⭐⭐⭐⭐⭐ | 4GB | High accuracy, good hardware |
| `large-v1` | Very Large | ⚡ | ⭐⭐⭐⭐⭐ | 8GB | Best accuracy, powerful hardware |
| `large-v2` | Very Large | ⚡ | ⭐⭐⭐⭐⭐ | 8GB | Latest model, best results |

### Hardware Recommendations

**For CPU-only systems:**
- 4GB RAM: Use `tiny` or `base`
- 8GB RAM: Use `small` or `medium`
- 16GB+ RAM: Use `large-v1` or `large-v2`

**For GPU systems:**
- Any GPU with 4GB+ VRAM: Use `large-v2` (best results)
- GPU with 2GB VRAM: Use `medium` or `large-v1`

### Changing the Model

Edit line 47 in `main.py`:
```python
# Change this line to your preferred model
transcriber = Transcriber(model_size="large-v1")  # Options: tiny, base, small, medium, large-v1, large-v2
```

## 📁 Project Structure

```
ClippedAI/
├── main.py                 # Main application script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License with commercial restrictions
├── input/                 # Place your videos here
│   ├── video1.mp4
│   ├── video2.mp4
│   └── *_transcription.pkl # Cached transcriptions (auto-generated)
├── output/                # Generated YouTube Shorts
│   ├── clip1.mp4
│   ├── clip2.mp4
│   └── ...
└── env/                   # Virtual environment (created during setup)

# Website files (for GitHub Pages - can be deleted for local use)
├── index.html             # Website homepage
├── styles.css             # Website styling
├── script.js              # Website interactivity
├── sitemap.xml            # SEO sitemap
├── robots.txt             # Search engine instructions
└── .github/workflows/     # GitHub Pages deployment
```

## 🗑️ Clean Installation (Optional)

If you only want to use ClippedAI locally and don't need the website, you can delete these files:
```bash
# Delete website-related files
rm index.html styles.css script.js sitemap.xml robots.txt
rm -rf .github/
```

**Note**: These files are only needed for the GitHub Pages website at https://shaarav4795.github.io/ClippedAI/. The core functionality works perfectly without them.

## 🎬 Usage

1. **Add your videos** to the `input/` folder
   ```bash
   cp /path/to/your/video.mp4 input/
   ```

2. **Run the script**
   ```bash
   python main.py
   ```

3. **Follow the prompts** to:
   - Match videos with existing transcriptions (if any)
   - Choose how many clips to generate per video
   - Let AI process and create your YouTube Shorts

4. **Find your results** in the `output/` folder

## 🎨 Customization

### Font Configuration

The script uses Montserrat Extra Bold for subtitles. To change fonts:

1. **Install your preferred font** system-wide
2. **Edit the font name** in `main.py` line 158:
   ```python
   font_used = "Your-Font-Name"
   ```

### Clip Duration Settings

Adjust clip length in `main.py`:
```python
MIN_CLIP_DURATION = 45   # Minimum duration in seconds
MAX_CLIP_DURATION = 120  # Maximum duration in seconds
```

### Engagement Scoring

The AI uses multiple factors to select the best clips:
- Word density (45% weight)
- Engagement words ratio (30% weight) 
- Duration balance (25% weight)

## 🔧 Troubleshooting

### Common Issues

**"No module named 'clipsai'"**
```bash
pip install clipsai
```

**"FFmpeg not found"**
- Ensure FFmpeg is installed and in your system PATH
- Restart your terminal after installation

**"CUDA out of memory"**
- Use a smaller transcription model
- Close other GPU-intensive applications
- Reduce batch size if applicable

**"Font not found"**
- Install the required font system-wide
- Or change to a system font in the code

**"API key errors"**
- Verify your API keys are correct
- Check your internet connection
- Ensure you have sufficient API credits

**"HuggingFace access denied"**
- Make sure you've requested access to all three Pyannote repositories
- Wait a few minutes after requesting access before running the script
- Verify your HuggingFace token has "read" permissions

### Performance Tips

1. **Use SSD storage** for faster video processing
2. **Close unnecessary applications** to free up RAM
3. **Use GPU acceleration** if available
4. **Process videos in smaller batches** for large files
5. **Cache transcriptions** to avoid re-processing

## 📊 Performance Benchmarks

| Video Length | Model | Processing Time | RAM Usage |
|--------------|-------|-----------------|-----------|
| 10 minutes | large-v2 | ~15-20 min | 8GB |
| 10 minutes | medium | ~10-15 min | 4GB |
| 10 minutes | small | ~8-12 min | 2GB |
| 10 minutes | base | ~5-8 min | 1GB |

*Times vary based on hardware and video complexity*

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [clipsai](https://github.com/Zulko/clipsai) - Core video processing library
- [Whisper](https://github.com/openai/whisper) - Speech recognition
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [Groq](https://groq.com/) - AI title generation

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Shaarav4795/ClippedAI/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/Shaarav4795/ClippedAI/discussions)
- 📧 **Email**: aryashaarav@icloud.com
- 💬 **Discord**: shaarav4795.

---

⭐ **Star this repository** if you find it helpful!

🔗 **Share with creators** who want to automate their YouTube Shorts workflow!