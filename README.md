<div align="center" id="top">
<a href="https://docs.agno.com">
<picture>
<source media="(prefers-color-scheme: dark)" srcset=".assets/logo-dark.svg">
<source media="(prefers-color-scheme: light)" srcset=".assets/logo-light.svg">
<img src=".assets/logo-light.svg" alt="Agno">
</picture>
</a>
</div>

<div align="center">
<a href="https://docs.agno.com">📚 Documentação</a> &nbsp;|&nbsp;
<a href="https://docs.agno.com/examples/introduction">💡 Exemplos</a> &nbsp;|&nbsp;
<a href="https://github.com/agno-agi/agno/stargazers">🌟 Star Us</a>
</div>

# Índice

- [Sobre o Agno](#sobre-o-agno)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Exemplos de Uso](#exemplos-de-uso)
- [Recursos Avançados](#recursos-avançados)
- [Documentação e Suporte](#documentação-e-suporte)

## Sobre o Agno

O [Agno](https://docs.agno.com) é uma estrutura leve para construir agentes multimodais de IA, projetado com três princípios básicos:

- **Simplicidade**: Sem complexidades - apenas Python puro
- **Desempenho**: Agentes extremamente rápidos com mínimo uso de memória
- **Agnóstico**: Compatível com qualquer modelo, provedor ou modalidade

### Principais Recursos

- 🚀 **Ultra Rápido**: 6000x mais rápido que alternativas similares
- 🔄 **Multi Modal**: Suporte para texto, imagem, áudio e vídeo
- 🤝 **Multi Agent**: Trabalho em equipe entre agentes especializados
- 💾 **Gerenciamento de Memória**: Armazenamento eficiente de sessões
- 📊 **Monitoramento**: Acompanhamento em tempo real via [agno.com](https://app.agno.com)

## Instalação

### 1. Requisitos Básicos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Ambiente virtual (recomendado)

### 2. Configuração do Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate
```

### 3. Instalação do Agno

```bash
# Instalação básica
pip install -U agno

# Para desenvolvimento
pip install -e .
```

### 4. Dependências Opcionais

Escolha as dependências conforme sua necessidade:

```bash
# Para busca web
pip install duckduckgo-search

# Para processamento de PDF e banco vetorial
pip install lancedb tantivy pypdf

# Para Google Gemini
pip install google-generativeai

# Para dados financeiros
pip install yfinance
```

## Configuração

### 1. Variáveis de Ambiente

Primeiro, copie o arquivo de exemplo:

```bash
cp .env.example .env
```

### 2. Chaves API dos Provedores

Configure as chaves API dos provedores que você pretende usar:

#### Provedores Principais

```env
# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# Google (Gemini)
GOOGLE_API_KEY=your-google-api-key-here
VERTEX_PROJECT=your-vertex-project-id    # Opcional - para VertexAI
VERTEX_LOCATION=your-vertex-location     # Opcional - para VertexAI

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=your-azure-endpoint
AZURE_OPENAI_API_VERSION=2024-02-15
AZURE_DEPLOYMENT=your-deployment-name
```

#### Provedores Adicionais

```env
# AWS (Bedrock)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=your-aws-region

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-key

# Cohere
COHERE_API_KEY=your-cohere-key

# HuggingFace
HUGGINGFACE_API_KEY=your-huggingface-key

# Mistral
MISTRAL_API_KEY=your-mistral-key

# Together AI
TOGETHER_API_KEY=your-together-key

# Nvidia
NVIDIA_API_KEY=your-nvidia-key
NVIDIA_API_URL=https://api.nvidia.com/v1/

# Ollama (Local)
OLLAMA_HOST=http://localhost:11434

# OpenRouter
OPENROUTER_API_KEY=your-openrouter-key

# Outros Provedores
SAMBANOVA_API_KEY=your-sambanova-key
XAI_API_KEY=your-xai-key              # Para Grok
FIREWORKS_API_KEY=your-fireworks-key
INTERNLM_API_KEY=your-internlm-key
DEEPSEEK_API_KEY=your-deepseek-key
GROQ_API_KEY=your-groq-key
```

### 3. Configurações do Framework

#### Configurações Gerais

```env
# Telemetria (opcional)
AGNO_TELEMETRY=true    # Define como false para desabilitar

# Cache
AGNO_CACHE_DIR=.cache  # Diretório para cache

# Logging
AGNO_LOG_LEVEL=INFO    # Opções: DEBUG, INFO, WARNING, ERROR
```

#### Banco de Dados Vetorial

```env
# Configurações do banco vetorial
VECTOR_DB_URI=tmp/lancedb        # Caminho do banco de dados
VECTOR_DB_TABLE=default          # Nome da tabela padrão
```

#### Configurações de Memória

```env
# Backend de memória
MEMORY_BACKEND=local    # Opções: local, redis, postgres
MEMORY_TTL=3600        # Tempo de vida em segundos

# Configurações Redis (se usar MEMORY_BACKEND=redis)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your-password     # Se necessário

# Configurações Postgres (se usar MEMORY_BACKEND=postgres)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=agno
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
```

#### Limites de Taxa

```env
# Rate Limiting
RATE_LIMIT_ENABLED=true     # Ativar/desativar limite de taxa
RATE_LIMIT_REQUESTS=100     # Número máximo de requisições
RATE_LIMIT_WINDOW=60        # Janela de tempo em segundos
```

### 4. Onde Obter as Chaves API

- OpenAI: <https://platform.openai.com/api-keys>
- Google (Gemini): <https://makersuite.google.com/app/apikey>
- Azure: <https://portal.azure.com>
- AWS: <https://aws.amazon.com/console/>
- Anthropic: <https://console.anthropic.com>
- Cohere: <https://dashboard.cohere.com/api-keys>
- HuggingFace: <https://huggingface.co/settings/tokens>
- Mistral: <https://console.mistral.ai/api-keys/>
- Together AI: <https://api.together.xyz/settings/api-keys>
- OpenRouter: <https://openrouter.ai/keys>

### 5. Verificação da Configuração

Para verificar se suas variáveis de ambiente estão configuradas corretamente:

```python
from agno.config import Config

config = Config()
print(config.get_provider_key("openai"))  # Deve mostrar sua chave OpenAI
```

> **Nota**: Mantenha suas chaves API seguras e nunca as compartilhe ou cometa no controle de versão.

## Exemplos de Uso

### Exemplo Básico

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    description="Assistente amigável",
    markdown=True
)
agent.print_response("Olá, como posso ajudar?", stream=True)
```

### Exemplo com Gemini

```python
from agno.agent import Agent
from agno.models.gemini import GeminiChat

agent = Agent(
    model=GeminiChat(
        api_key="SUA_CHAVE_API_GEMINI",
        model="gemini-pro",
        temperature=0.7
    ),
    description="Assistente Gemini",
    markdown=True
)
```

### Exemplo com Ferramentas Web

```python
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    description="Assistente com acesso à web",
    tools=[DuckDuckGoTools()],
    show_tool_calls=True
)
```

## Recursos Avançados

### Banco de Dados Vetorial

```python
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType

agent = Agent(
    # ... configuração básica ...
    knowledge=PDFUrlKnowledgeBase(
        urls=["seu_arquivo.pdf"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="conhecimento"
        )
    )
)
```

### Equipe de Agentes

```python
web_agent = Agent(
    nome="Agente Web",
    função="Pesquisar na web",
    tools=[DuckDuckGoTools()]
)

finance_agent = Agent(
    nome="Agente Financeiro",
    função="Análise financeira",
    tools=[YFinanceTools()]
)

team = Agent(team=[web_agent, finance_agent])
```

## Documentação e Suporte

- 📚 [Documentação Completa](https://docs.agno.com)
- 💡 [Exemplos Detalhados](https://docs.agno.com/examples/introduction)
- 💬 [Comunidade Discord](https://discord.gg/4MtYHHrgA8)
- 🤝 [Fórum da Comunidade](https://community.agno.com/)

## Contribuindo

Contribuições são bem-vindas! Consulte nosso [guia de contribuição](CONTRIBUTING.md).

---

<p align="center">
<a href="#top">⬆️ Voltar ao topo</a>
</p>
