# Subtitle Software
A software that helps automatically generate subtitles in videos, allows for easy editing towards those subtitles when needed, and provides additional features such as video cutting and converting subtitles into different formats.

## Setup

1. Copy `ffmpeg.exe`, `ffplay.exe`, `ffprobe.exe` into `C:\windows\system32`.
2. Install Python (version 3.7 or above).
3. Install `ffmpeg-python`, `openai-whisper`, and `pandas` by running the following commands:
   ```bash
   pip install ffmpeg-python
   ```
   ```bash
   pip install openai-whisper
   ```
   ```bash
   pip install pandas
   ```
   **You can input these commands by double-clicking `start.bat` and typing them in there, or you can use your terminal and `cd` to the same directory where this is located.**

## Run

1. Double-click `start.bat` to get it running.
2. Copy the video you want into the current directory (e.g., `ling_1.mp4`).
3. Run command 1 to add auto-generated subtitles to the video and output a transcript of the subtitles:<br>
   **Example:**
   ```bash
   python run.py 1 ling_1.mp4
   ```
   This command will generate 3 files:
   * `ling_1_src_captions.mp4` (video file with captions)
   * `ling_1.srt` (srt file of transcript)
   * `ling_1.txt` (txt file of transcript)

   **Both the txt and srt files are timestamped for each subtitle, making it convenient to edit them when needed.**

4. After making necessary changes to the subtitle files, run command 2 to apply the edited subtitles to the video:<br>
   ```bash
   python run.py 2 ling_1.mp4
   ```
   You can also specify the subtitle file explicitly:
   ```bash
   python run.py 2 ling_1.mp4 --srt_file my_subtitles.srt
   ```

5. **New Feature: Cutting Video Clips**<br>
   You can now extract specific parts of the video using the `cut` command:
   ```bash
   python run.py cut ling_1.mp4 --t0 00:01:00 --t1 00:02:30 --cut_file cut_clip.mp4
   ```
   This extracts a section from 1:00 to 2:30 and saves it as `cut_clip.mp4`.

6. **New Feature: Generating Delivery Files (Excel, ASS, and TXT Formats)**<br>
   You can convert subtitle files into structured formats for better handling and archiving:
   ```bash
   python run.py convert_output ling_1.mp4 --srt_file ling_1.srt --out_xls_file subtitles.xlsx --out_ass_file subtitles.ass --out_txt_file subtitles_cleaned.txt
   ```
   This command converts the subtitles into an Excel file (`subtitles.xlsx`), an ASS subtitle file (`subtitles.ass`), and a cleaned TXT file (`subtitles_cleaned.txt`).

## Applications of the Software

This software is useful when you want to generate subtitles for videos that lack them. Key features include:
- **Automatic Subtitle Generation**: Generates subtitles in multiple languages without additional setup.
- **Easy Editing**: Provides structured transcript files (SRT and TXT) for modification.
- **Subtitle Embedding**: Allows adding translated subtitles to videos.
- **Video Cutting**: Extracts specific parts of a video.
- **Format Conversion**: Converts subtitles into Excel, ASS, or cleaned TXT formats.

### Example Use Cases
- **Translating Videos**: Convert Korean video subtitles to English by editing the transcript files.
- **Content Creation**: Easily add captions to YouTube or educational videos.
- **Video Editing**: Cut sections of a video and add subtitles efficiently.

With these features, the software is a powerful tool for subtitle management, translation, and video editing.
