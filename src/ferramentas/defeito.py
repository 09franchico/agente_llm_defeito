from langchain.prompts import PromptTemplate
from pydantic import BaseModel , Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import BaseTool
import json



def busca_dados_de_defeito(etiqueta):
    return {
        "defeito":"Error de solda na placa",
        "profissinal":"Francisco",
        "departamento":"Producao",
        "cargo":"Engenheiro",
        
    }


#-------------------------------------------------------------------------------------
class ExtratorDeEtiqueta(BaseModel):
    etiqueta:str = Field("Etiqueta ER ou 8S do sistema, sempre em letras minúsculas.")



class MostrarDefeito(BaseTool):
    
    name:str = "MostrarDefeito"
    description:str = """Esta ferramenta mostra qual foi o defeito de uma etiquera ER. Passe para essa ferramenta como argumento a etiqueta ER."""
    
    
    def _run(self, input: str) -> str:
        
        # llm = ChatDeepSeek(
        #         model= "deepseek-chat",
        #         temperature=0,
        #     )
        
        # llm = ChatOllama(
        #         model="gemma3:4b",
        #         temperature=0.3,
        #     )
        llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0,
               )
        
        parser = JsonOutputParser(pydantic_object=ExtratorDeEtiqueta)
        template = PromptTemplate(template="""Você deve analisar a entrada a seguir e extrair a etiqueta informada em minúsculo.
                        Entrada:
                        -----------------
                        {input}
                        -----------------
                        Formato de saída:
                        {formato_saida}""",
                        input_variables=["input"],
                        partial_variables={"formato_saida" : parser.get_format_instructions()}
                        
                        )
        
        
        cadeia = template | llm | parser
        resposta = cadeia.invoke({"input" : input})
        etiqueta = resposta['etiqueta']
        etiqueta = etiqueta.lower().strip()
        
        dados = busca_dados_de_defeito(etiqueta)
        
        return json.dumps(dados)