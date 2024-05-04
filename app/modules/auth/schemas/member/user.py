from pydantic import BaseModel


class OrmModeBaseModel(BaseModel):
    class Config:
        from_attributes = True
