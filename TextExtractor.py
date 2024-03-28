import html2text
import requests
import urllib.request
from bs4 import BeautifulSoup
import urllib.request


def download_first_image(url,image_name ,div_class='scp-image-block'):
    # Faz a solicitação GET para a página HTML
    response = requests.get(url)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Analisa o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra o primeiro div com a classe especificada
        div_tag = soup.find('div', class_=div_class)

        # Se encontrou o div com a classe especificada
        if div_tag:
            # Encontra a primeira tag de imagem dentro do div
            img_tag = div_tag.find('img')

            # Se houver uma imagem dentro do div
            if img_tag:
                # Pega a URL da imagem
                img_url = img_tag['src']

                # Baixa a imagem
                urllib.request.urlretrieve(img_url, f'{image_name}')
            else:
                print("Nenhuma imagem encontrada dentro do div com a classe '{}'.".format(div_class))
        else:
            print("Nenhum div com a classe '{}' encontrado nesta página.".format(div_class))
    else:
        print("Falha ao recuperar a página.")


def remover_classes(soup, class_names):
    for class_name in class_names:
        elements = soup.find_all(class_=class_name)
        for element in elements:
            element.extract()


def html_para_markdown_url(url):
    # Faz a solicitação HTTP para obter o HTML da URL
    response = requests.get(url)

    if response.status_code == 200:
        html_string = response.text

        # Usa BeautifulSoup para encontrar a div com o ID main-content
        soup = BeautifulSoup(html_string, 'html.parser')
        main_content_div = soup.find('div', {'id': 'page-content'})

        if main_content_div:
            # Remove os elementos com as classes especificadas
            remover_classes(soup, ['footer-wikiwalk-nav', 'licensebox','header-diamond','creditRate','bottom-box','footnotes-footer'])

            # Converte o HTML para Markdown
            converter = html2text.HTML2Text()
            converter.body_width = 0  # Para não quebrar as linhas
            markdown_text = converter.handle(str(main_content_div))
            return markdown_text
        else:
            print("Não foi possível encontrar a div com o ID main-content")
            return None
    else:
        print(f"Não foi possível obter o HTML da URL: {url}")
        return None