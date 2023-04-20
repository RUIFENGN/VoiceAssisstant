import pyaudio
import wave
import tkinter as tk
import os
import audioProcess2 as ap
import time
import threading
from pathlib import Path
# Explicit imports to satisfy Flake8
from tkinter import Canvas, PhotoImage

# 设置参数
CHUNK = 1024  # 每次读取的音频帧大小
FORMAT = pyaudio.paInt16  # 音频格式（16位）
CHANNELS = 1  # 麦克风通道数
RATE = 44100  # 音频采样率

# 创建 pyaudio 流
p = pyaudio.PyAudio()
stream = None
frames = []

is_recording = False   # 初始化录音状态为 False
# 开始录制音频
def start_recording():
    global stream, frames,is_recording
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
        while is_recording: # 判断是否录制
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
    global stream, frames,is_recording
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
    #print(frames)
    if len(frames) > 0:
        wf = wave.open("output.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("* 音频文件生成 *")
        # 调用transformer模型

        recoText = ap.audioProcess("output.wav")
        # 更新文本对象的内容
        canvas.itemconfigure(output_text, text=recoText)
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
    print("我进了新线程了")
    # 启动线程执行长时间的操作
    t = threading.Thread(target=start_recording)
    t.start()

def stop_click():
    # 将按钮设置为不可点击状态
    button_2.config(state="disabled")
    # 启动线程执行长时间的操作
    t = threading.Thread(target=stop_recording)
    t.start()

# 运行 GUI 应用程序
# root.mainloop()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\python_code\VoiceAssisstant\frame0")


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
    width=320,
    height=141,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start_click,
    relief="flat"
)
button_1.pack()
button_1.place(
    x=611,
    y=46.0,
    width=320.0,
    height=141.0
)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = tk.Button(
    width=320,
    height=141,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=stop_click,
    relief="flat"
)
button_2.pack()
button_2.place(
    x=1043.0,
    y=46.0,
    width=320.0,
    height=141.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    990.0,
    424.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    297.0,
    205.0,
    image=image_image_3
)

canvas.create_text(
    82.0,
    70.0,
    anchor="nw",
    text="语音识别小工具",
    fill="#000000",
    font=("Inter Bold", 31 * -1)
)

canvas.create_text(
    82.0,
    149.0,
    anchor="nw",
    text="依次点击\n“开始录音”\n“停止录音”\n即可识别文本",
    fill="#000000",
    font=("Inter", 36 * -1)
)

output_text = canvas.create_text(
    656.0,
    264.0,
    anchor="nw",
    text="要输出的文本",
    fill="#000000",
    font=("Inter", 36 * -1)
)

window.resizable(False, False)
window.mainloop()
