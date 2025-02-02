"""🔍 Web Research Agent - Your AI Research Assistant!

This example shows how to create an AI agent that can search the web for information.
We'll create a research assistant that combines web search with natural conversation.
This demonstrates how to use tools to extend an agent's capabilities.

Example prompts to try:
- "Quais são as últimas notícias sobre IA no Brasil?"
- "Me fale sobre as tendências de tecnologia em 2024"
- "O que está acontecendo no mundo dos esportes hoje?"
- "Quais são as previsões econômicas para este ano?"

Run `pip install agno google-generativeai duckduckgo-search` to install dependencies.
"""

import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.gemini import GeminiChat
from agno.tools.duckduckgo import DuckDuckGoTools
import sys
from agno.utils.cleanup import with_graceful_exit
import google.generativeai as genai


@with_graceful_exit
def main():
    # Verificar API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️ Por favor, configure a variável de ambiente GOOGLE_API_KEY")
        sys.exit(1)

    # Configurar o Gemini
    genai.configure(api_key=api_key)

    # Apresentação inicial limpa
    print(dedent("""
    🔍 Agente Pesquisador - Seu Assistente de Pesquisa Virtual! 🔍

    Olá! Eu sou seu assistente de pesquisa, especializado em buscar e analisar 
    informações da web de forma rápida e precisa. Posso pesquisar qualquer 
    assunto e trazer as informações mais relevantes e atualizadas!

    Como me usar:
    - Me faça perguntas sobre qualquer assunto
    - Peça por informações atualizadas sobre temas específicos
    - Digite 'sair' para encerrar nossa conversa

    Vamos começar? Me faça uma pergunta! 📚
    """).strip() + "\n\n")

    try:
        # Criar o agente pesquisador com o modelo Gemini
        chat_model = GeminiChat(model_id="gemini-pro")

        agent = Agent(
            model=chat_model,
            tools=[DuckDuckGoTools()],
            instructions=dedent("""\
                Você é um pesquisador entusiasmado com talento para explicar! 🔍
                Pense em si mesmo como uma mistura de jornalista investigativo e professor.

                Seu guia de estilo:
                - Comece com um título chamativo usando emoji
                - Faça buscas precisas para encontrar informações atualizadas
                - Organize as informações de forma clara e concisa
                - Use linguagem acessível e exemplos práticos
                - Termine com uma conclusão relevante e uma despedida amigável

                Lembre-se:
                - Sempre verifique as fontes
                - Priorize informações recentes e confiáveis
                - Mantenha um tom profissional mas amigável
                - Use exemplos do contexto brasileiro quando possível\
            """),
            markdown=True,
            show_tool_calls=True,
            add_references=True
        )

        # Loop interativo
        while True:
            user_input = input(
                "\nSua pergunta (ou 'sair' para terminar): ").strip()

            if not user_input or user_input.lower() in ['sair', 'exit', 'quit']:
                break

            agent.print_response(user_input)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nOcorreu um erro: {str(e)}")
    finally:
        print("\nEncerrando o pesquisador... Foi um prazer ajudar você! 🎓")
        sys.exit(0)


if __name__ == "__main__":
    main()

# More example prompts to try:
"""
Try these engaging news queries:
1. "What's the latest development in NYC's tech scene?"
2. "Tell me about any upcoming events at Madison Square Garden"
3. "What's the weather impact on NYC today?"
4. "Any updates on the NYC subway system?"
5. "What's the hottest food trend in Manhattan right now?"
"""
