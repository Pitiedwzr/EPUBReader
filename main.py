import requests
import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

url = ''
api_token = ''

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

headers = {
    'Content-Type': 'text/plain',
    'Authorization': f'Bearer {api_token}',
    'Format': voice_format
}


def create_ssml(text, voice_name):
    return f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
      <voice name="{voice_name}">
        {text}
      </voice>
    </speak>
    """

ssml_data = create_ssml(text, voice_name)

# 调用TTS API
def text_to_speech(text, voice_name, file_name):
    ssml_data = create_ssml(text, voice_name)
    headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'Bearer {api_token}',
        'Format': voice_format
    }
    response = requests.post(url, headers=headers, data=ssml_data.encode('utf-8'))
    if response.status_code == 200:
        with open(file_name, 'wb') as audio_file:
            audio_file.write(response.content)
        return True
    return False

def main(epub_path):
    book = epub.read_epub(epub_path)
    audio_files = []
    global_index = 0

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.content, 'html.parser')
        for p in soup.find_all('p'):
            # 将段落文本转换为语音
            file_name = f'paragraph_{global_index}.mp3'
            if text_to_speech(p.text, voice_name, file_name):
                print(f"段落 {global_index} 转换成功，保存为 {file_name}")
                audio_tag = soup.new_tag('audio', controls=True)
                audio_tag['src'] = f'../audio/{file_name}'
                p.append(audio_tag)
                audio_files.append(file_name)
                global_index += 1
            else:
                print(f"段落 {global_index} 转换失败")
        item.content = str(soup)

    # 将音频文件添加到EPUB中
    for audio_file in audio_files:
        audio_item = epub.EpubItem(
            uid=audio_file,
            file_name=f'audio/{audio_file}',
            media_type='audio/mpeg',
            content=open(audio_file, 'rb').read()
        )
        book.add_item(audio_item)

    # 重新打包EPUB文件
    epub.write_epub('BOOK_audio.epub', book)

main('BOOK.epub')