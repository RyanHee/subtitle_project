import tkinter as tk
from tkinter import ttk, messagebox, font
import re
import os,sys
import run

######## GUI configuration parameters

# Font and color
title_font = ("Helvetica", 16, "bold")  # Font: (Font name, Size, Style)

w_dlt = 20 # spacing between entry fields
y_dlt = 30 # spacing between rows
y_sec_dlt = 60 # spacing between sections
x_0 = 20
y_0 = 20

######## Build GUI
win_size = [1024,720]
win_size_str = f'{win_size[0]}x{win_size[1]}'
root = tk.Tk()
root.geometry(win_size_str)
root.title('Translation Tool 0.3.0')

default_font = font.nametofont("TkDefaultFont")

######################### Section: Video Cutting

# params: input video file t0, t1 output video file

def on_cutvideo_bt_click(args):
    i_video_file = args[0][3].get()
    t0 = args[2][3].get()
    t1 = args[3][3].get()
    o_video_file = args[1][3].get()

    if i_video_file == None or i_video_file == '':
        msg = 'Please enter the input video file name'
        messagebox.showinfo('Notice', msg)
        return

    if t0 == None or t0=='':
        msg = 'Please enter the start time, e.g., 00:00:00'
        messagebox.showinfo('Notice', msg)
        return

    if t1 == None or t1=='':
        msg = 'Please enter the end time, e.g., 00:00:00'   
        messagebox.showinfo('Notice', msg)
        return
    
    if o_video_file == None or o_video_file=='':
        msg = 'Please enter the output file name'
        messagebox.showinfo('Notice', msg)
        return

    rt = run.cut_video(i_video_file, t0, t1, o_video_file)

    if rt == 0:
        msg = f'Successfully cut, check output file {o_video_file}'
        messagebox.showinfo('Notice', msg)
    else:
        msg = 'Cutting failed, check the start and end times\n'
        msg += "Time format is HH:MM:SS or MM:SS\n"
        msg += "1:12:34 means 1 hour 12 minutes 34 seconds; 12:34 means 12 minutes 34 seconds"
        messagebox.showinfo('Notice', msg)

    return
    i_video_file = args[0][3].get()
    t0 = args[2][3].get()
    t1 = args[3][3].get()
    o_video_file = args[1][3].get()

    if i_video_file == None or i_video_file == '':
        msg = '请输入原始视频文件名'
        messagebox.showinfo('提示', msg)
        return

    if t0 == None or t0=='':
        msg = '请输入开始时间, 例如 00:00:00'
        messagebox.showinfo('提示', msg)
        return

    if t1 == None or t1=='':
        msg = '请输入结束时间, 例如 00:00:00'   
        messagebox.showinfo('提示', msg)
        return
    
    if o_video_file == None or o_video_file=='':
        msg = '请输入输出文件名'
        messagebox.showinfo('提示', msg)
        return

    rt = run.cut_video(i_video_file, t0, t1, o_video_file)

    if rt == 0:
        msg = f'截取成功, 请检查输出文件 {o_video_file}'
        messagebox.showinfo('提示', msg)
    else:
        msg = '截取失败, 请检查截取开始和节数时间\n'
        msg += "时间格式是 HH:MM:SS 或者 MM:SS\n"
        msg += "1:12:34表示1小时12分钟34秒; 12:34表示12分钟34秒"
        messagebox.showinfo('提示', msg)

    return

cutvideo_boxes_0 = [ ['Input File Name:  ', 800, 'i_video_file', None] ]
cutvideo_boxes_1 = [ ['Output File Name:  ', 800, 'o_video_file', None] ]
cutvideo_boxes_2 = [ ['Start Time HH:MM:SS  ', 80, 't0', None], ['End Time HH:MM:SS  ', 80, 't1', None] ]

cutvideo_boxess = [cutvideo_boxes_0, cutvideo_boxes_1, cutvideo_boxes_2]
cutvideo_args = cutvideo_boxes_0 + cutvideo_boxes_1 + cutvideo_boxes_2
xstart = x_0
ystart = y_0

label = tk.Label(text="Cut Video", font=title_font)
label.place(x=xstart, y=ystart)  # Specify position
ystart += y_dlt

for cutvideo_boxes in cutvideo_boxess:
    xstart = x_0
    for i in range(len(cutvideo_boxes)):
        txtlen = default_font.measure(cutvideo_boxes[i][0])
        label = ttk.Label(text=cutvideo_boxes[i][0], width=txtlen)
        label.place(x=xstart, y=ystart)
        xstart += txtlen
        cutvideo_boxes[i][3] = ttk.Entry()
        cutvideo_boxes[i][3].place(x=xstart, y=ystart, width=cutvideo_boxes[i][1])
        xstart += cutvideo_boxes[i][1] + w_dlt

    ystart += y_dlt

# Button (execute)
#ystart += y_dlt
xstart = x_0
bt_txt = " Cut "
bt_w = default_font.measure(bt_txt) + 20
cutvideo_bt = ttk.Button(text=bt_txt, command=lambda: on_cutvideo_bt_click(cutvideo_args))
cutvideo_bt.place(x=xstart, y=ystart, width=bt_w)

######################### Section: Step 1, Add Original Captions to Video and Generate Subtitle File (txt)

def on_step1_bt_click(args):
    i_video_file = args[0][3].get()

    if i_video_file == None or i_video_file == '':
        msg = 'Please enter the input video file name'
        messagebox.showinfo('Notice', msg)
        return

    o_video_file = i_video_file[0:-4]+'_src_captions.mp4'
    srt_file = i_video_file[0:-4]+'.txt'
    run.add_caption(i_video_file,o_video_file=o_video_file,lang='ko',srt_file=srt_file)

    msg = f'Processing completed! Check {o_video_file} and {srt_file}'
    messagebox.showinfo('Notice', msg)

    return

ystart += y_sec_dlt
label = tk.Label(text="Step 1: Add Original Captions to Video and Generate Subtitle File (txt)", font=title_font)
label.place(x=xstart, y=ystart)
ystart += y_dlt

step1_boxes_0 = [ ['Input File Name:  ', 800, 'i_video_file', None] ]
step1_boxess = [step1_boxes_0]
step1_args = step1_boxes_0

for step1_boxes in step1_boxess:
    xstart = x_0
    for i in range(len(step1_boxes)):
        txtlen = default_font.measure(step1_boxes[i][0])
        label = ttk.Label(text=step1_boxes[i][0], width=txtlen)
        label.place(x=xstart, y=ystart)  # Specify position
        xstart += txtlen
        step1_boxes[i][3] = ttk.Entry()
        step1_boxes[i][3].place(x=xstart, y=ystart, width=step1_boxes[i][1])  # Specify position
        xstart += step1_boxes[i][1] + w_dlt

    ystart += y_dlt

# Button (execute)
#ystart += y_dlt
xstart = x_0
bt_txt = " Run "
#bt_w = (len(bt_txt)*char_w)
bt_w = default_font.measure(bt_txt) + 20
step1_bt = ttk.Button(text=bt_txt, command=lambda: on_step1_bt_click(step1_args))
step1_bt.place(x=xstart, y=ystart, width=bt_w)



######################### Section: Step 2, Add Translated Subtitles to Original Video File

def on_step2_bt_click(args):
    i_video_file = args[0][3].get()
    font_size = args[1][3].get()
    font_color = args[2][3].get()

    if font_size is None or font_size == '':
        font_size = None
    else:
        try:
            font_size = int(font_size)
        except:
            msg = 'Please enter a valid font size, e.g., 12'
            messagebox.showinfo('Notice', msg)
            return

    if font_color is None or font_color == '':
        font_color = None
    else:
        if font_color[0:1] != '#':
            font_color = '#' + font_color

        # Regular expression to match hex color codes
        hex_color_pattern = re.compile(r'^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$')
        valid = bool(hex_color_pattern.match(font_color))
        if valid:
            print(f"font_color={font_color}")
        else:
            msg = 'Please enter a valid color, e.g., FF0000 for red'
            messagebox.showinfo('Notice', msg)
            return

        color1 = run.convert_color_format(font_color[1:])
        font_color = '#' + color1

    o_video_file = i_video_file[0:-4] + '_dst_captions.mp4'
    srt_file = i_video_file[0:-4] + '.txt'
    if not os.path.exists(srt_file):
        msg = f"Subtitle file {srt_file} not found; Please specify the correct path"
        messagebox.showinfo('Notice', msg)
        return

    run.add_caption_from_srtfile(
        i_video_file, o_video_file=o_video_file,
        srt_file=srt_file, font_size=font_size, font_color=font_color
    )
    msg = f"Processing completed! Check if {o_video_file} was generated"
    messagebox.showinfo('Notice', msg)

    return


ystart += y_sec_dlt
label = tk.Label(text="Step 2: Add Translated Subtitles to Original Video File", font=title_font)
label.place(x=xstart, y=ystart)  # Specify position
ystart += y_dlt

step2_boxes_0 = [['Input File Name:  ', 800, 'i_video_file', None]]
step2_boxes_1 = [['Font Size (12-24):  ', 60, 'font_size', None], ['Font Color (Red is FF0000):  ', 100, 'font_color', None]]
step2_boxess = [step2_boxes_0, step2_boxes_1]
step2_args = step2_boxes_0 + step2_boxes_1

for step2_boxes in step2_boxess:
    xstart = x_0
    for i in range(len(step2_boxes)):
        txtlen = default_font.measure(step2_boxes[i][0])
        label = ttk.Label(text=step2_boxes[i][0], width=txtlen)
        label.place(x=xstart, y=ystart)  # Specify position
        xstart += txtlen
        step2_boxes[i][3] = ttk.Entry()
        step2_boxes[i][3].place(x=xstart, y=ystart, width=step2_boxes[i][1])  # Specify position
        xstart += step2_boxes[i][1] + w_dlt

    ystart += y_dlt

# Button (execute)
#ystart += y_dlt
xstart = x_0
bt_txt = " Run "
#bt_w = (len(bt_txt)*char_w)
bt_w = default_font.measure(bt_txt) + 20
step2_bt = ttk.Button(text=bt_txt, command=lambda: on_step2_bt_click(step2_args))
step2_bt.place(x=xstart, y=ystart, width=bt_w)


######################### Section: Generate Delivery Files

def on_genout_bt_click(args):
    i_video_file = args[0][3].get()
    i_srt_file = args[1][3].get()
    out_txt_file = args[2][3].get()
    out_ass_file = args[3][3].get()

    if i_video_file == None or i_video_file == '':
        msg = 'Please enter the input video file name'
        messagebox.showinfo('Notice', msg)
    
    if i_srt_file == None or i_srt_file == '':
        msg = 'Please enter the translated txt file name'
        messagebox.showinfo('Notice', msg)

    if out_txt_file == None or out_txt_file == '':
        out_txt_file = None

    if out_ass_file == None or out_ass_file == '':
        out_ass_file = None
    
    if out_txt_file == None and out_ass_file is None:
        msg = 'Please enter at least one output file name (txt or ass)'
        messagebox.showinfo('Notice', msg)


    rt = run.get_mp4_resolution(i_video_file)
    if rt is None:
        msg = f"Input video file {i_video_file} not found; Please specify the correct path"
        messagebox.showinfo('Notice', msg)
        return

    print(f"Input video resolution is {rt[0]}x{rt[1]}")
    width = rt[0]
    height = rt[1]

    data_list = run.convert_srt_file_to_json(i_srt_file)
    if data_list is None:
        msg = f"Translated txt file {i_srt_file} seems to have issues, please check its content"
        return

    if out_txt_file is not None:
        if out_txt_file == i_srt_file:
            msg = f"Output delivery txt file name cannot be the same as the translated txt file name!"
            messagebox.showinfo('Notice', msg)
            return

        run.convert_json_to_txt(data_list, out_txt_file)
	
    if out_ass_file is not None:
        run.convert_json_to_ass(data_list, out_ass_file, i_video_file,width, height)

    if out_txt_file is not None and out_ass_file is not None:
        msg = f'Processing completed! Check {out_txt_file} and {out_ass_file}'
    elif out_txt_file is not None:
        msg = f'Processing completed! Check {out_txt_file}'
    else: #out_ass_file is not None:
        msg = f'Processing completed! Check {out_ass_file}'
    messagebox.showinfo('Notice', msg)

    return
    i_video_file = args[0][3].get()
    i_srt_file = args[1][3].get()
    out_txt_file = args[2][3].get()
    out_ass_file = args[3][3].get()

    if i_video_file == None or i_video_file == '':
        msg = '请输入原始视频文件名'
        messagebox.showinfo('提示', msg)
    
    if i_srt_file == None or i_srt_file == '':
        msg = '请输入翻译好的txt文件名'
        messagebox.showinfo('提示', msg)

    if out_txt_file == None or out_txt_file == '':
        out_txt_file = None

    if out_ass_file == None or out_ass_file == '':
        out_ass_file = None
    
    if out_txt_file == None and out_ass_file is None:
        msg = '请输入输出交付的txt或ass文件名, 至少1个'
        messagebox.showinfo('提示', msg)


    rt = run.get_mp4_resolution(i_video_file)
    if rt is None:
        msg = f"找不到原始视频文件{i_video_file}; 指定正确路径"
        messagebox.showinfo('提示', msg)
        return

    print(f"原始视频分辨率是{rt[0]}x{rt[1]}")
    width = rt[0]
    height = rt[1]

    data_list = run.convert_srt_file_to_json(i_srt_file)
    if data_list is None:
        msg = f"翻译好的txt文件{i_srt_file}似乎有问题, 请确认内容"
        return

    if out_txt_file is not None:
        if out_txt_file == i_srt_file:
            msg = f"输出交付txt文件名不能和翻译好的txt文件名一样!"
            messagebox.showinfo('提示', msg)
            return

        run.convert_json_to_txt(data_list, out_txt_file)
	
    if out_ass_file is not None:
        run.convert_json_to_ass(data_list, out_ass_file, i_video_file,width, height)

    if out_txt_file is not None and out_ass_file is not None:
        msg = f'处理完成! 确认{out_txt_file}和{out_ass_file}是否生成了'
    elif out_txt_file is not None:
        msg = f'处理完成! 确认{out_txt_file}是否生成了'
    else: #out_ass_file is not None:
        msg = f'处理完成! 确认{out_ass_file}是否生成了'
    messagebox.showinfo('提示', msg)

    return

ystart += y_sec_dlt
label = tk.Label(text="Generate Delivery txt and ass Subtitle Files", font=title_font)
label.place(x=xstart, y=ystart)  # Specify position
ystart += y_dlt

genout_boxes_0 = [ ['Video File Name:  ', 800, 'i_video_file', None] ]
genout_boxes_1 = [ ['Translated txt File Name (Number, Time --> Time):  ', 600, 'i_srt_file', None] ]
genout_boxes_2 = [ ['Output Delivery txt File Name:  ', 800, 'out_txt_file', None] ]
genout_boxes_3 = [ ['Output Delivery ass File Name:  ', 800, 'out_ass_file', None] ]

genout_boxess = [genout_boxes_0, genout_boxes_1, genout_boxes_2, genout_boxes_3]
genout_args = genout_boxes_0 + genout_boxes_1 + genout_boxes_2 + genout_boxes_3

for genout_boxes in genout_boxess:
    xstart = x_0
    for i in range(len(genout_boxes)):
        txtlen = default_font.measure(genout_boxes[i][0])
        label = ttk.Label(text=genout_boxes[i][0], width=txtlen)
        label.place(x=xstart, y=ystart)  # Specify position
        xstart += txtlen
        genout_boxes[i][3] = ttk.Entry()
        genout_boxes[i][3].place(x=xstart, y=ystart, width=genout_boxes[i][1])  # Specify position
        xstart += genout_boxes[i][1] + w_dlt

    ystart += y_dlt

# Button (execute)
xstart = x_0
bt_txt = " Generate Delivery Files "
bt_w = default_font.measure(bt_txt) + 20
genout_bt = ttk.Button(text=bt_txt, command=lambda: on_genout_bt_click(genout_args))
genout_bt.place(x=xstart, y=ystart, width=bt_w)


######## Run the GUI event loop
root.mainloop()