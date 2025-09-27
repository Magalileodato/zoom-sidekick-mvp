"""
STT Service - Speech to Text
-----------------------------
Responsável por converter arquivos de áudio em texto.
Usa o modelo Whisper da OpenAI para realizar a transcrição.
Este módulo é isolado para facilitar testes e manutenção.
"""

import whisper
import logging

# Configuração do logger para este módulo
logger = logging.getLogger(__name__)

# Carrega o modelo Whisper uma vez na inicialização
# Modelos maiores são mais precisos, mas consomem mais memória
# 'base' é suficiente para MVP
try:
    model = whisper.load_model("base")
    logger.info("Modelo Whisper carregado com sucesso")
except Exception as e:
    logger.error(f"Falha ao carregar modelo Whisper: {e}")
    model = None

def transcribe(audio_file) -> str:
    """
    Recebe um arquivo de áudio (file-like object) e retorna o texto transcrito.

    Parâmetros:
    ----------
    audio_file : file-like
        Arquivo de áudio enviado pelo usuário.

    Retorna:
    -------
    str
        Texto transcrito do áudio.
    """
    if model is None:
        logger.warning("Modelo não carregado, retornando string vazia")
        return ""

    try:
        # Transcreve o áudio usando Whisper
        result = model.transcribe(audio_file)
        text = result.get("text", "").strip()
        logger.info(f"Transcrição concluída: {text[:50]}...")  # Log das primeiras palavras
        return text
    except Exception as e:
        logger.error(f"Erro ao transcrever áudio: {e}")
        return ""
