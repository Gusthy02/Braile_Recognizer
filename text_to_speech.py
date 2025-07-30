from gtts import gTTS

def convert_text_to_speech(text, lang='pt', filename='output.mp3'):
    """
    Converte um texto para fala e salva como um arquivo MP3.
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        return f"Áudio salvo como {filename}"
    except Exception as e:
        return f"Erro ao converter texto para fala: {e}"

if __name__ == '__main__':
    # Exemplo de uso
    text_to_convert = "Olá, este é um teste do sistema de Text-to-Speech da luva leitora de braile."
    print(convert_text_to_speech(text_to_convert, lang='pt', filename='teste_tts.mp3'))

    text_to_convert_en = "Hello, this is a test of the braille reading glove's Text-to-Speech system."
    print(convert_text_to_speech(text_to_convert_en, lang='en', filename='test_tts_en.mp3'))