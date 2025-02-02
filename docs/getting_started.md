# Guia de Instalação Completa - Agno Framework

## 1. Configuração Inicial

### 1.1 Ambiente Virtual
```bash
# Na raiz do projeto
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate
# OU (Linux/Mac)
source venv/bin/activate
```

### 1.2 Instalação Base
```bash
# Instalar Agno em modo desenvolvimento
cd libs/agno
pip install -e .
cd ../..
```

## 2. Provedores de IA

### 2.1 Provedores Principais
```bash
# Google Gemini
pip install google-generativeai

# OpenAI
pip install openai

# Mistral
pip install mistralai

# Anthropic
pip install anthropic

# Azure OpenAI
pip install azure-openai
```

### 2.2 Provedores Adicionais
```bash
# Deepseek
pip install deepseek-ai

# HuggingFace
pip install huggingface_hub

# Together AI
pip install together
```

## 3. Ferramentas e Recursos

### 3.1 Ferramentas de Busca e Pesquisa
```bash
# DuckDuckGo
pip install duckduckgo-search

# Processamento de PDF
pip install pypdf
```

### 3.2 Banco de Dados Vetorial
```bash
# LanceDB e Tantivy
pip install lancedb tantivy
```

### 3.3 Recursos Multimodais
```bash
# Processamento de Imagem
pip install Pillow

# Processamento de Áudio
pip install sounddevice numpy

# Processamento de Vídeo
pip install opencv-python
```

### 3.4 Armazenamento e Cache
```bash
# Redis (opcional - para cache)
pip install redis

# PostgreSQL (opcional - para armazenamento)
pip install psycopg2-binary
```

## 4. Verificação da Instalação

### 4.1 Verificar Dependências
```bash
pip list
```

### 4.2 Testar Configuração
```python
from agno.config import Config
config = Config()
print("Configuração OK!")
```

## 5. Possíveis Problemas

### 5.1 Erros Comuns
- ModuleNotFoundError: Instalar dependência específica
- ImportError: Verificar versão do Python
- API Key Error: Configurar .env

### 5.2 Soluções
- Reinstalar dependências específicas
- Atualizar pip: python -m pip install --upgrade pip
- Verificar compatibilidade de versões

# Guia de Início - Agno Framework

## 1. Sequência de Aprendizado Recomendada

### 1.1 Instalação e Configuração Inicial
1. Preparar ambiente
2. Instalar dependências
3. Configurar chaves API

### 1.2 Primeiros Passos
1. Agente básico (`01_basic_agent.py`)
   - Primeiro contato com o framework
   - Exemplo simples de conversação
   - Personalização básica

## 2. Estrutura do Projeto

### 2.1 Visão Geral
```
agno/
├── .assets/           # Assets do projeto
├── .github/           # Configurações do GitHub
├── cookbook/          # Exemplos e tutoriais
│   └── getting_started/
│       ├── 01_basic_agent.py
│       ├── 02_agent_with_tools.py
│       └── ...
├── docs/             # Documentação
├── evals/            # Avaliações
├── libs/             # Código fonte principal
│   ├── agno/         # Pacote principal
│   │   ├── agno/     # Código fonte
│   │   │   ├── agent/    # Implementação dos agentes
│   │   │   ├── models/   # Provedores de IA
│   │   │   │   ├── anthropic/
│   │   │   │   ├── gemini/
│   │   │   │   ├── mistral/
│   │   │   │   ├── openai/
│   │   │   │   └── ...
│   │   │   ├── tools/    # Ferramentas
│   │   │   └── utils/    # Utilitários
│   │   ├── pyproject.toml
│   │   └── requirements.txt
│   └── infra/        # Infraestrutura
├── scripts/          # Scripts utilitários
├── tests/            # Testes
└── venv/             # Ambiente virtual
```

### 2.2 Principais Componentes

#### Provedores de IA (`libs/agno/agno/models/`)
- `anthropic/` - Modelos Claude
- `gemini/` - Google Gemini
- `mistral/` - Mistral AI
- `openai/` - GPT e DALL-E
- E outros provedores...

#### Ferramentas (`libs/agno/agno/tools/`)
- Ferramentas de busca
- Processamento de documentos
- Análise de dados
- E outras funcionalidades...

## 3. Instalação e Configuração

### 3.1 Preparar Ambiente

# Criar e ativar ambiente virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```
### 3.2 Instalação em Modo Desenvolvimento:
###  A instalação precisa ser feita dentro da pasta libs/agno porque é onde está o pacote principal do framework. Vou explicar:

  1- Estrutura do Projeto:

agno/                      # Raiz do repositório
├── libs/                  # Bibliotecas do projeto
│   └── agno/             # Pacote principal
│       ├── setup.py      # Arquivo de instalação
│       ├── agno/         # Código fonte
│       │   ├── agent/
│       │   ├── models/
│       │   └── tools/
│       └── requirements.txt
├── cookbook/             # Exemplos
└── docs/                # Documentação

  2-Por que essa estrutura?:
O pacote principal (agno) está em libs/agno para:
Separar o código fonte dos exemplos e documentação
Permitir múltiplos pacotes relacionados no futuro
Manter uma estrutura limpa e organizada

  3-Processo de Instalação:

cd libs/agno
pip install -e .  # Instala o pacote em modo desenvolvimento
cd ../..          # Volta para a raiz

- O -e significa "editable" - permite editar o código sem reinstalar
  O . indica para instalar o pacote do diretório .
  
```bash
# Na raiz do repositório (pasta agno)
cd agno  # ou caminho para a raiz do projeto

```bash
# Navegar até o diretório do pacote
cd libs/agno

# Instalar em modo desenvolvimento
pip install -e .

# Voltar para a raiz do projeto
cd ../..
```
# IMPORTANTE: Na raiz do projeto, instalar todas as dependências necessárias

```bash
pip install -U agno  # Instalação básica
pip install google-generativeai  # Para Gemini
pip install duckduckgo-search   # Para ferramentas de busca
pip install lancedb tantivy     # Para base de dados vetorial
```

> **Nota**: Todas as dependências devem ser instaladas na raiz do projeto, onde está o ambiente virtual (venv).

### 3.3 Configurar Provedores

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Adicione e configure as chaves API dos provedores que você pretende usar:
```env
# ==== Provedores de IA ====

# OpenAI (https://platform.openai.com/api-keys)
OPENAI_API_KEY=sua-chave-aqui

# Google Gemini (https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=sua-chave-gemini

# Mistral AI (https://console.mistral.ai/api-keys)
MISTRAL_API_KEY=sua-chave-mistral

# Anthropic Claude (https://console.anthropic.com/account/keys)
ANTHROPIC_API_KEY=sua-chave-anthropic

# Azure OpenAI (https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/OpenAI)
AZURE_OPENAI_API_KEY=sua-chave-azure
AZURE_OPENAI_ENDPOINT=seu-endpoint

# DeepSeek (https://platform.deepseek.ai/api-keys)
DEEPSEEK_API_KEY=sua-chave-deepseek

# HuggingFace (https://huggingface.co/settings/tokens)
HUGGINGFACE_API_KEY=sua-chave-huggingface

# Together AI (https://api.together.xyz/settings/api-keys)
TOGETHER_API_KEY=sua-chave-together

# Cohere (https://dashboard.cohere.ai/api-keys)
COHERE_API_KEY=sua-chave-cohere
```

> **Nota**: Você só precisa configurar as chaves dos provedores que pretende usar. Cada exemplo no `cookbook` indica quais provedores são necessários.

## 4. Executando os Agentes

### 4.1 Navegação Correta para executar os Agentes:
```bash
# IMPORTANTE: Sempre navegue para a pasta correta antes de executar
cd cookbook/getting_started
```
### 4.2 Executando Exemplos
```bash
# Agente básico
python 01_basic_agent.py

# Agente com ferramentas
python 02_agent_with_tools.py

# Outros exemplos...
```

## 5. Catálogo de Agentes

### 5.1 Agentes Básicos
| Arquivo | Descrição | Requisitos |
|---------|-----------|------------|
| `01_basic_agent.py` | Agente conversacional básico | Qualquer provedor de IA |
| `02_agent_with_tools.py` | Agente com ferramentas de busca | DuckDuckGo |
| `03_agent_with_knowledge.py` | Agente com base de conhecimento | Base de dados vetorial |
| `04_agent_with_storage.py` | Agente com armazenamento persistente | Sistema de arquivos |

### 5.2 Agentes de Equipe e Estruturados
| Arquivo | Descrição | Requisitos |
|---------|-----------|------------|
| `05_agent_team.py` | Múltiplos agentes trabalhando juntos | Múltiplos provedores |
| `06_structured_output.py` | Saída em formato estruturado | Qualquer provedor |
| `07_write_your_own_tool.py` | Como criar ferramentas customizadas | - |

### 5.3 Agentes de Pesquisa
| Arquivo | Descrição | Requisitos |
|---------|-----------|------------|
| `08_research_agent_exa.py` | Agente especializado em pesquisa | DuckDuckGo |
| `09_research_workflow.py` | Fluxo completo de pesquisa | DuckDuckGo + Base de dados |

### 5.4 Agentes Multimodais
| Arquivo | Descrição | Requisitos |
|---------|-----------|------------|
| `10_image_agent.py` | Processamento de imagens | Gemini/OpenAI |
| `11_generate_image.py` | Geração de imagens | DALL-E/Stable Diffusion |
| `12_generate_video.py` | Geração de vídeos | Provedor compatível |
| `13_audio_input_output.py` | Processamento de áudio | Provedor de áudio |

### 5.5 Agentes com Estado e Contexto
| Arquivo | Descrição | Requisitos |
|---------|-----------|------------|
| `14_agent_state.py` | Gerenciamento de estado | Qualquer provedor |
| `15_agent_context.py` | Gerenciamento de contexto | Qualquer provedor |
| `16_agent_session.py` | Gerenciamento de sessão | Sistema de armazenamento |
| `17_user_memories_and_summaries.py` | Memória e resumos | Base de dados |

### 5.6 Agentes Especiais
| Arquivo | Descrição | Requisitos |
|---------|-----------|------------|
| `18_retry_function_call.py` | Retentativas automáticas | Qualquer provedor |

## 6. Configuração das APIs e Uso dos Agentes

### 6.1 Configurar APIs no .env
```bash
# 1. Copiar arquivo de exemplo
cp .env.example .env

# 2. Editar o arquivo .env com suas chaves
```

### 6.2 Onde Obter as Chaves API
| Provedor | Onde Obter | Variável no .env |
|----------|------------|------------------|
| Google Gemini | [Google AI Studio](https://makersuite.google.com/app/apikey) | `GOOGLE_API_KEY` |
| OpenAI | [OpenAI Platform](https://platform.openai.com/api-keys) | `OPENAI_API_KEY` |
| Mistral | [Mistral Platform](https://console.mistral.ai/) | `MISTRAL_API_KEY` |
| Anthropic | [Anthropic Console](https://console.anthropic.com/) | `ANTHROPIC_API_KEY` |
| HuggingFace | [HuggingFace Settings](https://huggingface.co/settings/tokens) | `HUGGINGFACE_API_KEY` |

### 6.3 Testando os Agentes
1. **Agente Básico (Gemini)**:
```bash
cd cookbook/getting_started
python 01_basic_agent.py  # Requer GOOGLE_API_KEY
```

2. **Agente com Busca**:
```bash
python 02_agent_with_tools.py  # Requer GOOGLE_API_KEY + DuckDuckGo
```

3. **Agente com Imagens**:
```bash
python 10_image_agent.py  # Requer GOOGLE_API_KEY ou OPENAI_API_KEY
```

### 6.4 Requisitos por Tipo de Agente
| Tipo de Agente | APIs Necessárias | Bibliotecas Extras |
|----------------|------------------|-------------------|
| Básico | Qualquer provedor | Nenhuma |
| Busca | Provedor + DuckDuckGo | duckduckgo-search |
| Imagem | Gemini/OpenAI | Pillow |
| Áudio | OpenAI Whisper | sounddevice |
| Pesquisa | Provedor + DuckDuckGo | duckduckgo-search + lancedb |