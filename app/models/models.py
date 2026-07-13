from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

u = User(
    name="Utkarsh",
    age="1"
)
print(u)
print(type(u.age))
