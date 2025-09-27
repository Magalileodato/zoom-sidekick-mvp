"""
main.py - Ponto de entrada da aplicação FastAPI
------------------------------------------------
Responsável por:
- Iniciar a API
- Registrar rotas
- Configurar middlewares (CORS)
- Capturar erros globais
- Endpoints de health check
"""

# ------------------------
# Imports
# ------------------------
# Padrões
import traceback

# FastAPI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Locais
from app import routes
from app.utils.logger import logger

# ------------------------
# Criação da aplicação FastAPI
# ------------------------
app = FastAPI(
    title="Zoom Sidekick MVP",
    description="MVP de assistente de entrevistas em reuniões online",
    version="1.0.0",
)

# ------------------------
# Middleware CORS
# ------------------------
# Em produção, substituir '*' pelos domínios confiáveis
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Middleware de tratamento global de exceções
# ------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Captura qualquer exceção não tratada nos endpoints
    e retorna resposta padrão com status 500.
    """
    # Log detalhado do erro e traceback para debug
    logger.error(f"Erro inesperado: {exc}\n{traceback.format_exc()}")
    
    # Resposta para o usuário/cliente
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno. Contate o administrador."},
    )

# ------------------------
# Registro de rotas
# ------------------------
app.include_router(routes.router)

# ------------------------
# Endpoint raiz (async para consistência)
# ------------------------
@app.get("/", tags=["Health"], summary="Verifica se a API está rodando")
async def read_root():
    """
    Endpoint raiz de verificação do status da API.
    Pode ser usado para monitoramento básico.
    """
    logger.info("Health check raiz solicitado")
    return {"status": "Zoom Sidekick API is running 🚀"}

# ------------------------
# Endpoint health detalhado
# ------------------------
@app.get("/health", tags=["Health"], summary="Health check detalhado")
async def health_check():
    """
    Retorna informações de status da aplicação
    para monitoramento de serviços e containers.
    """
    logger.info("Health check detalhado solicitado")
    return {"status": "ok", "message": "API is running"}
