#Imports gerais
from models import Curso
from typing import Optional
from time import sleep
from typing import Any
from typing import Dict, List
from models import cursos
#from fastapi.responses import JSONResponse

#Imports FastAPI
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header
from fastapi import Depends

def fakeDb():
    try:
        print('Abrindo a conexão com o Banco de dados...')
        sleep(1)
    finally:
        print('Fechando a conexão com o Banco de dados...')
        sleep(1)

app = FastAPI(
    title='API de Cursos da Geek University',
    version= '0.0.1',
    description= 'Uma API para estudo da FastAPI'
    )



@app.get('/cursos', description = 'Retorna todos os cursos existentes no banco de dados da API', summary = 'Retorna todos os cursos', response_model= List[Curso], response_description='Cursos encontrados com sucesso')
async def getcursos(db: Any = Depends(fakeDb)):
    return cursos

@app.get('/cursos/{curso_id}', description= 'Retorna apenas um curso do banco de dados de acordo com o ID digitado na URI de pesquisa', summary='Retorna apenas um curso de acordo com o ID fornecido') #Request HTTP GET na URL /cursos/id do curso (ainda não definido)
async def getcurso(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fakeDb)): #Definindo a função que irá realizar o GET, recebendo como parametro o curso_id digitado pelo usuário na URL, definindo como inteiro para não dar erro de servidor #500
    try:
        curso = cursos[curso_id]
        return curso #Definindo a variável curso a partir dos dados de cursos no index curso_id obtido na URL digitada pelo usuário
    #curso.update({'id': curso_id}) #Alterando os dados NESTA REQUISIÇÃO EM ESPECIFICO e inserindo o id no objeto cursos a partir do número digitado pelo usuário
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')
    
@app.post('/cursos', status_code=status.HTTP_201_CREATED, description='Envia um curso para a API a partir das informações fornecidas no body da requisição HTTP', summary='Envia informações ao banco de dados', response_model=Curso)
async def postcurso(curso: Curso, db: Any = Depends(fakeDb)):
    #if curso.id not in cursos: modo inicial de acessar cursos
        next_id: int = len(cursos) + 1
        curso.id = next_id
        cursos.append(curso)
        return curso
    #else:
    #    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Já existe um curso com ID {curso.id}.')

@app.put('/cursos/{curso_id}', description='Altera um curso e suas informações no banco de dados a partir do ID obtido na URI e das informações do body da requisição HTTP', summary='Altera as informações de cursos de acordo com ID e Body')
async def putcurso(curso_id: int, curso: Curso, db: Any = Depends(fakeDb)):    
    if curso_id in cursos:
        cursos[curso_id] = curso
        #curso.id = curso_id podemos atualizar o id dessa forma também, ou excluir como feito anteriormente e abaixo
        del curso.id
        return curso
    
    else:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')


@app.delete('/cursos/{curso_id}', description='Deleta um curso a partir do seu ID obtido na URI', summary='Deleta um curso a partir do ID')
async def delcurso(curso_id: int, db: Any = Depends(fakeDb)):
    if curso_id in cursos:
        del cursos[curso_id]
        del curso_id
        #return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')
    
@app.get('/calculadora', description='Soma os valores obtidos na URI', summary='Soma até 3 valores obtidos na URI')
async def calculadora(a: int = Query(default = None, gt=5), b: int = Query(default = None, gt=10), c: Optional[int] = Query(default = None, gt=10), x_geek: str = Header(default=None), db: Any = Depends(fakeDb)):
    soma = a + b
    if c:
        soma += c

    print(f'X_GEEK: {x_geek}')

    return {"resultado" : soma}




if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host= '0.0.0.0', port=8000, debug= True, reload=True)

