from pydantic import BaseModel

class Persona(BaseModel):
    name: str
    age: int
    gender: str
    species: str
    personality: str
    tone: str
    quirks: str
    emotional_depth: int
    communication_style: str