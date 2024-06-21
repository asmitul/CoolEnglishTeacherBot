from typing import Dict
import requests
from pathlib import Path

from configs.server import SERVER_HOST as host, SERVER_PORT as port, API_KEY

VERSION = "v1"
BASE_URL = f"http://{host}:{port}/{VERSION}"

def translate_text(text: str, source_language: str, target_language: str, audio_language: str, voice: str, speed_factor: float) -> Dict:
    url = f"{BASE_URL}/translate"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    payload = {
        "text": text,
        "source_language": source_language,
        "target_language": target_language,
        "audio_language": audio_language,
        "voice": voice,
        "speed_factor": speed_factor
    }
    response = requests.post(url, params=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def download_audio_file(file_id: str, download_path: Path):
    url = f"{BASE_URL}/download/{file_id}"
    headers = {
        "accept": "application/json",
        "access_token": API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(download_path, "wb") as file:
        file.write(response.content)

if __name__ == "__main__":
    # Example usage:
    text_to_translate = "你好"
    source_lang = "chinese"
    target_lang = "english"
    audio_lang = "target"
    voice_type = "alloy"
    speed = 0.75

    # Translate text and get file_id
    translation_response = translate_text(text_to_translate, source_lang, target_lang, audio_lang, voice_type, speed)
    file_id = translation_response.get("file_id")

    if file_id:
        # Download the audio file using file_id
        download_path = Path("downloaded_speech.mp3")
        download_audio_file(file_id, download_path)
    else:
        print("Translation failed, no file_id returned")
