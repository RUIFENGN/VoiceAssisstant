import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers import Wav2Vec2Processor
from transformers import set_seed
import responseGPT as rg
import librosa

import huggingface_hub
token = "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"
huggingface_hub.login(token=token)

# 加载模型和标记器
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")


processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")

import pyaudio

def audioProcess(wavFile):

    # 加载音频文件并进行预处理
    audio_file = wavFile
    audio_input, sr = torchaudio.load(audio_file)
    if sr != 16000:  # 如果采样率不是16000，进行转换
        transform = torchaudio.transforms.Resample(sr, 16000)
        audio_input = transform(audio_input)
    input_values = processor(audio_input,sampling_rate=16000, return_tensors="pt", padding=True).input_values
    input_values = input_values.squeeze(0)  # 将第一维的大小从1去掉


    # 使用模型进行推理并输出结果
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    print(transcription)
    GPTstring = rg.responseGPT(transcription)
    print(GPTstring)
    return transcription,GPTstring
