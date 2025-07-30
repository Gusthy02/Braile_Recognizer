from flask import Flask, request, render_template_string, send_from_directory
import os
import sys

# Adiciona o diretório atual ao PATH para importar braille_recognizer e text_to_speech
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from braille_recognizer import recognize_braille
from text_to_speech import convert_text_to_speech

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Simulador de Luva Braile</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background-color: #f4f4f4; 
            color: #333; 
        }
        .container { 
            max-width: 600px; 
            margin: auto; 
            background: #fff; 
            padding: 30px; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        }
        h1 { 
            color: #0056b3; 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .form-group { margin-bottom: 20px; }
        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: bold; 
        }
        input[type="text"] { 
            width: calc(100% - 22px); 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 4px; 
        }
        button { 
            background-color: #007bff; 
            color: white; 
            padding: 10px 15px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 16px; 
        }
        button:hover { background-color: #0056b3; }
        .result { 
            margin-top: 30px; 
            padding: 15px; 
            background-color: #e9ecef; 
            border-radius: 4px; 
            border: 1px solid #ced4da; 
        }
        .result h2 { margin-top: 0; color: #0056b3; }
        .tactile-feedback-display { 
            margin-top: 20px; 
            border: 1px solid #ccc; 
            padding: 10px; 
            min-height: 100px; 
            background-color: #f8f9fa; 
            border-radius: 4px; 
        }
        .dot { 
            width: 20px; 
            height: 20px; 
            background-color: #bbb; 
            border-radius: 50%; 
            display: inline-block; 
            margin: 5px; 
        }
        .dot.active { background-color: #007bff; }
        audio { width: 100%; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Simulador de Luva Braile</h1>
        <form method="POST" action="/">
            <div class="form-group">
                <label for="image_path">Caminho da Imagem Braile (ex: braille_sample.png):</label>
                <input type="text" id="image_path" name="image_path" value="{{ image_path_val }}">
            </div>
            <button type="submit">Reconhecer Braile</button>
        </form>

        {% if recognized_text %}
        <div class="result">
            <h2>Resultado do Reconhecimento:</h2>
            <p>{{ recognized_text }}</p>
            {% if audio_file %}
            <h2>Áudio:</h2>
            <audio controls autoplay>
                <source src="{{ audio_file }}" type="audio/mpeg">
                Seu navegador não suporta o elemento de áudio.
            </audio>
            {% endif %}
            <h2>Simulação de Feedback Tátil:</h2>
            <div class="tactile-feedback-display">
                {% if recognized_text == "Olá Mundo! (Braile Simulado)" %}
                    <div class="dot active"></div><div class="dot active"></div><div class="dot"></div>
                    <div class="dot active"></div><div class="dot"></div><div class="dot active"></div>
                    <div class="dot"></div><div class="dot active"></div><div class="dot"></div>
                    <div class="dot active"></div><div class="dot active"></div><div class="dot active"></div>
                    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                    <p>Simulando padrão de vibração para "Olá Mundo!"</p>
                {% elif recognized_text == "Nenhum braile detectado (Braile Simulado)" %}
                    <p>Nenhum padrão de vibração. Luva em estado de repouso.</p>
                {% else %}
                    <p>Padrão de vibração genérico para texto reconhecido.</p>
                {% endif %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    recognized_text = None
    audio_file = None
    image_path_val = "braille_sample.png"

    if request.method == "POST":
        image_path_val = request.form["image_path"]
        if not os.path.exists(image_path_val):
            recognized_text = (
                f"Erro: O arquivo \'{image_path_val}\' não foi encontrado. "
                "Certifique-se de que a imagem está no diretório correto."
            )
        else:
            recognized_text = recognize_braille(image_path_val)
            if "Erro" not in recognized_text:
                audio_filename = "recognized_braille.mp3"
                convert_text_to_speech(recognized_text, lang="pt", filename=audio_filename)
                audio_file = f"/{audio_filename}"

    return render_template_string(
        HTML_TEMPLATE, 
        recognized_text=recognized_text, 
        image_path_val=image_path_val, 
        audio_file=audio_file
    )

@app.route("/recognized_braille.mp3")
def serve_audio():
    # CORREÇÃO: Usar send_from_directory para servir o arquivo do diretório atual
    return send_from_directory(os.getcwd(), "recognized_braille.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)