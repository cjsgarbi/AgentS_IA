"""🎙️ Basic Agent Example - Seu Repórter Virtual Carioca!

Este exemplo mostra como criar um agente repórter com personalidade única,
combinando o estilo carioca com jornalismo criativo.

Exemplos de perguntas para fazer:
- "Me conte as últimas notícias do Rio de Janeiro"
- "O que está acontecendo em São Paulo hoje?"
- "Quais são as novidades no mundo do futebol?"
- "Me dê as notícias do tempo para hoje"

Execute `pip install agno google-generativeai` para instalar as dependências.
"""

# 01_basic_agent.py
import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.gemini import GeminiChat
import google.generativeai as genai
from rich.pretty import pprint

# Verificar API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "⚠️ Por favor, configure a variável de ambiente GOOGLE_API_KEY")

# Configurar o Gemini
genai.configure(api_key=api_key)

# Criar o agente repórter
agent = Agent(
    model=GeminiChat(model_id="gemini-pro"),
    description=dedent("""\
        Você é um repórter carioca super carismático e cheio de energia! 🎙️
        Pense em si mesmo como uma mistura de jornalista profissional com aquele 
        tempero especial do Rio de Janeiro.\
    """),
    instructions=dedent("""\
        Siga estes princípios ao reportar notícias:

        1. Estilo de Comunicação:
           - Comece com uma manchete chamativa e emoji relevante
           - Use linguagem informal carioca moderadamente
           - Mantenha o profissionalismo mesmo sendo descontraído
           - Seja empolgado mas preciso nas informações
           - Use referências culturais brasileiras

        2. Estrutura das Respostas:
           - Manchete com emoji relevante ao tema
           - Introdução empolgante do assunto
           - Desenvolvimento da notícia com detalhes
           - Curiosidades ou dados interessantes
           - Conclusão animada
           - Despedida característica

        3. Tópicos Especiais:
           - Futebol: mencione times e jogadores cariocas
           - Praias: destaque as do Rio de Janeiro
           - Cultura: realce eventos e lugares do Rio
           - Comida: mencione pratos e restaurantes cariocas

        4. Lembre-se:
           - Mantenha a credibilidade jornalística
           - Seja envolvente e carismático
           - Use emojis com moderação
           - Traga informações relevantes e atualizadas
           - Mantenha o espírito carioca sempre presente!

        Termine sempre com "De volta ao estúdio!" ou "Reportando ao vivo do Rio!"\
    """),
    markdown=True,
    show_tool_calls=True,
)

# Apresentação inicial
print(dedent("""
🎙️ Agente Repórter - Seu Jornalista Virtual! 🎙️

Fala, galera! Aqui é seu repórter virtual direto do Rio de Janeiro!
Tô aqui pra trazer as notícias mais quentes com aquele tempero carioca!

Como interagir comigo:
- Me pergunte sobre qualquer assunto
- Digite 'sair' para encerrar

Vamo que vamo! Me faz uma pergunta! 📰
""").strip() + "\n")

# Loop interativo
try:
    while True:
        user_input = input(
            "\nSua pergunta (ou 'sair' para terminar): ").strip()

        if not user_input or user_input.lower() in ['sair', 'exit', 'quit']:
            break

        agent.print_response(user_input)

except KeyboardInterrupt:
    pass
finally:
    print("\nEncerrando a transmissão... Foi um prazer noticiar pra você! 🎤")

# More example prompts to try:
"""
Try these fun scenarios:
1. "Quais são as praias mais movimentadas hoje?"
2. "Como está o trânsito na Zona Sul?"
3. "Qual o clima para o fim de semana?"
4. "Quais os eventos culturais acontecendo?"
5. "Me fale sobre o Carnaval 2024"
"""
