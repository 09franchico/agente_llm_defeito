
from langchain.agents import AgentExecutor
from src.agentes.agente import AgenteDgb
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI
app = FastAPI()

load_dotenv()


class RequestData(BaseModel):
    texto: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/agente/defeito")
def agente(body: RequestData):
    agente = AgenteDgb()
    executor = AgentExecutor(agent=agente.agente,
                             tools=agente.tools,
                             verbose=True)
    
    resposta = executor.invoke({"input": f"{body.texto}"})
    
    return resposta