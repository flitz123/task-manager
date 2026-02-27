from pydantic import BaseModel, Emailstr


class UserCreate(BaseModel):
    email: Emailstr
    password: str


class UserOut():
    int: int
    email: Emailstr

    class Config:
        from_attributes = True
