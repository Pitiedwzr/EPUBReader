import ebooklib
from ebooklib import epub
import requests
import tempfile
import os

# 准备EPUB文件路径和API TOKEN
epub_file_path = "The Beginners Bible Timeless Childrens Stories (Zondervan) (Z-Library).epub"
api_token = "060718"
api_url = "https://ms-ra-forwarder-xi-silk.vercel.app/api/ra"  # 更改为您的API网址

# 从EPUB文件中提取文本内容
def extract_text_from_epub(epub_file_path):
    book = epub.read_epub(epub_file_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text += item.get_content().decode('utf-8')  # 解码为字符串
    return text

# 调用API生成音频
def generate_audio(text, api_token, api_url):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "text/plain",
        "FORMAT": "audio-24khz-96kbitrate-mono-mp3"
    }
    data = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US"><voice name="en-US-GuyNeural">{text}</voice></speak>'
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.content  # 返回字节类型的音频数据
    else:
        print("Failed to generate audio:", response.status_code)
        return None

# 将音频添加到EPUB文件中
def add_audio_to_epub(epub_file_path, audio_data):
    book = epub.read_epub(epub_file_path)
    audio_item = epub.EpubItem(uid="audio", file_name="audio.mp3", content=audio_data, media_type="audio/mp3")
    book.add_item(audio_item)
    book.toc.append(audio_item)
    epub.write_epub("output.epub", book)

# 主程序
def main():
    text = extract_text_from_epub(epub_file_path)
    audio_data = generate_audio(text, api_token, api_url)
    if audio_data:
        add_audio_to_epub(epub_file_path, audio_data)

if __name__ == "__main__":
    main()
