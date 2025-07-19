import warnings
warnings.filterwarnings("ignore", message="Model was trained with pyannote.audio")
warnings.filterwarnings("ignore", message="Model was trained with torch")
warnings.filterwarnings("ignore", message="Lightning automatically upgraded")
warnings.filterwarnings("ignore", message="SymbolDatabase.GetPrototype() is deprecated")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

import os
import pickle
# Suppress FFmpeg warnings
os.environ['FFREPORT'] = 'file=ffmpeg.log:level=32'  # Only show errors, not warnings
# Suppress HuggingFace tokenizers parallelism warnings
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import nltk
from clipsai import Transcriber, ClipFinder, resize, MediaEditor, AudioVideoFile
from clipsai.clip.clip import Clip
import subprocess
import json
import tempfile
import sys

nltk.download('punkt')

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
HUGGINGFACE_TOKEN = 'YOUR API KEY HERE'  # <-- User's actual token
MIN_CLIP_DURATION = 45  # Minimum duration in seconds for YouTube Shorts
MAX_CLIP_DURATION = 120  # Maximum duration in seconds for YouTube Shorts

def get_transcription_file_path(input_path):
    """Generate the transcription file path based on input video path"""
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(INPUT_DIR, f"{base_name}_transcription.pkl")

def load_existing_transcription(transcription_path):
    """Load existing transcription if it exists"""
    if os.path.exists(transcription_path):
        print(f"Found existing transcription: {transcription_path}")
        try:
            with open(transcription_path, 'rb') as f:
                transcription = pickle.load(f)
            print("Successfully loaded existing transcription!")
            return transcription
        except Exception as e:
            print(f"Error loading existing transcription: {e}")
            return None
    return None

def save_transcription(transcription, transcription_path):
    """Save transcription to file (both .pkl and .json)"""
    import json
    try:
        with open(transcription_path, 'wb') as f:
            pickle.dump(transcription, f)
        print(f"Transcription saved to: {transcription_path}")
        # Save as JSON as well
        json_path = os.path.splitext(transcription_path)[0] + '.json'
        try:
            # Try to use to_dict() if available
            if hasattr(transcription, 'to_dict'):
                data = transcription.to_dict()
            # Try to use get_word_info() if available (common for transcript objects)
            elif hasattr(transcription, 'get_word_info'):
                data = transcription.get_word_info()
            else:
                data = transcription  # fallback
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(data, jf, ensure_ascii=False, indent=2)
            print(f"Transcription also saved as JSON to: {json_path}")
        except Exception as je:
            print(f"Error saving transcription as JSON: {je}")
    except Exception as e:
        print(f"Error saving transcription: {e}")

def transcribe_with_progress(audio_file_path, transcriber):
    """Transcribe with progress tracking"""
    print('Transcribing video...')
    
    # Get video duration for progress calculation
    try:
        probe_cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', audio_file_path]
        duration = float(subprocess.check_output(probe_cmd).decode().strip())
        print(f"Video duration: {duration:.2f} seconds")
    except:
        duration = 0
        print("Could not determine video duration for progress tracking")
    
    # Custom progress callback
    def progress_callback(current_time):
        if duration > 0:
            progress = (current_time / duration) * 100
            print(f"Transcription progress: {progress:.1f}% ({current_time:.1f}s / {duration:.1f}s)")
        else:
            print(f"Transcription progress: {current_time:.1f}s processed")
    
    # For now, we'll use a simple approach since clipsai doesn't expose progress directly
    # You can enhance this by modifying the clipsai library or using a different approach
    print("Starting transcription (progress updates may be limited)...")
    transcription = transcriber.transcribe(audio_file_path=audio_file_path, iso6391_lang_code='en')
    print("Transcription completed!")
    return transcription

def create_animated_subtitles(video_path, transcription, clip, output_path):
    """
    Create clean, bold subtitles matching the provided style: white bold for text, yellow bold for numbers/currency, no effects, TOP CENTER.
    """
    print('Creating styled subtitles...')
    
    # Get word info for the clip
    word_info = [w for w in transcription.get_word_info() if w["start_time"] >= clip.start_time and w["end_time"] <= clip.end_time]
    if not word_info:
        print('No word-level transcript found for the clip. Skipping subtitles.')
        return video_path
    
    # Build cues: group words into phrases of max 25 chars
    cues = []
    current_cue = {
        'words': [],
        'start_time': None,
        'end_time': None
    }
    
    for w in word_info:
        word = w["word"]
        start_time = w["start_time"] - clip.start_time
        end_time = w["end_time"] - clip.start_time
        
        should_start_new = False
        if current_cue['start_time'] is None:
            should_start_new = True
        elif len(' '.join(current_cue['words']) + ' ' + word) > 25:
            should_start_new = True
        elif start_time - current_cue['end_time'] > 0.5:
            should_start_new = True
        
        if should_start_new:
            if current_cue['words']:
                cues.append({
                    'start': current_cue['start_time'],
                    'end': current_cue['end_time'],
                    'text': ' '.join(current_cue['words'])
                })
            current_cue = {
                'words': [word],
                'start_time': start_time,
                'end_time': end_time
            }
        else:
            current_cue['words'].append(word)
            current_cue['end_time'] = end_time
    if current_cue['words']:
        cues.append({
            'start': current_cue['start_time'],
            'end': current_cue['end_time'],
            'text': ' '.join(current_cue['words'])
        })
    
    # Determine font used and print to console
    font_used = "Montserrat-ExtraBold"
    print(f"Subtitles will use font: {font_used}")
    print("NOTE: Ensure 'Montserrat-ExtraBold' font is installed in your system-wide font directory (e.g., /Library/Fonts on macOS).")

    # Write ASS subtitle file with clean, bold styling at the TOP CENTER
    ass_file = os.path.abspath(os.path.join(OUTPUT_DIR, 'temp_subtitles.ass'))
    with open(ass_file, 'w', encoding='utf-8') as f:
        f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Montserrat-ExtraBold,80,&H00FFFFFF,&H000000FF,&H40000000,&HFF000000,-1,0,0,0,100,100,2,0,1,15,0,8,30,30,120,1
Style: Yellow,Montserrat-ExtraBold,80,&H0000FFFF,&H000000FF,&H40000000,&HFF000000,-1,0,0,0,100,100,2,0,1,15,0,8,30,30,120,1
Style: Fallback,Arial Rounded MT Bold,80,&H00FFFFFF,&H000000FF,&H40000000,&HFF000000,-1,0,0,0,100,100,2,0,1,15,0,8,30,30,120,1
Style: FallbackYellow,Arial Rounded MT Bold,80,&H0000FFFF,&H000000FF,&H40000000,&HFF000000,-1,0,0,0,100,100,2,0,1,15,0,8,30,30,120,1
Style: Fallback2,Arial Black,80,&H00FFFFFF,&H000000FF,&H40000000,&HFF000000,-1,0,0,0,100,100,2,0,1,15,0,8,30,30,120,1
Style: Fallback2Yellow,Arial Black,80,&H0000FFFF,&H000000FF,&H40000000,&HFF000000,-1,0,0,0,100,100,2,0,1,15,0,8,30,30,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
        for cue in cues:
            start = ass_time(cue['start'])
            end = ass_time(cue['end'])
            words = cue['text'].split()
            line = ''
            for w in words:
                if any(char.isdigit() for char in w) or ('$' in w) or (',' in w and w.replace(',', '').isdigit()):
                    line += f'{{\\rYellow}}{w} '
                else:
                    line += f'{w} '
            line = line.strip()
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{line}\n")
    
    final_output = output_path.replace('.mp4', '_with_subtitles.mp4')
    # Use absolute, forward-slash paths for ffmpeg (cross-platform)
    abs_video_path = os.path.abspath(video_path)
    abs_final_output = os.path.abspath(final_output)
    ass_file_ffmpeg = ass_file.replace("\\", "/")
    ffmpeg_cmd = [
        'ffmpeg', '-i', abs_video_path,
        '-vf', f'ass={ass_file_ffmpeg}',
        '-c:a', 'copy',
        '-y',
        abs_final_output
    ]
    try:
        result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        os.remove(ass_file)
        print(f'Styled subtitles added successfully!')
        return abs_final_output
    except subprocess.CalledProcessError as e:
        print(f'Error adding subtitles: {e}')
        print(f'FFmpeg stderr: {e.stderr.decode()}')
        print(f'FFmpeg stdout: {e.stdout.decode()}')
        return video_path

def ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centisecs = int((seconds % 1) * 100)
    return f"{hours:d}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

def get_viral_title(transcript_text, groq_api_key):
    import requests
    examples = [
        "She was almost dead 😵", "He made $1,000,000 in 1 hour 💸", "This changed everything... 😲", "They couldn't believe what happened! 😱", "He risked it all for this 😬", "She said YES! 💍", "He lost everything in seconds 😢", "The offer that shocked everyone 🤯", "He walked away with $500,000 🤑", "She turned down the deal! 🙅‍♀️", "He quit his job for this 😳", "She broke the record! 🏆", "He lost it all in Vegas 🎰", "She found out the truth 😳", "He got a second chance 🙌", "She saved his life 🦸‍♀️", "He was left speechless 😶", "She made history 📚", "He got the golden buzzer! 🔔", "She walked away a millionaire 💰", "He faced his fears 😨", "She got the surprise of her life 😮", "He made the impossible possible 🤯", "She said what?! 😲", "He got caught on camera 🎥", "She made the deal of a lifetime 🤝", "He risked everything for love ❤️", "She shocked the judges 😱", "He got the last laugh 😂", "She turned the tables 🔄", "He made the ultimate sacrifice 🥲", "She got the call she was waiting for ☎️", "He pulled off the impossible 😮", "She got the offer of a lifetime 💼", "He made the crowd go wild 🙌", "She got the biggest surprise 😲", "He made the judges cry 😢", "She got the golden ticket 🎫", "He made the world record 🌍", "She got the best deal ever 🏆", "He made the crowd cheer 👏", "She got the shock of her life 😱", "He made the impossible happen 🤯", "She got the best surprise 🎉", "He made the judges laugh 😂", "She got the golden opportunity 🥇", "He made the best deal 💰", "She got the best offer 🏅", "He made the impossible real 😲", "She got the best surprise ever 🎉", "He made the judges smile 😊", "She got the golden chance 🥇", "He made the best offer 💸", "She got the best deal 💰", "He made the impossible true 🤯", "She got the best opportunity 🏆", "He made the judges happy 😃", "She got the golden moment 🥇", "He made the best surprise 🎉", "She got the best chance 🍀", "He made the impossible work 🤔", "She got the best moment 🏆", "He made the judges proud 👏", "She got the golden surprise 🥇", "He made the best opportunity 🏅", "She got the best smile 😊", "He made the impossible win 🏆", "She got the best win 🏆", "He made the judges amazed 😲", "She got the golden win 🥇", "He made the best smile 😊", "She got the best proud 😃", "He made the impossible proud 😎", "She got the best amazed 😲", "He made the judges win 🏆", "She got the golden proud 🥇", "He made the best amazed 😲", "She got the best win ever 🏆"
    ]
    prompt = (
        "Given the following transcript, generate a catchy, viral YouTube Shorts title (max 7 words). "
        "ALWAYS include an emoji in the title. ONLY output the title, nothing else. Do NOT use hashtags. Do NOT explain, do NOT repeat the prompt, do NOT add quotes. If you do not follow these instructions, your output will be discarded. The title should be in the style of these examples: "
        + ", ".join(examples) + ".\n\nTranscript:\n" + transcript_text
    )
    headers = {
        'Authorization': f'Bearer {groq_api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 30,
        "temperature": 0.8
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )
    response.raise_for_status()
    result = response.json()
    # Just return the first line of the response as the title, and filter out any lines that look like explanations or quotes
    content = result['choices'][0]['message']['content']
    lines = [l.strip('"') for l in content.strip().split('\n') if l.strip() and not l.lower().startswith('here') and not l.lower().startswith('title:')]
    title = lines[0] if lines else "Untitled Clip"
    return title

def calculate_engagement_score(clip, transcription):
    """
    Calculate a custom engagement score for a clip based on available data.
    Higher scores indicate more engaging content.
    """
    # Get words in the clip
    clip_words = [w for w in transcription.get_word_info() 
                  if w["start_time"] >= clip.start_time and w["end_time"] <= clip.end_time]
    
    if not clip_words:
        return 0.0
    
    # Calculate various engagement factors
    duration = clip.end_time - clip.start_time
    word_count = len(clip_words)
    word_density = word_count / duration if duration > 0 else 0
    
    # Count numbers, currency, and exclamation marks (engagement indicators)
    engagement_words = 0
    for word_info in clip_words:
        word = word_info["word"]
        if any(char.isdigit() for char in word) or '$' in word or '!' in word:
            engagement_words += 1
    
    # Calculate engagement score (0-1 scale)
    # Factors: word density (45%), engagement words ratio (30%), duration balance (25%)
    word_density_score = min(word_density / 3.0, 1.0)  # Normalize to 0-1
    engagement_ratio = engagement_words / word_count if word_count > 0 else 0
    duration_score = min(duration / 75.0, 1.0)  # Prefer clips around 75 seconds
    
    engagement_score = (word_density_score * 0.45 + 
                       engagement_ratio * 0.30 + 
                       duration_score * 0.25)
    
    return engagement_score

# Find all mp4 files in the input directory
input_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.mp4')]
if not input_files:
    raise FileNotFoundError('No mp4 file found in input directory.')

# Find all transcription files in the input directory
transcription_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('_transcription.pkl')]

# If more than one mp4, ask user to match transcription files (if any)
video_transcription_map = {}
if len(input_files) > 1:
    print("Multiple video files detected:")
    for idx, f in enumerate(input_files, 1):
        print(f"  {idx}) {f}")
    print("\nAvailable transcription files:")
    for idx, f in enumerate(transcription_files, 1):
        print(f"  {idx}) {f}")
    print("\nFor each video, enter the number of the matching transcription file, or 0 to transcribe from scratch.")
    for vid_idx, video_file in enumerate(input_files, 1):
        while True:
            try:
                match = input(f"Match transcription for '{video_file}' (0 for none): ").strip().replace('\r', '')
                match_idx = int(match)
                if match_idx == 0:
                    video_transcription_map[video_file] = None
                    break
                elif 1 <= match_idx <= len(transcription_files):
                    video_transcription_map[video_file] = transcription_files[match_idx-1]
                    break
                else:
                    print("Invalid choice. Try again.")
            except Exception:
                print("Invalid input. Try again.")
else:
    # Only one video, try to auto-match
    video_file = input_files[0]
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    expected_trans = f"{base_name}_transcription.pkl"
    if expected_trans in transcription_files:
        video_transcription_map[video_file] = expected_trans
    else:
        video_transcription_map[video_file] = None

# Prompt user for number of clips for each video BEFORE any processing
video_max_clips = {}
clip_ranges = [(1,2), (3,4), (5,6), (7,8), (9,10), (11,12)]
for video_file in video_transcription_map:
    print(f"\nHow many clips do you want for '{video_file}'?")
    for i, (low, high) in enumerate(clip_ranges, 1):
        print(f"  {i}) {low}-{high}")
    try:
        user_choice = int(input("Your choice: ").strip().replace('\r', ''))
        if not (1 <= user_choice <= len(clip_ranges)):
            raise ValueError
    except Exception:
        print("Invalid input. Defaulting to 2 clips.")
        user_choice = 1
    max_clips = clip_ranges[user_choice-1][1]
    print(f"Will select up to {max_clips} clips (if available and engaging).\n")
    video_max_clips[video_file] = max_clips

# Process each video file
for video_idx, (video_file, transcription_file) in enumerate(video_transcription_map.items(), 1):
    print(f"\n=== Processing Video {video_idx}/{len(video_transcription_map)}: {video_file} ===")
    input_path = os.path.abspath(os.path.join(INPUT_DIR, video_file))
    transcription_path = os.path.join(INPUT_DIR, transcription_file) if transcription_file else get_transcription_file_path(input_path)
    max_clips = video_max_clips[video_file]

    # 1. Transcribe the video (or load existing)
    transcriber = Transcriber(model_size="large-v1")
    transcription = load_existing_transcription(transcription_path) if transcription_file else None
    if transcription is None:
        transcription = transcribe_with_progress(input_path, transcriber)
        save_transcription(transcription, transcription_path)

    # 2. Find clips
    clipfinder = ClipFinder()
    clips = clipfinder.find_clips(transcription=transcription)
    if not clips:
        print('No clips found in the video.')
        continue

    # 3. Filter clips by duration and select the best ones
    valid_clips = [c for c in clips if MIN_CLIP_DURATION <= (c.end_time - c.start_time) <= MAX_CLIP_DURATION]
    selected_clips = []

    if valid_clips:
        # Calculate engagement scores for all valid clips
        clip_scores = [(clip, calculate_engagement_score(clip, transcription)) for clip in valid_clips]
        # Sort by engagement score (highest first)
        clip_scores.sort(key=lambda x: x[1], reverse=True)
        # Select up to max_clips, but only include clips with engagement >= 0.6 (for 3rd and beyond)
        for i, (clip, score) in enumerate(clip_scores):
            if i < 2 or score >= 0.6:
                if len(selected_clips) < max_clips:
                    selected_clips.append(clip)
            else:
                break
        print(f'Selected top {len(selected_clips)} clips:')
        for i, clip in enumerate(selected_clips):
            score = calculate_engagement_score(clip, transcription)
            print(f'  Clip {i+1}: {clip.start_time:.1f}s - {clip.end_time:.1f}s (duration: {clip.end_time - clip.start_time:.1f}s, engagement: {score:.3f})')
        print(f'Clip selection criteria: Top engaging clips within {MIN_CLIP_DURATION}-{MAX_CLIP_DURATION} second range')
    else:
        print(f'No clips found between {MIN_CLIP_DURATION} and {MAX_CLIP_DURATION} seconds.')
        # Find clips that are too short and try to extend them
        short_clips = [c for c in clips if c.end_time - c.start_time < MIN_CLIP_DURATION]
        if short_clips:
            print('Attempting to extend most engaging short clips to minimum duration...')
            short_clip_scores = [(clip, calculate_engagement_score(clip, transcription)) for clip in short_clips]
            short_clip_scores.sort(key=lambda x: x[1], reverse=True)
            # Take top 2 short clips and extend them
            for i, (clip, score) in enumerate(short_clip_scores[:2]):
                if clip.end_time - clip.start_time < MIN_CLIP_DURATION:
                    extension_needed = MIN_CLIP_DURATION - (clip.end_time - clip.start_time)
                    max_extension = min(extension_needed, MAX_CLIP_DURATION - (clip.end_time - clip.start_time))
                    extended_clip = Clip(
                        start_time=clip.start_time,
                        end_time=clip.end_time + max_extension,
                        start_char=clip.start_char,
                        end_char=clip.end_char
                    )
                    selected_clips.append(extended_clip)
                    print(f'Extended clip {i+1}: {extended_clip.start_time:.1f}s - {extended_clip.end_time:.1f}s (duration: {extended_clip.end_time - extended_clip.start_time:.1f}s)')
        else:
            # All clips are too long, trim the most engaging ones
            print('All clips are too long. Trimming most engaging clips to maximum duration...')
            long_clip_scores = [(clip, calculate_engagement_score(clip, transcription)) for clip in clips]
            long_clip_scores.sort(key=lambda x: x[1], reverse=True)
            # Take top 2 long clips and trim them
            for i, (clip, score) in enumerate(long_clip_scores[:2]):
                if clip.end_time - clip.start_time > MAX_CLIP_DURATION:
                    trimmed_clip = Clip(
                        start_time=clip.start_time,
                        end_time=clip.start_time + MAX_CLIP_DURATION,
                        start_char=clip.start_char,
                        end_char=clip.end_char
                    )
                    selected_clips.append(trimmed_clip)
                    print(f'Trimmed clip {i+1}: {trimmed_clip.start_time:.1f}s - {trimmed_clip.end_time:.1f}s (duration: {trimmed_clip.end_time - trimmed_clip.start_time:.1f}s)')

    # Process each selected clip
    for clip_index, clip in enumerate(selected_clips):
        print(f'\n--- Processing Clip {clip_index + 1}/{len(selected_clips)} ---')
        # 4. Trim the video to the selected clip
        media_editor = MediaEditor()
        media_file = AudioVideoFile(input_path)
        trimmed_path = os.path.join(OUTPUT_DIR, f'trimmed_clip_{clip_index + 1}.mp4')
        print('Trimming video to selected clip...')
        trimmed_media_file = media_editor.trim(
            media_file=media_file,
            start_time=clip.start_time,
            end_time=clip.end_time,
            trimmed_media_file_path=trimmed_path
        )
        # 5. Try to resize to 9:16 aspect ratio
        output_path = os.path.join(OUTPUT_DIR, f'yt_short_{clip_index + 1}.mp4')
        try:
            print('Resizing video to 9:16 aspect ratio...')
            crops = resize(
                video_file_path=trimmed_path,
                pyannote_auth_token=HUGGINGFACE_TOKEN,
                aspect_ratio=(9, 16)
            )
            resized_video_file = media_editor.resize_video(
                original_video_file=AudioVideoFile(trimmed_path),
                resized_video_file_path=output_path,
                width=crops.crop_width,
                height=crops.crop_height,
                segments=crops.to_dict()["segments"],
            )
            print(f'YouTube Short (9:16) saved to {output_path}')
        except Exception as e:
            print(f'Resizing failed: {e}')
            print('Saving trimmed clip without resizing...')
            output_path = trimmed_path
        # 6. Add styled subtitles
        final_output = create_animated_subtitles(output_path, transcription, clip, output_path)
        # 7. Generate viral title using Groq API
        clip_text = " ".join([w["word"] for w in transcription.get_word_info() if w["start_time"] >= clip.start_time and w["end_time"] <= clip.end_time])
        groq_api_key = "YOUR API KEY HERE"
        title = get_viral_title(clip_text, groq_api_key)
        print(f"\nViral Title for Clip {clip_index + 1}: {title}")
        # 8. Save the final video with the viral title (keep spaces, punctuation, and emojis)
        import shutil
        import string
        def safe_filename(s):
            # Only remove characters not allowed in filenames, but keep spaces, punctuation, and emojis
            valid_chars = f"-_.() {string.ascii_letters}{string.digits}" + "'!?,:;@#$%^&+=[]{}" + "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙😚🙂🤗🤩🤔🤨😐😑😶🙄😏😣😥😮🤐😯😪😫😴😌😛😜😝🤤😒😓😔😕🙃🤑😲☹️🙁😖😞😟😤😢😭😦😧😨😩🤯😬😰😱🥵🥶😳🤪😵😡😠🤬😷🤒🤕🤢🤮🥴😇🥳🥺🤠🤡🤥🤫🤭🧐🤓😈👿👹👺💀👻👽🤖💩😺😸😹😻😼😽🙀😿😾👍👎👌✌️🤞🤟🤘🤙🖕🖐️✋🖖👋🤚👐👏🙌👐🤲🙏✍️💅🤳💪🦵🦶👂👃🧠🦷🦴👀👁️👅👄💋👓🕶️🥽🥼🦺👔👕👖🧣🧤🧥🧦👗👘🥻🩱🩲🩳👙👚👛👜👝🛍️🎒👞👟🥾🥿👠👡👢👑👒🎩🎓🧢⛑️📿💄💍💎"  # common emoji block
            return ''.join(c for c in s if c in valid_chars)
        viral_filename = safe_filename(title).strip() + ".mp4"
        viral_path = os.path.join(OUTPUT_DIR, viral_filename)
        shutil.copy(final_output, viral_path)
        print(f"Final video saved as: {viral_path}\n")

print(f"\n🎉 Successfully created YouTube Shorts for {len(video_transcription_map)} video(s)!") 