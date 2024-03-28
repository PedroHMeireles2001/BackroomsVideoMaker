from TextExtractor import html_para_markdown_url,download_first_image
from GPTResumer import scripting,make_audio, sanitize
from Editor import apply_vignette_effect_to_image, apply_blur, create_video_with_audio
import os
import shutil

PREFIX = "[VIDEO MAKER] "

def print_message(msg):
    print(PREFIX+msg)

def save_txt(texto, nome_arquivo):
    try:
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(texto)
    except Exception as e:
        print(f"Error on file: {e}")


def create_work_dir():
    try:
        shutil.rmtree("work")
    except FileNotFoundError:
        pass
    except OSError as e:
        print(e)
    os.mkdir("work")

def make_image(image_path):
    print_message("Downloading image")

    print_message("Editing image")
    download_first_image(url, image_path)
    apply_vignette_effect_to_image(image_path)
    apply_blur(image_path)



def main(url):
    create_work_dir()
    level_path = "work/" + url.split("/")[-1].replace("-", "_")
    image_path = level_path + ".png"
    make_image(image_path)


    print_message("Extracting text from url")
    markdown_text = html_para_markdown_url(url)

    if not markdown_text:
        return

    save_txt(markdown_text, level_path + "_markdown.txt")

    print_message("Cleaning text")
    markdown_sanitized = sanitize(markdown_text)
    save_txt(markdown_sanitized, level_path + "_markdownSanitized.txt")
    print_message("Scripting")
    script = scripting(markdown_sanitized)
    save_txt(script, level_path + ".txt")
    print_message("Recording audio")
    make_audio(script, level_path)
    print_message("Recording video")
    create_video_with_audio(image_path,level_path+".mp3",level_path+".mp4")
if __name__ == "__main__":
    url = "http://backrooms-wiki.wikidot.com/level-35"
    main(url)
