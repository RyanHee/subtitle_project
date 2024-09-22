import ffmpeg
import whisper
import os
import subprocess
import argparse


def extract_audio(video_file, audio_file):
    try:
        # Extract the audio from the video file
        ffmpeg.input(video_file).output(audio_file).run(overwrite_output=True)
        print(f"Audio extracted to {audio_file}")
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode()}")


def generate_transcript(audio_file, transcript_file):
    try:
        # Load the Whisper model
        model = whisper.load_model("base")  # You can use "small", "medium", "large" for more accuracy
        result = model.transcribe(audio_file)

        # Write transcript to a .txt file
        with open(transcript_file, 'w', encoding='utf-8') as f:
            for segment in result['segments']:
                f.write(f"{segment['text']}\n")  # Write only the text, no timestamps

        print(f"Transcript saved to {transcript_file}")
    except Exception as e:
        print(f"Error generating transcript: {str(e)}")


# Main function 1
def generate_video_transcript(video_file, transcript_file):
    audio_file = "extracted_audio.wav"

    # Extract audio from the video
    extract_audio(video_file, audio_file)

    # Generate transcript using Whisper
    generate_transcript(audio_file, transcript_file)

    # Clean up: Remove the extracted audio file if you don't need it
    if os.path.exists(audio_file):
        os.remove(audio_file)


# Function to convert seconds to SRT time format
def seconds_to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


# Generate SRT file from Whisper transcription
def generate_srt(transcription, output_srt_file):
    with open(output_srt_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(transcription['segments'], start=1):
            start_time = seconds_to_srt_time(segment['start'])
            end_time = seconds_to_srt_time(segment['end'])
            text = segment['text'].strip()

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")


# main function 2
def add_caption(i_video_file, o_video_file=None, lang=None, srt_file=None, txt_file=None):
    audio_file = "extracted_audio.wav"

    if o_video_file is None:
        o_video_file = i_video_file[0:-4] + '_captions.mp4'

    if srt_file is None:
        srt_file = i_video_file[0:-4] + '.srt'

    # Step 1: Extract audio from the video
    print(f"generating audio file ...")
    extract_audio(i_video_file, audio_file)

    # Load and run Whisper to get transcription with timestamps
    model = whisper.load_model("base")
    if lang is None:
        result = model.transcribe(audio_file)
    else:
        result = model.transcribe(audio_file, language=lang)

    # Create subtitles.srt file
    # srt_file = "captions.srt"
    print("generating srt file {srt_file} ...")
    generate_srt(result, srt_file)
    generate_srt(result, txt_file)
    # Add subtitles to the video using ffmpeg
    print("generating output file {o_video_file} ...")
    subprocess.run(['ffmpeg', '-i', i_video_file, '-vf', f"subtitles={srt_file}", '-c:a', 'copy', o_video_file, '-y'])

    # Clean up: Remove the extracted audio file if you don't need it
    if os.path.exists(audio_file):
        os.remove(audio_file)


def add_caption_from_srtfile(i_video_file, o_video_file=None, srt_file=None):
    if o_video_file is None:
        o_video_file = i_video_file[0:-4] + '_captions.mp4'
    if srt_file is None:
        srt_file = i_video_file[0:-4] + '.srt'

    # Add subtitles to the video using ffmpeg
    print("generating output file {o_video_file} ...")
    subprocess.run(['ffmpeg', '-i', i_video_file, '-vf', f"subtitles={srt_file}", '-c:a', 'copy', o_video_file, '-y'])


def print_usage():
    print("command options:")
    print("")
    print("command 1:")
    print(f"python run.py 1 [video file name]")
    print(f"for example:")
    print(f"python run.py 1 ling_1.mp4")
    print("")
    print("command 2:")
    print(f"python run.py 2 [video file name] --txt_file [translated_subtitle file name]")
    print(f"if [translated_subtitle file name] is the same as [video file name] (ex: video file name is ling_1.mp4, translated_subtitle file name is ling_1.txt): ")
    print(f"python run.py 2 ling_1.mp4")
    print(f"or you can also use --txt_file to indicate the translated_subtitle file you want to ")
    print(f"python run.py 2 ling_1.mp4 --txt_file ling_1.txt")
    print("")
    print("command 3:")
    print(f"python run.py 3 [video file name] --srt_file [translated_subtitle file name]")
    print(f"if [translated_subtitle file name] is the same as [video file name] (ex: video file name is ling_1.mp4, translated_subtitle file name is ling_1.srt): ")
    print(f"python run.py 3 ling_1.mp4")
    print(f"or you can also use --srt_file to indicate the translated_subtitle file you want to ")
    print(f"python run.py 3 ling_1.mp4 --srt_file ling_1.srt")


def main():
    # Create the ArgumentParser object
    parser = argparse.ArgumentParser(description="arguments for translating software")

    # Add a required integer argument
    parser.add_argument('step', type=int, help="run command: 1, 2, or 3")
    parser.add_argument('i_video_file', type=str, help="original file name")

    # Add optional arguments with default values
    parser.add_argument('--txt_file', type=str, default=None, help="subtitle file (.txt) name")
    parser.add_argument('--srt_file', type=str, default=None, help="subtitle file (.srt) name")

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    step = args.step
    i_video_file = args.i_video_file
    if not os.path.exists(i_video_file):
        print(f"找不到原始视频文件{i_video_file}; 指定正确路径")
        quit()

    if step == 1:
        o_video_file = i_video_file[0:-4] + '_src_captions.mp4'
        txt_file = i_video_file[0:-4] + '.txt'
        srt_file = i_video_file[0:-4] + '.srt'
        add_caption(i_video_file, o_video_file=o_video_file, lang='ko', srt_file=srt_file, txt_file=txt_file)
        print(f"\n\n\n\nProcess complete! check whether {o_video_file} and {txt_file} were generated")
    elif step == 2:
        # txt file as caption
        o_video_file = i_video_file[0:-4] + '_dst_captions.mp4'
        if args.txt_file is None:
            txt_file = i_video_file[0:-4] + '.txt'
        else:
            txt_file = args.txt_file
        if not os.path.exists(txt_file):
            print(f"cannot locate subtitle file {txt_file}; please make sure it is in the correct directory")
            quit()

        add_caption_from_srtfile(i_video_file, o_video_file=o_video_file, srt_file=txt_file)
        print(f"\n\n\n\nProcess complete! Check whether {o_video_file} was generated")
    elif step == 3:
        # srt file as caption
        o_video_file = i_video_file[0:-4] + '_dst_captions.mp4'
        if args.srt_file is None:
            srt_file = i_video_file[0:-4] + '.srt'
        else:
            srt_file = args.srt_file
        if not os.path.exists(srt_file):
            print(f"cannot locate subtitle file {srt_file}; please make sure it is in the correct directory")
            quit()

        add_caption_from_srtfile(i_video_file, o_video_file=o_video_file, srt_file=srt_file)
        print(f"\n\n\n\nProcess complete! Check whether {o_video_file} was generated")
    else:
        print(f"Error: Invalid command!")
        print_usage()
        quit()


if __name__ == '__main__':
    main()

# Usage 1
# video_file = "arthistory_1.mp4"  # Replace with your video file
# transcript_file = "arthistory_1_transcript.txt"  # Desired output transcript file
# generate_video_transcript(video_file, transcript_file)

# Usage 2
# video_file = "arthistory_1.mp4"  # Replace with your video file
# o_video_file = "arthistory_1_caption.mp4"  # Desired output transcript file
# video_file = "ling_1.mp4"  # Replace with your video file
# o_video_file = "arthistory_1_caption.mp4"  # Desired output transcript file
# add_caption(video_file,lang='ko')
# add_caption_from_srtfile(video_file)
