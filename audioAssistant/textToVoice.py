import pyttsx3

# 创建TTS引擎
engine = pyttsx3.init()
# 设置语速 (默认值为200.0)
engine.setProperty('rate', 180)

# 设置音调 (默认值为100.0)
engine.setProperty('pitch', 150)

# 添加呼吸声效果
engine.setProperty('volume', 0.5)

def textToVoice(text):
    # 将文本转换为语音并播放
    engine.say(text)
    engine.runAndWait()
