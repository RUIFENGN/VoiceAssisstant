import openai
openai.api_key = "YOUR API KEY" #将此修改为自己的openai的api key

def responseGPT(prompt):
    # 利用OpenAI的GPT-3 API对语音进行回复
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"请简短的用中文回答下列问题:\n{prompt}",
      temperature=0.5,
      max_tokens=1024,
      n=1,
      stop=None,
    )

    # 解析API响应，获取回复后的文本
    result = response.choices[0].text

    return result
