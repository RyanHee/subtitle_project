import ffmpeg
import whisper
import os
import subprocess
import argparse
import re

import json
import pandas as pd

def get_mp4_resolution(file_path):
	# Run ffprobe to get video metadata
	cmd = [
		"ffprobe", "-v", "error", "-select_streams", "v:0",
		"-show_entries", "stream=width,height", "-of", "json", file_path
	]
	result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	try:
		result.check_returncode()
	except subprocess.CalledProcessError as e:
		print(f"Error running ffprobe: {e.stderr}")
		return None
	metadata = json.loads(result.stdout)
	
	# Extract width and height
	width = metadata["streams"][0]["width"]
	height = metadata["streams"][0]["height"]
	return width, height

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

	# Step 1: Extract audio from the video
	extract_audio(video_file, audio_file)

	# Step 2: Generate transcript using Whisper
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
def add_caption(i_video_file,o_video_file=None,lang=None,srt_file=None):
	audio_file = "extracted_audio.wav"

	if o_video_file is None:
		o_video_file = i_video_file[0:-4]+'_captions.mp4'
	
	if srt_file is None:
		srt_file = i_video_file[0:-4]+'.srt'
	
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
	#srt_file = "captions.srt"
	print("generating srt file {srt_file} ...")
	generate_srt(result, srt_file)

	# Add subtitles to the video using ffmpeg
	print("generating output file {o_video_file} ...")
	subprocess.run(['ffmpeg', '-i', i_video_file, '-vf', f"subtitles={srt_file}", '-c:a', 'copy', o_video_file, '-y'])

	# Clean up: Remove the extracted audio file if you don't need it
	if os.path.exists(audio_file):
		os.remove(audio_file)

def add_caption_from_srtfile(i_video_file,o_video_file=None,srt_file=None,font_size=None,font_color=None):
	if o_video_file is None:
		o_video_file = i_video_file[0:-4]+'_captions.mp4'	
	if srt_file is None:
		srt_file = i_video_file[0:-4]+'.srt'
	
	# Add subtitles to the video using ffmpeg
	print("generating output file {o_video_file} ...")
	subtitle_param = f"subtitles={srt_file}"
	if font_size is not None or font_color is not None:
		subtitle_param += ":force_style=\'"
		
		i = 0
		if font_size is not None:
			font_size_str = f"FontSize={font_size}"
			subtitle_param += font_size_str
			i += 1
		
		if font_color is not None:
			font_color = font_color[1:] # remove #
			if i>0:
				subtitle_param+=','
			subtitle_param += f"PrimaryColour=&H{font_color}&"
			i+=1
		
		subtitle_param += "\'"
		
		print(f"subtitle_param={subtitle_param}")
		
		subprocess.run(['ffmpeg', '-i', i_video_file, '-vf', subtitle_param, '-c:a', 'copy', o_video_file, '-y'])
	else:
		subprocess.run(['ffmpeg', '-i', i_video_file, '-vf', f"subtitles={srt_file}", '-c:a', 'copy', o_video_file, '-y'])
	#ffmpeg -i input_video.mp4 -vf "subtitles=subtitle.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF&'" -c:a copy output_video.mp4

# RRGGBB TO BBGGRR
def convert_color_format(color):
	# Check if the input is a valid 6-character hex string
	if len(color) == 6 and all(c in '0123456789abcdefABCDEF' for c in color):
		# Rearrange to bbggrr format
		return color[4:6] + color[2:4] + color[0:2]
	else:
		raise ValueError("Invalid color format. Please use 'rrggbb' format, like FF0000")
		quit()

def convert_srt_file_to_json(srt_file):
	# open srt_file, read content and split to lines
	content = None
	with open(srt_file, "r", encoding="utf-8") as file:
		# read file content, and split to lines
		content = file.readlines()
	if content is None or len(content)==0:
		print(f'读取 {srt_file} 失败')
		return None

	data_list = []
	curr_entry = None
	# state:
	# looking_for_index
	# looking_for_timestamp
	# looking_for_text
	state = 'looking_for_index'
	for entry in content:
		# remove \n at the end
		entry = entry.strip()

		if len(entry)==0:
			continue

		if state == 'looking_for_index':
			# find first number
			try:
				index = int(entry)
				state = 'looking_for_timestamp'
				if curr_entry is not None:
					curr_entry['index'] = index
				else:
					curr_entry = {'index':index}
			except ValueError:
				if len(data_list)>0:
					data_list[-1]['text'] += '\n' + entry

		elif state == 'looking_for_timestamp':
			# find first --> 
			if ' --> ' in entry:
				ts = entry.split(" --> ")
				if len(ts)!=2:
					continue
				state = 'looking_for_text'
				for i in range(2):
					# convert xx:xx:xx,xxx to xx:xx:xx.xx (1 second = 1000 ms)
					if ',' in ts[i]:
						tt = ts[i].split(',')
						if len(tt)!=2:
							continue
						try:
							# basically 518ms -> 518/10 = 52
							t1 = round(int(tt[1])/10)
							tt[1] = f'{t1:02d}'
						except ValueError:
							continue
						ts[i] = tt[0] + '.' + tt[1]

				curr_entry['from'] = ts[0]
				curr_entry['to'] = ts[1]
			else:
				continue

		elif state == 'looking_for_text':
			if 'text' not in curr_entry:
				curr_entry['text'] = entry
			else:
				curr_entry['text'] += '\n' + entry
			data_list.append(curr_entry)
			curr_entry = None
			state = 'looking_for_index'

	return data_list

# test
#convert_srt_file_to_json('ling.txt')

def convert_json_to_txt(data_list, txt_file):
	with open(txt_file, "w", encoding="utf-8") as file:
		for entry in data_list:
			msg = ''
			msg += f"{entry['index']}\t"
			msg += f"{entry['from']} --> {entry['to']}\t"
			msg += f"{entry['text']}"
			file.write(f"{msg}\n")


def convert_json_to_ass(data_list, ass_file, video_file,width, height):
	content_0 = None
	content_1 = None
	with open('ass_hdr_0.txt', "r", encoding="utf-8") as file:
		# read file content, and split to lines
		content_0 = file.readlines()
	if content_0 is None or len(content_0)==0:
		print(f'读取 ass_hdr_0.txt 失败')
		return None
	with open('ass_hdr_1.txt', "r", encoding="utf-8") as file:
		# read file content, and split to lines
		content_1 = file.readlines()
	if content_1 is None or len(content_1)==0:
		print(f'读取 ass_hdr_1.txt 失败')
		return None
	
	with open(ass_file, "w", encoding="utf-8") as file:
		# 头写上去
		for line in content_0:
			file.write(line)
		
		msg = f'PlayResX: {width}\n'
		file.write(msg)
		msg = f'PlayResY: {height}\n'
		file.write(msg)
		file.write('\n')

		msg = '[Aegisub Project Garbage]\n'
		file.write(msg)
		msg = f'Audio File: {video_file}\n'
		file.write(msg)
		msg = f'Video File: {video_file}\n'
		file.write(msg)
		msg = 'Video AR Mode: 4\n'
		file.write(msg)
		msg = 'Video AR Value: 1.777778\n'
		file.write(msg)
		msg = 'Video Zoom Percent: 0.500000\n'
		file.write(msg)
		msg = 'Scroll Position: 0\n'
		file.write(msg)
		msg = f'Active Line: {len(data_list)}\n'
		file.write(msg)
		msg = 'Video Position: 0\n'
		file.write(msg)
		file.write('\n')

		# styles
		for line in content_1:
			file.write(line)
		
		# columns
		# Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
		for entry in data_list:
			msg = 'Dialogue: 0,'
			msg += f"{entry['from']},"
			msg += f"{entry['to']},"
			msg += 'Default,,0,0,0,,'
			msg += f"{entry['text']}"
			file.write(f"{msg}\n")

def prt_t_msg():
	print(f"错误: cut步骤必须输入正确的截取开始和结束时间")
	print("t0表示开始时间; t1表示结束时间")
	print("格式是 HH:MM:SS 或者 MM:SS")
	print("1:12:34表示1小时12分钟34秒; 12:34表示12分钟34秒")

def cut_video(i_video_file, t0, t1, cut_file):
	ts = [t0,t1]
	tsf = []
	for i in range(len(ts)):
		t = ts[i].split(':')
		hms = ['0','0','0']
		if len(t)==2:
			hms[1] = t[0]
			hms[2] = t[1]
		elif len(t)==3:
			hms[0] = t[0]
			hms[1] = t[1]
			hms[2] = t[2]
		elif len(t)==1:
			hms[2] = t[0]
		else:
			print_t_msg()
			return -1
		for k in range(3):
			try:
				number = int(hms[k])
			except ValueError:
				prt_t_msg()
				return -1
			hms[k] = number
			
		print(f"ts{i}: {hms}")
		msg  = f"{hms[0]:02d}:{hms[1]:02d}:{hms[2]:02d}"
		msg2 = f"{hms[0]:02d}H{hms[1]:02d}M{hms[2]:02d}S"
		print(f"{msg}, {msg2}")
		ts[i] = msg
		tsf.append(msg2)
		
	if cut_file is None:
		cut_file = f"{tsf[0]}_{tsf[1]}_{i_video_file}"
			
	# ffmpeg -i input_video.mp4 -ss t0 -to t1 -c copy output_video.mp4
	print(f"{i_video_file} {ts[0]} {ts[1]} {cut_file}")
	#quit()
	subprocess.run(['ffmpeg', '-i', i_video_file, '-ss', ts[0], '-to', ts[1], '-c', 'copy', cut_file, '-y'])
		
	print('\n\n')
	print(f"确认文件 {cut_file} 是否生成")
	return 0


def print_usage():
	print("使用方式:")
	print("")
	print("步骤1:")
	print(f"python run 1 原始视频文件名")
	print(f"例如:")
	print(f"python run 1 ling_1.mp4")
	print("")
	print("步骤2:")
	print(f"python run 2 原始视频文件名 --srt_file 字幕翻译文件名")	
	print(f"例如, 假设翻译好的文件和原始视频文件名一样, 视频是ling_1.mp4, 翻译是ling_1.srt: ")
	print(f"python run 2 ling_1.mp4")
	print(f"或者, 也可以用--srt_file指定翻译文件名")
	print(f"python run 2 ling_1.mp4 --srt_file ling_1.srt")
	
	# 20241222
	print('')
	print('截取原始文件，生成需要翻译部分的文件')
	print(f"python run cut 原始视频文件名 --cut_file 新视频文件名 --t0 XX:XX:XX --t1 XX:XX:XX")

	# 20241230
	print('')
	print('生成交付文件')
	print(f"python run convert_output 原始视频文件名 --out_xls_file 输出excel文件名 --out_ass_file 输出ass文件名 --out_txt_file 输出txt文件名")
	
def main():
	# Create the ArgumentParser object
	parser = argparse.ArgumentParser(description="翻译软件的参数")

	# 20241222 change to string
	# Add a required integer argument
	#parser.add_argument('step', type=int, help="运行步骤: 1、2、cut")
	parser.add_argument('step', type=str, help="运行步骤: 1、2、cut")
	parser.add_argument('i_video_file', type=str, help="原始视频文件名")
	
	# Add optional arguments with default values
	parser.add_argument('--srt_file', type=str, default=None, help="字幕文件(srt文件)名")

	parser.add_argument('--font_size', type=int, default=None, help="字体大小12-24")
	parser.add_argument('--font_color', type=str, default=None, help="字体颜色, 例如红色为FF0000")
	
	# 20241222
	parser.add_argument('--cut_file', type=str, default=None, help="截取的视频文件名")	
	parser.add_argument('--t0', type=str, default=None, help="开始截取时间HH:MM:SS")	
	parser.add_argument('--t1', type=str, default=None, help="截取结束时间HH:MM:SS")	
	
	# 20241230
	# --srt_file: 字母文件名
	parser.add_argument('--out_xls_file', type=str, default=None, help="输出excel文件")	
	parser.add_argument('--out_ass_file', type=str, default=None, help="输出ass文件")	
	parser.add_argument('--out_txt_file', type=str, default=None, help="输出txt文件")	

	
	# Parse the arguments
	args = parser.parse_args()

	# Access the arguments
	step = args.step
	i_video_file = args.i_video_file
	if not os.path.exists(i_video_file) and step!='convert_output':
		print(f"找不到原始视频文件{i_video_file}; 指定正确路径")
		quit()
	
	#print(f'step = {step}')
	#quit()
	
	# 20241222 change to string
	#if step==1:
	if step=='1':
		print('\n\n step 1 ...')
		
		o_video_file = i_video_file[0:-4]+'_src_captions.mp4'
		srt_file = i_video_file[0:-4]+'.txt'
		add_caption(i_video_file,o_video_file=o_video_file,lang='ko',srt_file=srt_file)
		print(f"\n\n\n\n处理完成! 确认{o_video_file}和{srt_file}是否生成了")
	# 20241222 change to string
	elif step=='2':
	#elif step==2:
		font_size = args.font_size
		if font_size is not None:
			print(f"font_size={font_size}")
		font_color = args.font_color
		if font_color is not None:
			if font_color[0:1] != '#':
				font_color = '#'+ font_color

			# Regular expression to match hex color codes
			hex_color_pattern = re.compile(r'^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$')
			valid = bool(hex_color_pattern.match(font_color))
			if valid:
				print(f"font_color={font_color}")
			else:
				print(f"font_color is bad {font_color}")
				font_color=None
			
			color1 = convert_color_format(font_color[1:])
			font_color = '#' + color1
			
		#quit()
		
		o_video_file = i_video_file[0:-4]+'_dst_captions.mp4'
		if args.srt_file is None:
			srt_file = i_video_file[0:-4]+'.txt'
		else:
			srt_file = args.srt_file
		if not os.path.exists(srt_file):
			print(f"找不到字幕文件{srt_file}; 指定正确路径")
			quit()
		
		add_caption_from_srtfile(i_video_file,o_video_file=o_video_file,srt_file=srt_file,font_size=font_size,font_color=font_color)
		print(f"\n\n\n\n处理完成! 确认{o_video_file}是否生成了")	
	
	elif step == 'convert_output':
		rt = get_mp4_resolution(i_video_file)
		if rt is None:
			print(f"找不到原始视频文件{i_video_file}; 指定正确路径")
			return
		print(f"原始视频分辨率是{rt[0]}x{rt[1]}")
		width = rt[0]
		height = rt[1]
		#quit()

		srt_file = args.srt_file
		xls_file = args.out_xls_file
		ass_file = args.out_ass_file
		txt_file = args.out_txt_file
		if srt_file is None:
			print(f"--srt_file文件必须指定, 这是翻译好的字幕文件")
			return
		if xls_file is None and ass_file is None and txt_file is None:
			print("--out_xls_file, --out_ass_file, --out_txt_file 必须指定至少其一, 作为输出文件")
			return
		
		print(f'convert {srt_file} to json ...')
		data_list = convert_srt_file_to_json(srt_file)
		if data_list is None:
			return
		#print(data_list)

		if xls_file is not None:
			df = pd.DataFrame(data_list)
			df.to_excel(xls_file, index=False, engine="openpyxl")
			print(f'保存到 {xls_file} 成功')
		
		if txt_file is not None:
			convert_json_to_txt(data_list, txt_file)
			print(f'保存到 {txt_file} 成功')
		
		if ass_file is not None:
			convert_json_to_ass(data_list, ass_file, i_video_file,width, height)
			print(f'保存到 {ass_file} 成功')

	# 20241222
	elif step == 'cut':
		t0 = args.t0
		t1 = args.t1
		cut_file = args.cut_file

		if t0 is None or t1 is None:
			prt_t_msg()
			quit()

		'''		
		ts = [t0,t1]
		tsf = []
		for i in range(len(ts)):
			t = ts[i].split(':')
			hms = ['0','0','0']
			if len(t)==2:
				hms[1] = t[0]
				hms[2] = t[1]
			elif len(t)==3:
				hms[0] = t[0]
				hms[1] = t[1]
				hms[2] = t[2]
			elif len(t)==1:
				hms[2] = t[0]
			else:
				print_t_msg()
				quit()
			for k in range(3):
				try:
					number = int(hms[k])
				except ValueError:
					prt_t_msg()
					quit()
				hms[k] = number
			
			print(f"ts{i}: {hms}")
			msg  = f"{hms[0]:02d}:{hms[1]:02d}:{hms[2]:02d}"
			msg2 = f"{hms[0]:02d}H{hms[1]:02d}M{hms[2]:02d}S"
			print(f"{msg}, {msg2}")
			ts[i] = msg
			tsf.append(msg2)
		
		if cut_file is None:
			cut_file = f"{tsf[0]}_{tsf[1]}_{i_video_file}"
			
		# ffmpeg -i input_video.mp4 -ss t0 -to t1 -c copy output_video.mp4
		print(f"{i_video_file} {ts[0]} {ts[1]} {cut_file}")
		#quit()
		subprocess.run(['ffmpeg', '-i', i_video_file, '-ss', ts[0], '-to', ts[1], '-c', 'copy', cut_file, '-y'])
		
		print('\n\n')
		print(f"确认文件 {cut_file} 是否生成")
		'''

		cut_video(i_video_file, t0, t1, cut_file)

	else:
		print(f"错误: 输入步骤错误")
		print_usage()
		quit()

if __name__ == '__main__':
	main()
	
# Usage 1
#video_file = "arthistory_1.mp4"  # Replace with your video file
#transcript_file = "arthistory_1_transcript.txt"  # Desired output transcript file
#generate_video_transcript(video_file, transcript_file)

# Usage 2
#video_file = "arthistory_1.mp4"  # Replace with your video file
#o_video_file = "arthistory_1_caption.mp4"  # Desired output transcript file
#video_file = "ling_1.mp4"  # Replace with your video file
#o_video_file = "arthistory_1_caption.mp4"  # Desired output transcript file
#add_caption(video_file,lang='ko')
#add_caption_from_srtfile(video_file)