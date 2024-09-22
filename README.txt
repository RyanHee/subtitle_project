手动安装：
1. 拷贝ffmpeg.exe到c:\windows\system32
2. 安装Python
3. pip install ffmpeg-python openai-whisper



运行：
1. 双击start.bat

2. 拷贝要处理的视频到start.bat所在目录
   例如：拷贝ling_1.mp4 到这个目录

3. 运行第一步，给原始视频文件打上原始文字字幕，并且生成字幕文件(txt)
   例如: python run.py 1 ling_1.mp4
   生成两个文件:
   * ling_1_src_captions.mp4是带韩文字幕的视频
   * ling_1.txt是字幕文本文件，把里面韩文替换为中文即可

4. 运行第二步，给原始视频文件添加翻译的字幕
   例如: python run.py 2 ling_1.mp4
   这里只给了原始视频文件名，默认翻译好的文本文件是一样的(ling_1.txt)

   也可以指定翻译好的文件名, 例如: 
   python run.py 2 ling_1.mp4 --srt_file fanyi.txt
   这里翻译好的文件名是fanyi.txt

   最后生成的视频文件是ling_1_dst_captions.mp4 


   