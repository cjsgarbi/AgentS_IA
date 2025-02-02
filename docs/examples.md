# Exemplos de Uso

## 1. Agente Básico Interativo (Repórter)
```python
def main():
    print("""
🎙️ Agente Repórter - Seu Jornalista Virtual! 🎙️

Olá! Eu sou seu repórter virtual, especializado em contar histórias de forma 
dinâmica e envolvente. Posso cobrir qualquer tipo de notícia com aquele 
tempero especial do jornalismo brasileiro!

Como me usar:
- Me faça perguntas sobre notícias e eventos
- Peça por histórias específicas de qualquer lugar
- Digite 'sair' para encerrar nossa conversa
""")

    agent = Agent(
        model=GeminiChat(id="gemini-pro"),
        instructions="""
            Instruções do repórter aqui...
        """,
        markdown=True
    )
    # Loop interativo
    while True:
        user_input = input("\nSua pergunta (ou 'sair' para terminar): ")
        
        if user_input.lower() in ['sair', 'exit', 'quit']:
            break
        
        agent.print_response(user_input, stream=True)
```

## 2. Agente com Ferramentas de Busca (Pesquisador)
```python
def main():
    print("""
🔍 Agente Pesquisador - Seu Investigador de Notícias e Fatos! 🌐

Olá! Sou um agente especializado em pesquisar e trazer informações atualizadas 
da web. Posso buscar notícias, fatos, eventos e qualquer tipo de informação 
atual para você!

Minhas capacidades:
- Buscar notícias em tempo real
- Pesquisar fatos e dados atualizados
- Verificar informações em múltiplas fontes
""")

    agent = Agent(
        model=GeminiChat(id="gemini-pro"),
        tools=[DuckDuckGoTools()],
        instructions="""
            Instruções do pesquisador aqui...
        """,
        markdown=True
    )
    # Loop interativo
    while True:
        user_input = input("\nSua pergunta (ou 'sair' para terminar): ")
        
        if user_input.lower() in ['sair', 'exit', 'quit']:
            break
        
        agent.print_response(user_input, stream=True)
```

> **Nota**: Cada agente deve ter uma apresentação clara de suas capacidades e instruções de uso.

[Mais exemplos...] 