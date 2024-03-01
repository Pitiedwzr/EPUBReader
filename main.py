import json
import ebooklib
from ebooklib import epub
import requests

# ��ȡ�����ļ�
def read_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config

# ��EPUB�ļ�����ȡ�ı�����
def extract_text_from_epub(epub_file_path):
    book = epub.read_epub(epub_file_path)
    text = ""
    for item in book.get_items():
        # ���item�Ƿ�Ϊ�ı�����
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # ��ȡ�ı�����
            text += item.get_content().decode('utf-8')  # ����Ϊ�ַ���
    return text

# ����API������Ƶ
def generate_audio(text, api_token, api_url, audio_format):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "text/plain",
        "FORMAT": audio_format  # ����ʽ����ֱ������Ϊ�ַ���
    }
    data = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US"><voice name="en-US-GuyNeural">{text}</voice></speak>'
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.content  # �����ֽ����͵���Ƶ����
    else:
        print("Failed to generate audio:", response.status_code)
        return None

# ����Ƶ��ӵ�EPUB�ļ���
def add_audio_to_epub(epub_file_path, audio_data):
    book = epub.read_epub(epub_file_path)
    audio_item = epub.EpubItem(uid="audio", file_name="audio.mp3", content=audio_data, media_type="audio/mp3")
    book.add_item(audio_item)
    book.toc.append(audio_item)
    epub.write_epub("output.epub", book)

# ������
def main():
    config = read_config()
    audio_format = config["format_audio"]
    epub_file_path = config["epub_file_path"]
    api_token = config["api_token"]
    api_url = config["api_url"]
    text = extract_text_from_epub(epub_file_path)
    print(text)  # ��ӡ��ȡ���ı�����
    audio_data = generate_audio(text, api_token, api_url, audio_format)
    if audio_data:
        add_audio_to_epub(epub_file_path, audio_data)

if __name__ == "__main__":
    main()
