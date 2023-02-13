from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware
)
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Importa classes para persistencia dos dados no SQLite
import database.crud as crud
import model.models as models
from database.schemas import UserModel, User
from database.database import SessionLocal, engine

from service import Service
# from service.service import Service

# Importar MovieUtils e Genre para usar na api do TMDB
from tmdb.models import Genre
from tmdb.api_utils import (
    RequestApi, MovieUtils
)
app = FastAPI()

# habilita CORS (permite que o Svelte acesse o fastapi)
origins = [
    "http://localhost",
    "http://localhost:5173",
]

# Faz parte da configuaracao do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# todo: testar para ver se o banco nao esta sendo
# apagado toda vez que inicia o fastapi
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =============================
# USER (sqlite)
# =============================


@app.post("/user/create")
async def create_user(user: UserModel, db: Session = Depends(get_db)):
    print(user)
    # verifica se ja nao um usuario com este email
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    # faz o insert no banco
    new_user = crud.create_user(db=db, user=user)
    # print(new_user)
    return new_user


@app.get("/user/list")
async def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/user/delete/{id}")
async def delete_user(id=int, db: Session = Depends(get_db)):
    return crud.delete_user(db, id)


@app.post("/user/update")
def update_user(user: User, db: Session = Depends(get_db)):
    return crud.update_user(db, user)


@app.get("/user/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, id)

# =============================
# MOVIE (tmdb)
# =============================


@app.get("/genres")
async def get_genres():
    return Service.get_genres()


@app.get("/movies")
async def get_movies():
    # chamar a classe MovieUtils para consultar TMDB
    movies = MovieUtils.get_movies(Genre.Scifi.value)
    return movies


@app.get("/artista/id/{id}")
async def get_artista(id):
    artista = RequestApi.get_artista(id)
    if "name" not in artista:
        raise HTTPException(
            status_code=404, detail="No person found with id = {id}")
    return {
        "name": artista['name'],
        "id": artista['id'],
        "popularity": artista['popularity'],
        "biography": artista['biography'],
    }



# =================== ROTA get_artista ===================================

# Rota HTTP, onde a função "get_artista"
# é chamada quando uma requisição GET é enviada para o endpoint
# "/artist/name/{nome}".

# A função "get_artista" tem um parâmetro "nome",
#  que é obtido a partir da URL da requisição. 
#  Por exemplo, se a URL da requisição for 
#  "http://example.com/artist/name/Adele", 
#  então o parâmetro "nome" será "Adele".
@app.get("/artist/name/{nome}")# URL que acessará o endpoint para API TMDB
async def get_artista(nome): # Função get_artista
    artista = RequestApi.get_artista_by_name(nome)
    return artista

#==========================================================================


@app.get("/find/{title}/{genre}")
async def find(title: str, genre):
    import json
    data = json.load(open('filmes.json'))
    encontrou = []
    for filme in data:
        # in - contains (ou contem um substring)
        if title.lower() in filme['title'].lower():
            # append - adiciona na lista
            encontrou.append(filme)
    return encontrou


@app.get("/")  # HTTP GET
async def home():
    return {"msg": "pycine back-end"}
