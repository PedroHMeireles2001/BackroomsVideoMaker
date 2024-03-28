import os

import pysrt
from moviepy.editor import VideoClip, AudioFileClip
from PIL import Image, ImageFilter, ImageDraw
from moviepy.video.VideoClip import ImageClip


def apply_vignette_effect_to_image(image_path, darkness=0.8):
    if os.path.exists(image_path):
        # Abre a imagem
        img = Image.open(image_path)

        # Converte a imagem para o modo RGB
        img = img.convert('RGB')

        # Cria uma máscara de vinhetagem
        mask = Image.new("L", img.size, 255)
        draw = ImageDraw.Draw(mask)
        width, height = img.size
        gradient = int(min(width, height) * darkness)
        for x in range(width):
            for y in range(height):
                alpha = min(255, 255 * max(0, gradient - ((x - width / 2) ** 2 + (y - height / 2) ** 2) ** 0.5) / gradient)
                draw.point((x, y), int(255 - alpha))

        # Aplica a máscara à imagem
        img.paste((0, 0, 0), mask=mask)

        # Salva a imagem com o efeito de vinhetagem (sobrescrevendo a original)
        img.save(image_path)
        return True
    else:
        print("O arquivo de imagem não foi encontrado:", image_path)
        return False


def apply_blur(image_path):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.filter(ImageFilter.BoxBlur(radius=5))
        img.save(image_path)
        return True
    else:
        return False

def create_video_with_audio(image_path, audio_path,subtitle_path, output_path):
    # Carrega a imagem
    image_clip = VideoClip(lambda t: ImageClip(image_path).get_frame(t), duration=AudioFileClip(audio_path).duration)

    # Carrega o áudio
    audio_clip = AudioFileClip(audio_path)

    # Carrega o arquivo de legenda .srt
    subs = pysrt.open(subtitle_path)



    # Cria o vídeo com a imagem e o áudio
    video_clip = image_clip.set_audio(audio_clip)

    # Adiciona cada legenda ao vídeo
    for sub in subs:
        # Converte o tempo de início e fim das legendas para segundos
        start_time = sub.start.to_time().hour * 3600 + sub.start.to_time().minute * 60 + sub.start.to_time().second + sub.start.to_time().microsecond / 1e6
        end_time = sub.end.to_time().hour * 3600 + sub.end.to_time().minute * 60 + sub.end.to_time().second + sub.end.to_time().microsecond / 1e6

        # Adiciona a legenda ao vídeo
        video_clip = video_clip.subclip(start_time, end_time).set_caption(sub.text)

    # Salva o vídeo
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

