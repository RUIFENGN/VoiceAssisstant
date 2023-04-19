import openai
openai.api_key = "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"
import textToVoice as tv

def responseGPT(prompt):
    # 利用OpenAI的GPT-3 API对语音进行回复
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"Please response the following sentence in a humorous way:\n{prompt}",
      temperature=0.5,
      max_tokens=1024,
      n=1,
      stop=None,
    )

    # 解析API响应，获取改写后的文章和评分
    result = response.choices[0].text
    # score = response.choices[0].score
    tv.textToVoice(result)

    return result
