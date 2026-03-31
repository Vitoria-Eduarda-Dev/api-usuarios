from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, users

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Usuários",
    description="Gerenciamento de usuários com JWT"
)

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Usuários FastAPI"}