import requests

# 设置API端点
url = 'h'
api_token = ''

def create_ssml(text, voice_name):
    # 这里是创建SSML字符串的函数，您可能需要根据实际情况进行调整
    return f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
      <voice name="{voice_name}">
        {text}
      </voice>
    </speak>
    """

voice_name = 'en-GB-RyanNeural'
'''
ChineseMale: zh-CN-XiaoyiNeural
ChineseFemale: zh-CN-XiaoxiaoNeural
English(US)Male: en-US-GuyNeural
English(US)Female: en-US-MichelleNeural
English(UK)Male: en-GB-RyanNeural
English(UK)Female: en-GB-SoniaNeural
'''
voice_format = 'audio-24khz-96kbitrate-mono-mp3'
text = u''

# 创建SSML数据
ssml_data = create_ssml(text, voice_name)

# 设置请求头部
headers = {
    'Content-Type': 'text/plain',
    'Authorization': f'Bearer {api_token}',
    'Format': voice_format  # 根据官方示例添加的格式头部
}




# 发送POST请求
response = requests.post(url, headers=headers, data=ssml_data.encode('utf-8'))

# 检查响应状态
if response.status_code == 200:
    # 将响应内容写入文件
    with open('output.mp3', 'wb') as audio_file:
        audio_file.write(response.content)
    print("音频合成成功，文件已保存为 output.mp3")
elif response.status_code == 401:
    print("音频合成失败，无效的密钥")
else:
    print(f"音频合成失败，错误代码：{response.status_code}")
