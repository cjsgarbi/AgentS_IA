"""
==== Configuração Central do Pacote Agno ====

Este arquivo é o ponto central de configuração do pacote agno.
Define dependências, versão e requisitos de instalação.

Funções principais:
1. Especificar todas as dependências necessárias
2. Definir a versão do pacote
3. Configurar a instalação do projeto

Como usar:
    cd libs/agno
    pip install -e .

Isso instalará o pacote em modo desenvolvimento, permitindo
editar o código sem precisar reinstalar.
"""

from setuptools import setup, find_packages

setup(
    name="agno",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",  # Necessário para o provedor Gemini
        "duckduckgo-search",    # Para ferramentas de busca
        "lancedb",              # Para banco de dados vetorial
        "tantivy",             # Para busca e indexação
    ],
    python_requires=">=3.8",
)
