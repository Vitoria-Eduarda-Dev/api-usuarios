from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, database, crud, auth

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db)
):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username já registrado")

    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email já registrado")

    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/me", response_model=schemas.UserOut)
def read_current_user(
    current_user: schemas.UserOut = Depends(auth.get_current_user)
):
    return current_user

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(database.get_db)
):
    db_user = crud.get_user(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return db_user

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user)
):
    db_user = crud.update_user(db, user_id, user)

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user)
):
    db_user = crud.delete_user(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return None