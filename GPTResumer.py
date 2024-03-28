import openai
from gtts import gTTS
from openai import OpenAI
from pathlib import Path

client = OpenAI()


def sanitize(markdown):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "turn this markdown into user-friendly, markdown-free text:"+markdown}
        ]
    )
    return completion.choices[0].message.content

def scripting(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"Separate the following text into the specified parts:\nText: ```{text}````\n Separate the text into the following parts:\n1. Name\n2. Difficulty Class\n3. Detailed Description\n4. Entrances and Exits\n5. Entities\n6. Bases "},
            {"role": "user", "content": text}
        ]
    )
    script = completion.choices[0].message.content
    script = script.replace("- ", "")
    script = script.replace("1. ", "")
    script = script.replace("2. ", "")
    script = script.replace("3. ", "")
    script = script.replace("4. ", "")
    script = script.replace("5. ", "")
    script = script.replace("6. ", "")
    return script



def translate(text, language):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate for {language}."},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content

def make_audio(text,file,language="en-US"):
    tts = gTTS(text=text, lang=language)
    tts.save(f"{file}.mp3")
