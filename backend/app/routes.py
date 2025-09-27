"""
Routes - Definição dos endpoints da API
---------------------------------------
Este arquivo define as rotas do FastAPI, utilizando os serviços do bot
para conduzir a entrevista e serviços auxiliares (STT, TTS, Summary).
Inclui:
- Logging
- Validação de arquivos
- Tratamento de erros
- Endpoint de saúde
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.bot_service import InterviewBot
from app.utils.logger import logger

# Inicializa o bot (perguntas padrão)
bot = InterviewBot()

# Criação do roteador do FastAPI
router = APIRouter()

# Diretório temporário para salvar arquivos de áudio
TMP_DIR = Path("tmp")
TMP_DIR.mkdir(parents=True, exist_ok=True)

# Define tamanho máximo de arquivo de áudio (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# ------------------------
# Endpoints
# ------------------------

@router.get("/health", tags=["Health"], summary="Verifica se a API está rodando")
async def health_check():
    """
    Endpoint de saúde da API.
    Retorna status HTTP 200 OK com mensagem.
    """
    logger.info("Health check solicitado")
    return {"status": "ok", "message": "API is running"}


@router.get("/next_question", tags=["Interview"], summary="Retorna a próxima pergunta do bot")
def get_next_question():
    """
    Retorna a próxima pergunta em texto e o estado da entrevista.
    """
    question = bot.get_next_question()
    logger.info(f"Próxima pergunta: {question}")
    return {
        "question": question,
        "question_index": bot.current_index,
        "finished": bot.is_finished()
    }


@router.post("/answer", tags=["Interview"], summary="Envia a resposta do usuário")
async def answer_question(audio: UploadFile = File(...)):
    """
    Recebe arquivo de áudio do usuário e retorna:
    - transcrição (STT)
    - resumo (GPT)
    - caminho do áudio da próxima pergunta (TTS)
    """
    logger.info(f"Recebido arquivo de áudio: {audio.filename}")

    # Valida tipo de arquivo
    if audio.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3"]:
        logger.warning(f"Tipo de arquivo inválido: {audio.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de arquivo não suportado"
        )

    # Valida tamanho do arquivo
    if audio.spool_max_size > MAX_FILE_SIZE:
        logger.warning(f"Arquivo muito grande: {audio.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo muito grande (máx. 5MB)"
        )

    try:
        # Processa a resposta via bot
        result = bot.process_response(audio.file)
        logger.info("Áudio processado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao processar áudio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar áudio: {str(e)}"
        )

    return {
        "transcription": result.get("transcription"),
        "summary": result.get("summary"),
        "next_question_audio": result.get("next_question_audio")
    }


@router.get("/play_audio/{audio_filename}", tags=["Interview"], summary="Baixa ou reproduz um áudio gerado")
def play_audio(audio_filename: str):
    """
    Endpoint para baixar ou reproduzir arquivo de áudio gerado.
    """
    audio_path = TMP_DIR / audio_filename

    if not audio_path.exists():
        logger.warning(f"Arquivo não encontrado: {audio_filename}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado"
        )

    logger.info(f"Reproduzindo arquivo de áudio: {audio_filename}")
    return FileResponse(
        path=audio_path,
        filename=audio_filename,
        media_type="audio/mpeg"
    )
