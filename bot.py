import os
import json
import time
import schedule
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip, CompositeVideoClip
import requests

STORIES_FILE = 'stories.json'

def load_stories():
    if not os.path.exists(STORIES_FILE):
        return []
    with open(STORIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_stories(stories):
    with open(STORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(stories, f, ensure_ascii=False, indent=4)

def fetch_story_from_groq():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Groq API anahtarı bulunamadı, varsayılan masal kullanılıyor.")
        return {
            "title": "Küçük Yıldızın Maceraları",
            "script": "Bir zamanlar gökyüzünde yaşayan küçük bir yıldız varmış. Bu yıldız parlamayı çok severmiş. Bir gün yeryüzündeki çocukların sesini duymuş ve onlara gülümsemiş."
        }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": "Çocuklar için kısa, eğitici ve akıcı bir masal yaz. Sadece JSON formatında şu anahtarları ver: title ve script"}],
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
        content = json.loads(data['choices'][0]['message']['content'])
        return content
    except Exception as e:
        print(f"Groq API hatası: {e}")
        return None

def create_video(story):
    title = story['title']
    script = story['script']
    
    print(f"Ses dosyası oluşturuluyor: {title}")
    tts = gTTS(text=script, lang='tr', slow=False)
    audio_path = "story.mp3"
    tts.save(audio_path)
    
    audio = AudioFileClip(audio_path)
    duration
