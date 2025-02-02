"""🧠 Recipe Expert with Knowledge - Your AI Thai Cooking Assistant!

This example shows how to create an AI cooking assistant that combines knowledge from a
curated recipe database with web searching capabilities. The agent uses a PDF knowledge base
of authentic Thai recipes and can supplement this information with web searches when needed.

Example prompts to try:
- "How do I make authentic Pad Thai?"
- "What's the difference between red and green curry?"
- "Can you explain what galangal is and possible substitutes?"
- "Tell me about the history of Tom Yum soup"
- "What are essential ingredients for a Thai pantry?"
- "How do I make Thai basil chicken (Pad Kra Pao)?"

Run `pip install google-generativeai lancedb tantivy pypdf duckduckgo-search agno` to install dependencies.

# Bibliotecas necessárias:
# - google-generativeai: Para configurar e interagir com o modelo de linguagem Gemini.
# - lancedb: Banco de dados vetorial para armazenar e pesquisar informações na base de conhecimento.
# - tantivy: Motor de busca para indexar e buscar informações textuais.
# - pypdf: Para manipular e extrair informações de arquivos PDF.
# - duckduckgo-search: Para realizar buscas na web quando necessário.
# - agno: Biblioteca principal que integra todas as funcionalidades para criar o agente de IA.
"""

from textwrap import dedent
import os
import google.generativeai as genai
from pathlib import Path
import tempfile
import atexit

from agno.agent import Agent
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.gemini import GeminiChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.google import GeminiEmbedder

# Criar diretório temporário seguro
temp_dir = tempfile.mkdtemp()
db_path = Path(temp_dir) / "lancedb"
db_path.mkdir(parents=True, exist_ok=True)

# Verificar API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "⚠️ Por favor, configure a variável de ambiente GOOGLE_API_KEY")

# Configurar o Gemini
genai.configure(api_key=api_key)

# Create a Recipe Expert Agent with knowledge of Thai recipes
agent = Agent(
    model=GeminiChat(model_id="gemini-pro"),
    instructions=dedent("""\
        You are a passionate and knowledgeable Thai cuisine expert! 🧑‍🍳
        Think of yourself as a combination of a warm, encouraging cooking instructor,
        a Thai food historian, and a cultural ambassador.

        Follow these steps when answering questions:
        1. First, search the knowledge base for authentic Thai recipes and cooking information
        2. If the information in the knowledge base is incomplete OR if the user asks a question better suited for the web, search the web to fill in gaps
        3. If you find the information in the knowledge base, no need to search the web
        4. Always prioritize knowledge base information over web results for authenticity
        5. If needed, supplement with web searches for:
            - Modern adaptations or ingredient substitutions
            - Cultural context and historical background
            - Additional cooking tips and troubleshooting

        Communication style:
        1. Start each response with a relevant cooking emoji
        2. Structure your responses clearly:
            - Brief introduction or context
            - Main content (recipe, explanation, or history)
            - Pro tips or cultural insights
            - Encouraging conclusion
        3. For recipes, include:
            - List of ingredients with possible substitutions
            - Clear, numbered cooking steps
            - Tips for success and common pitfalls
        4. Use friendly, encouraging language

        Special features:
        - Explain unfamiliar Thai ingredients and suggest alternatives
        - Share relevant cultural context and traditions
        - Provide tips for adapting recipes to different dietary needs
        - Include serving suggestions and accompaniments

        End each response with an uplifting sign-off like:
        - 'Happy cooking! ขอให้อร่อย (Enjoy your meal)!'
        - 'May your Thai cooking adventure bring joy!'
        - 'Enjoy your homemade Thai feast!'

        Remember:
        - Always verify recipe authenticity with the knowledge base
        - Clearly indicate when information comes from web sources
        - Be encouraging and supportive of home cooks at all skill levels\
    """),
    knowledge=PDFUrlKnowledgeBase(
        urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=LanceDb(
            uri=str(db_path),
            table_name="recipe_knowledge",
            search_type=SearchType.hybrid,
            embedder=GeminiEmbedder(),
        ),
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    add_references=True,
)

# Garantir que o conhecimento seja carregado
if agent.knowledge is not None:
    try:
        print("Carregando base de conhecimento...")
        agent.knowledge.load()
        print("Base de conhecimento carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar conhecimento: {str(e)}")
        raise

# Função para limpar recursos


def cleanup():
    try:
        if agent and agent.model and hasattr(agent.model, 'client'):
            agent.model.client = None
        if 'genai' in globals():
            genai._client = None
    except Exception as e:
        print(f"Erro ao limpar recursos: {str(e)}")


# Registrar função de limpeza para ser chamada no encerramento
atexit.register(cleanup)

# Testar o agente
print("\nTestando o agente...\n")
agent.print_response(
    "How do I make chicken and galangal in coconut milk soup"
)
agent.print_response("What is the history of Thai curry?")
agent.print_response("What ingredients do I need for Pad Thai?")

# Limpar recursos antes de encerrar
cleanup()

# More example prompts to try:
"""
Explore Thai cuisine with these queries:
1. "What are the essential spices and herbs in Thai cooking?"
2. "Can you explain the different types of Thai curry pastes?"
3. "How do I make mango sticky rice dessert?"
4. "What's the proper way to cook Thai jasmine rice?"
5. "Tell me about regional differences in Thai cuisine"
"""
