from langchain.agents import create_openai_tools_agent, create_react_agent
from langchain import hub
from langchain.agents import Tool
from src.ferramentas.defeito import MostrarDefeito
from src.ferramentas.resolver_defeito import ResolverDefeito
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI




class AgenteDgb:
    
    def __init__(self):
        
        # llm = ChatDeepSeek(
        #         model= "deepseek-chat",
        #         temperature=0.2,
        # )
        
        # llm = ChatOllama(
        #     model="gemma3:4b",
        #     temperature=0.1,
        #     )
        
        llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0,
               )
        
        #Instancia a ferramenta
        defeito = MostrarDefeito()
        resolver_defeito = ResolverDefeito()
    
        
        #Cria as ferramentas
        self.tools = [
            Tool(
                name = defeito.name,
                func = defeito.run,
                description = defeito.description,
                return_direct = False
                
                ),
            Tool(
                name=resolver_defeito.name,
                func=resolver_defeito.run,
                description=resolver_defeito.description,
                return_direct = False
            )
        ]


        # react
        prompt = hub.pull("hwchase17/react")
        self.agente = create_react_agent(llm, self.tools, prompt)
