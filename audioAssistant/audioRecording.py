import pyaudio
import wave
import tkinter as tk
import os
import tranformerProcess as ap
import time
import threading
from pathlib import Path
# Explicit imports to satisfy Flake8
from tkinter import Canvas, PhotoImage
import textToVoice as tv

# 设置参数
CHUNK = 1024  # 每次读取的音频帧大小
FORMAT = pyaudio.paInt16  # 音频格式（16位）
CHANNELS = 1  # 麦克风通道数
RATE = 44100  # 音频采样率

# 创建 pyaudio 流
p = pyaudio.PyAudio()
stream = None
frames = []

is_recording = False  # 初始化录音状态为 False


# 开始录制音频
def start_recording():
    global stream, frames, is_recording
    is_recording = True
    p = pyaudio.PyAudio()
    stream = None
    try:
        # 创建 pyaudio 流
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=0
                        )
        # 清空音频数据列表
        frames = []
        print("* 录制音频开始 *")

        last_update_time = time.time()  # 记录上一次刷新界面的时间戳
        while is_recording:  # 判断是否录制
            data = stream.read(CHUNK)
            frames.append(data)
            window.update()  # 刷新 GUI 界面，保证程序响应
            current_time = time.time()
            if current_time - last_update_time > 0.1:  # 如果距离上一次刷新界面已经过了10秒
                window.update()  # 刷新 GUI 界面，保证程序响应
                last_update_time = current_time  # 更新上一次刷新界面的时间戳
        # 操作完成后，重新将按钮设置为可点击状态
        button_1.config(state="normal")
    except Exception as e:
        # 异常处理
        print("无法访问麦克风！请检查麦克风是否连接并授权录音权限。")
        print(e)


# 结束录制音频
def stop_recording():
    global stream, frames, is_recording
    is_recording = False
    # 停止并关闭 pyaudio 流
    stream.stop_stream()
    stream.close()
    del stream  # 手动删除流对象释放内存
    p.terminate()
    print("* 录制音频完成 *")
    # 删除原有的 outPut.wav
    if os.path.exists("output.wav"):
        os.remove("output.wav")
    # 将音频数据写入 wav 文件
    # print(frames)
    if len(frames) > 0:
        wf = wave.open("output.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("* 音频文件生成 *")

        # 调用transformer模型
        recoText, GPT = ap.audioProcess("output.wav")
        # 更新文本对象的内容,删除多余的回车
        new_string = recoText.replace("\n", "")
        lowercase_string = new_string.lower()
        new_string1 = GPT.replace("?", "")
        new_string2 = new_string1.replace("？", "")
        canvas.itemconfigure(output_text, text=lowercase_string)
        canvas.itemconfigure(GPT_text, text=new_string2)
        tv.textToVoice(GPT)
    else:
        print("未录制到任何音频数据！请确认麦克风是否正常工作。")
    # 清空音频数据列表和 pyaudio 流
    frames = []
    stream = None
    # 操作完成后，重新将按钮设置为可点击状态
    button_2.config(state="normal")


# 创建 GUI 应用程序
'''root = tk.Tk()
root.title("录制音频")'''


def start_click():
    # 将按钮设置为不可点击状态
    button_1.config(state="disabled")
    canvas.itemconfig(image_9, anchor="nw")
    canvas.coords(image_9, 390.0, 349.0, )
    canvas.itemconfig(image_10, anchor="nw")
    canvas.coords(image_10, -1000, -1000, )
    canvas.itemconfigure(andsoon, text="……………")
    # 启动线程执行长时间的操作
    t = threading.Thread(target=start_recording)
    t.start()


def stop_click():
    # 将按钮设置为不可点击状态
    button_2.config(state="disabled")
    canvas.itemconfig(image_10, anchor="nw")
    canvas.coords(image_10, 390.0, 349.0, )
    canvas.itemconfig(image_9, anchor="nw")
    canvas.coords(image_9, -1000, -1000, )
    canvas.itemconfigure(andsoon, text="")
    # 启动线程执行长时间的操作
    t = threading.Thread(target=stop_recording)
    t.start()


# 运行 GUI 应用程序
# root.mainloop()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = tk.Tk()

window.geometry("1440x680")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=680,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    720.0,
    340.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = tk.Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start_click,
    relief="flat"
)
button_1.pack()
button_1.place(
    x=37.0,
    y=329.0,
    width=320.0,
    height=141.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = tk.Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=stop_click,
    relief="flat"
)
button_2.pack()
button_2.place(
    x=37.0,
    y=499.0,
    width=320.0,
    height=141.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1065.0,
    363.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    667.0,
    234.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    921.0,
    101.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    1318.0,
    101.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    1328.0,
    553.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    1177.0,
    570.0,
    image=image_image_7
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    -1000,
    -1000,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    -1000,
    -1000,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    281.0,
    175.0,
    image=image_image_11
)

canvas.create_text(
    51.0,
    68.0,
    anchor="nw",
    text="语音识别小工具",
    fill="#000000",
    font=("Inter Bold", 31 * -1)
)

canvas.create_text(
    51.0,
    129.0,
    anchor="nw",
    text="依次点击\n“开始录音”\n“停止录音”\n即可识别文本并智能回复",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    907.0,
    595.0,
    anchor="nw",
    text="created by:\n聂瑞丰/刘芸萱/张智博/韦子轩",
    fill="#000000",
    font=("Inter Bold", 24 * -1)
)

andsoon = canvas.create_text(
    385.0,
    543.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter", 24 * -1)
)

output_text = canvas.create_text(
    627.0,
    74.0,
    width=600,
    anchor="nw",
    text="…………",
    fill="#000000",
    font=("Inter", 30 * -1)
)

GPT_text = canvas.create_text(
    779.0,
    179.0,
    width=600,
    anchor="nw",
    text="\n\n…………",
    fill="#000000",
    font=("Inter", 20 * -1)
)

window.resizable(False, False)
window.mainloop()
