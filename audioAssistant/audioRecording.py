import pyaudio
import wave
import tkinter as tk
import os
import audioProcess2 as ap

# 设置参数
CHUNK = 1024  # 每次读取的音频帧大小
FORMAT = pyaudio.paInt16  # 音频格式（16位）
CHANNELS = 1  # 麦克风通道数
RATE = 44100  # 音频采样率

# 创建 pyaudio 流
p = pyaudio.PyAudio()
stream = None
frames = []

# 开始录制音频
def start_recording():
    global stream, frames
    #try:
    # 创建 pyaudio 流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=2
                    )

    # 清空音频数据列表
    frames = []
    print("* 录制音频开始 *")
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        root.update()  # 刷新 GUI 界面，保证程序响应
    #frames.append(stream.read(1024))

    '''except Exception as e:
        # 异常处理
        print("无法访问麦克风！请检查麦克风是否连接并授权录音权限。")
        print(e)'''

# 结束录制音频
def stop_recording():
    global stream, frames
    # 停止并关闭 pyaudio 流
    stream.stop_stream()
    stream.close()
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
        ap.audioProcess("output.wav")
    else:
        print("未录制到任何音频数据！请确认麦克风是否正常工作。")

# 创建 GUI 应用程序
root = tk.Tk()
root.title("录制音频")

# 创建 Start 按钮
start_button = tk.Button(root, text="Start", command=start_recording)
start_button.pack()

# 创建 Stop 按钮
stop_button = tk.Button(root, text="Stop", command=stop_recording)
stop_button.pack()



# 运行 GUI 应用程序
root.mainloop()