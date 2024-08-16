from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo') #Especificação de validação do titulo
    def validartitulo(cls, value:str): #cls é um parâmetro que recebe a classe em questão, value é o valor de titulo
        #Validacao 1
        palavras = value.split(' ')

        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras')
        
        #Validacao 2
        if value.islower():
            raise ValueError('O título deve estar em capitalize')
        
        return value
    
    @validator('aulas')
    def validaraulas(cls, value: int):
        if value <= 12:
            raise ValueError('O valor de aulas deve ser acima de 12')
        
        return value
        
    @validator('horas')
    def validarhoras(cls, value: int):
        if value <= 10:
            raise ValueError('O valor de aulas deve ser acima de 10') 
        
        return value

cursos = [
    Curso(id=1, titulo='Programação para leigos', aulas=42, horas=56),
    Curso(id=2, titulo='Algoritmos e lógica de programação', aulas=52, horas=66)
]
