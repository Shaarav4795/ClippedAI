# ClippedAI - AI-Powered YouTube Shorts Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

**Open-source alternative to OpusClip** - Transform long-form videos into engaging YouTube Shorts automatically using AI-powered transcription, clip detection, and viral title generation. Built on the powerful [clipsai](https://github.com/ClipsAI/clipsai) library.

## Features

- **Smart Clip Detection**: AI identifies the most engaging moments in your videos
- **Auto-Resize**: Automatically crops videos to 9:16 aspect ratio for YouTube Shorts
- **Animated Subtitles**: Clean, bold subtitles with smart styling (white text, yellow for numbers/currency)
- **Viral Title Generation**: AI generates catchy, titles optimized for engagement
- **Transcription Caching**: Save time by reusing existing transcriptions
- **Multiple Video Support**: Process multiple videos in one session
- **Engagement Scoring**: Intelligent clip selection based on content engagement metrics

## Why Choose ClippedAI Over OpusClip?

| Feature | ClippedAI | OpusClip |
| ------- | --------- | -------- |
| **Cost** | 100% Free | $39/month |
| **Privacy** | Local processing | Cloud-based |
| **Customization** | Fully customisable | Limited options |
| **API Keys** | Free (HuggingFace + Groq) | Paid subscriptions |
| **Offline Use** | Works offline (with no auto titles) | Requires internet |
| **Source Code** | Open source | Proprietary |
| **Model Control** | Choose your own models | Fixed models |
| **Transcription Caching** | Save time & money | No caching |

**Perfect for:** Content creators, developers, and anyone who wants professional video editing capabilities without the monthly subscription costs!

## Quick Start

### Prerequisites

- **Python 3.8+** (Tested on 3.11)
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

5. **Create environment file**

   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your API keys:
   nano .env
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

4. **Add the token to your environment file**
   - Edit the `.env` file and replace `your_huggingface_token_here` with your actual token
   - Example: `HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Note**: The first time you run the script, it will download the Pyannote models (~2GB). This may take several minutes depending on your internet connection.

#### Groq API Key (Required for viral titles) - **100% FREE**

1. Sign up at [Groq](https://console.groq.com/) (free tier available)
2. Get your API key from the dashboard
3. Add your API key to the `.env` file where `GROQ_API_KEY=your_groq_api_key_here`

**Cost**: Both API keys are completely free to use!

## Choosing the Right Transcription Model

The script uses Whisper models via `clipsai`. Choose based on your hardware:

### Model Size Comparison

| Model | Size | Speed | Accuracy | RAM Usage | Best For |
|-------|------|-------|----------|-----------|----------|
| `tiny` | 39MB | Very Fast | Low | 1GB | Quick testing, basic accuracy |
| `base` | 74MB | Fast | Medium | 1GB | Good balance, most users |
| `small` | 244MB | Moderate | High | 2GB | Better accuracy, recommended |
| `medium` | 769MB | Slow | Very High | 4GB | High accuracy, good hardware |
| `large-v1` | 1550MB | Very Slow | Excellent | 8GB | Best accuracy, powerful hardware |
| `large-v2` | 1550MB | Very Slow | Excellent | 8GB | Latest model, best results |

### Hardware Recommendations

**For CPU-only systems:**

- 4GB RAM: Use `tiny` or `base`
- 8GB RAM: Use `small` or `medium`
- 16GB+ RAM: Use `large-v1` or `large-v2`

**For GPU systems:**

- Any GPU with 4GB+ VRAM: Use `large-v2` (best results)
- GPU with 2GB VRAM: Use `medium` or `large-v1`

### Changing the Model

The transcription model can be configured via the `TRANSCRIPTION_MODEL` environment variable in your `.env` file:

```
TRANSCRIPTION_MODEL=large-v1  # Options: tiny, base, small, medium, large-v1, large-v2
```

## Project Structure

```
ClippedAI/
├── main.py                 # Main application script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── input/                 # Place your videos here
│   ├── video1.mp4
│   ├── video2.mp4
│   └── *_transcription.pkl # Cached transcriptions (auto-generated)
├── output/                # Generated YouTube Shorts
│   ├── clip1.mp4
│   ├── clip2.mp4
│   └── ...
└── env/                   # Virtual environment (created during setup)
```

## Customization

All key settings can now be configured through the `.env` file or within `main.py` for subtitle styling.

## Usage

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

## Customization

### Font Configuration

The script uses Montserrat Extra Bold for subtitles (from Google Fonts). To change fonts:

1. **Place your preferred font file** in the `fonts/` directory
2. **Edit the font name** in `main.py` line 158:

   ```python
   SUBTITLE_FONT = "Your-Font-Name"
   ```

3. **Update the ASS style definitions** in the `create_animated_subtitles` function to reference the new font

### Environment Variables Configuration

All key settings can now be configured through the `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `HUGGINGFACE_TOKEN` | your_huggingface_token_here | HuggingFace API token for speaker diarization |
| `GROQ_API_KEY` | your_groq_api_key_here | Groq API key for viral title generation |
| `MIN_CLIP_DURATION` | 45 | Minimum duration in seconds for YouTube Shorts |
| `MAX_CLIP_DURATION` | 120 | Maximum duration in seconds for YouTube Shorts |
| `TRANSCRIPTION_MODEL` | medium | Whisper model to use (tiny, base, small, medium, large-v1, large-v2) |
| `ASPECT_RATIO_WIDTH` | 9 | Width for aspect ratio (used with height for video resizing) |
| `ASPECT_RATIO_HEIGHT` | 16 | Height for aspect ratio (used with width for video resizing) |

### Engagement Scoring

The AI uses multiple factors to select the best clips:

- Word density (45% weight)
- Engagement words ratio (30% weight)
- Duration balance (25% weight)

## Troubleshooting

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
5. **Cache transcriptions** to avoid re-processing if testing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license - see the LICENSE file for details.

## Acknowledgments

- [clipsai](https://github.com/ClipsAI/clipsai) - Core video processing library
- [Whisper](https://github.com/openai/whisper) - Speech recognition
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [Groq](https://groq.com/) - AI title generation

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/Shaarav4795/ClippedAI/issues)
- **Discord**: .shaarav4795.

---

**Star this repository** if you find it helpful!

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Shaarav4795/ClippedAI&type=date&legend=top-left)](https://www.star-history.com/#Shaarav4795/ClippedAI&type=date&legend=top-left)
