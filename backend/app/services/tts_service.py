"""
TTS Service - Text to Speech
-----------------------------
Responsável por converter texto em áudio (fala) para o usuário.
Usa a biblioteca gTTS (Google Text-to-Speech) para gerar arquivos MP3.
Este módulo é isolado para facilitar manutenção e testes.
"""

from gtts import gTTS
import uuid
import os
import logging

# Configuração do logger para este módulo
logger = logging.getLogger(__name__)

# Pasta temporária para salvar áudios gerados
TMP_AUDIO_DIR = "tmp"
os.makedirs(TMP_AUDIO_DIR, exist_ok=True)

def generate_audio(text: str, lang: str = "pt") -> str:
    """
    Recebe um texto e gera um arquivo de áudio (MP3) com a fala correspondente.

    Parâmetros:
    ----------
    text : str
        Texto que será convertido em áudio.
    lang : str, opcional
        Código do idioma (default é 'pt' para português).

    Retorna:
    -------
    str
        Caminho do arquivo de áudio gerado.
    """
    try:
        # Gera um nome único para o arquivo de áudio
        filename = f"speech_{uuid.uuid4()}.mp3"
        filepath = os.path.join(TMP_AUDIO_DIR, filename)

        # Cria o objeto gTTS
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)  # Salva o arquivo

        logger.info(f"Áudio gerado com sucesso: {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"Erro ao gerar áudio TTS: {e}")
        return ""
