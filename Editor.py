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

def create_video_with_audio(image_path, audio_path, output_path):
    # Carrega a imagem
    image_clip = VideoClip(lambda t: ImageClip(image_path).get_frame(t), duration=AudioFileClip(audio_path).duration)

    # Carrega o áudio
    audio_clip = AudioFileClip(audio_path)


    # Cria o vídeo com a imagem e o áudio
    video_clip = image_clip.set_audio(audio_clip)


    # Salva o vídeo
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

