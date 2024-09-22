# Subtitle Software
A software that helps automatically generates subtitles in videos, allows for easy editing towards those subtitles when needed

## Setup

1. Copy `ffmpeg.exe`, `ffplay.exe`, `ffprobe.exe` into `C:\windows\system32`.
2. Install Python (version 3.7 or above).
3. Install `ffmpeg-python`, `openai-whisper` by running the following commands:<br>
<br>
   ```bash
   pip install ffmpeg-python
    ```
   ```bash
    pip install openai-whisper
    ```
    **You can input these commands by double clicking start.bat and typing it in there, or you can use your terminal and cd to the same directory where this is located**

## Run

1. Double click start.bat to get it running
2. Copy the video you want into the current directory (e.g. ling_1.mp4)
3. Run command 1, which adds subtitles into the video, as well as outputting a transcript of the subtitles<br>   
   **An example is shown below:**
    ```bash
   python run.py 1 ling_1.mp4
   ```
   The command will generate 3 files:
   * ling_1_src_captions.mp4 (video file with captions)
   * ling_1.srt (srt file of transcript)
   * ling_1.txt (txt file of transcript)<br>

    **It is important to note that the txt and srt files are time stamped for each subtitle, making it convenient to edit them when needed<br>**

    **txt and srt files would look something like this:**
![img.png](img.png)

4. After making necessary changes to the subtitle files, you can run commands 2 or 3 to implement these changes into the actual video <br>  
   Command 2:
    ```bash 
    python run.py 2 ling_1.mp4
    ```
    You can also specify the txt file in case you've decided to create a new one by using --txt_file:
    ```bash
    python run.py 2 ling_1.mp4 --txt_file [txt_file_name].txt
    ``` 
    <br>

   Command 3:
   ```bash 
    python run.py 3 ling_1.mp4
    ```
    You can also specify the srt file in case you've decided to create a new one by using --srt_file:
    ```bash
    python run.py 3 ling_1.mp4 --srt_file [srt_file_name].srt
    ```
   
    Command 2 and 3 serves the same purpose, but command 2 uses txt files as subtitle transcripts while command 3 uses srt files as subtitle transcripts
<br>  
Overall, 2 is better for people less familiar with editing, while 3 is better for people who have a lot of experience with editing and are familiar with srt files


## Applications of the software

&nbsp;&nbsp;&nbsp;&nbsp;This software can be quite useful when you want subtitles in your videos when they're not provided. One great thing about this software is that it supports multiple languages, it does not require additional setup or installations of language packs, making it very convenient to use.<br>  
&nbsp;&nbsp;&nbsp;&nbsp;Also, this software is useful for translations, say for example you want a Korean video to have English subtitles, then you can just edit the srt or txt transcript files that has Korean in it, and translate that to English instead.