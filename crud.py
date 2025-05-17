# crud.py
from fastapi import APIRouter, Depends, HTTPException
from typing import TypeVar, Generic, Type, List
from sqlmodel import SQLModel, Session, select
from db import get_session

ModelType = TypeVar("ModelType", bound=SQLModel)

class CRUDRouter(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], prefix: str):
        self.model = model
        self.router = APIRouter(prefix=prefix, tags=[model.__name__])

        @self.router.get("/", response_model=List[model])
        def list_items(session: Session = Depends(get_session)):
            return session.exec(select(model)).all()

        @self.router.post("/", response_model=model)
        def create_item(item: model, session: Session = Depends(get_session)):
            session.add(item)
            session.commit()
            session.refresh(item)
            return item

        @self.router.get("/{item_id}", response_model=model)
        def get_item(item_id: str, session: Session = Depends(get_session)):
            obj = session.get(model, item_id)
            if not obj:
                raise HTTPException(404, detail="Not found")
            return obj

        @self.router.put("/{item_id}", response_model=model)
        def update_item(item_id: str, item: model, session: Session = Depends(get_session)):
            existing = session.get(model, item_id)
            if not existing:
                raise HTTPException(404, detail="Not found")
            for key, val in item.dict(exclude_unset=True).items():
                setattr(existing, key, val)
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

        @self.router.delete("/{item_id}")
        def delete_item(item_id: str, session: Session = Depends(get_session)):
            obj = session.get(model, item_id)
            if not obj:
                raise HTTPException(404, detail="Not found")
            session.delete(obj)
            session.commit()
            return {"deleted": True}
