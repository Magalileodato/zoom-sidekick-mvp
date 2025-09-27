"""
Bot Service - Orquestração da Entrevista
----------------------------------------
Responsável por conduzir o fluxo da entrevista de forma automatizada:
1. Faz a pergunta ao usuário.
2. Recebe o áudio de resposta.
3. Transcreve o áudio (STT).
4. Resume a resposta (GPT).
5. Gera a próxima pergunta em áudio (TTS).
6. Retorna o áudio e o resumo.
"""

import logging
from app.services import stt_service, tts_service, summary_service

# Logger específico do bot
logger = logging.getLogger(__name__)

class InterviewBot:
    """
    Classe que representa o bot de entrevista.
    Mantém estado simples da conversa e orquestra serviços.
    """
    def __init__(self, questions=None):
        # Lista de perguntas da entrevista
        if questions is None:
            self.questions = [
                "Olá! Pode se apresentar brevemente?",
                "Quais são seus pontos fortes?",
                "Quais são seus pontos de melhoria?",
                "Fale sobre um projeto recente que você desenvolveu.",
                "Por que você quer trabalhar conosco?"
            ]
        else:
            self.questions = questions

        self.current_question_index = 0
        logger.info("InterviewBot inicializado com perguntas padrão")

    def get_next_question(self) -> str:
        """
        Retorna a próxima pergunta da lista.
        """
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            logger.info(f"Próxima pergunta: {question}")
            return question
        else:
            logger.info("Todas as perguntas foram feitas")
            return "Obrigado pela participação!"

    def process_response(self, audio_file) -> dict:
        """
        Recebe o áudio do usuário e retorna:
        - Transcrição
        - Resumo da resposta
        - Áudio da próxima pergunta (TTS)
        """
        logger.info("Processando resposta do usuário")

        # 1. Transcrever o áudio
        transcription = stt_service.transcribe(audio_file)
        logger.info(f"Transcrição obtida: {transcription[:50]}...")

        # 2. Resumir a resposta
        summary = summary_service.summarize(transcription)
        logger.info(f"Resumo gerado: {summary[:50]}...")

        # 3. Preparar próxima pergunta
        next_question = self.get_next_question()
        audio_path = tts_service.generate_audio(next_question)

        return {
            "transcription": transcription,
            "summary": summary,
            "next_question_audio": audio_path
        }
