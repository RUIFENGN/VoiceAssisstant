import torch
import torchaudio
import soundfile as sf
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# 加载 wav2vec2 模型
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# 读取音频文件
audio_file, _ = torchaudio.load("test.wav")


# 预处理音频文件
def preprocess_audio(audio_file):
    # 转换采样率
    audio_resampled = torchaudio.transforms.Resample(48000, 16000)(audio_file)
    # 缩放波形数据
    audio_scaled = torchaudio.transforms.Vol(1 / 32768)(audio_resampled)
    # 提取特征
    features = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_fft=512, win_length=400, hop_length=160,
                                                    n_mels=64)(audio_scaled)
    # 应用对数缩放
    features_log = torch.log(features + 1e-9)
    # 转换为模型输入格式
    input_values = tokenizer(features_log, return_tensors='pt').input_values

    return input_values


input_values = preprocess_audio(audio_file)

# 将音频输入模型并生成文本
with torch.no_grad():
    logits = model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]

print(transcription)
