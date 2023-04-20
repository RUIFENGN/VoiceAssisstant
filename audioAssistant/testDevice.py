'''import pyaudio

p = pyaudio.PyAudio()

# 选择测试设备
device_id = 0  # 选择用于测试的设备ID

# 打开测试设备
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=44100, input=True,
                input_device_index=device_id)
# 打开扬声器
output_stream = p.open(format=pyaudio.paInt16, channels=1,
                       rate=44100, output=True,
                       output_device_index=p.get_default_output_device_info()['index'])

# 播放测试音频
while True:
    data = stream.read(1024)
    output_stream.write(data)
'''

import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['maxInputChannels'] > 0:
        print(f"编号{i}: {dev['name']}")
