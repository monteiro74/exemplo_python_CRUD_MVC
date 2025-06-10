# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: documentador.py - Gerador de documentação técnica em Markdown
# Descrição: Este script percorre a estrutura do projeto, extrai conteúdos e gera
#            o arquivo documentacao.md com trechos de código, estruturas de diretórios,
#            diagramas Mermaid (UML) e detalhes adicionais como logs e imagens.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - os, datetime: Para manipulação de arquivos e metadados.
# - markdown, Mermaid (markdown formatado)
#
# Uso: Execute o script a partir da raiz do projeto:
#      $ python documentador.py
#      A documentação será salva em: documentacao/documentacao.md
# ==============================================================================

import os
from datetime import datetime

PASTAS = [
    "db_script", "model", "controller", "view", "images", "logs", "documentacao"
]

EXTENSOES_DOCUMENTADAS = [".py", ".sql", ".md", ".txt"]
CAMINHO_SAIDA = os.path.join("documentacao", "documentacao.md")

def gerar_cabecalho_markdown():
    agora = datetime.now()
    data = agora.strftime("%Y-%m-%d")
    hora = agora.strftime("%H:%M:%S")
    return f"""<!--
==============================================================================
Nome do Arquivo: documentacao.md - Documentação Técnica Consolidada
Descrição: Este arquivo documenta toda a estrutura, funcionalidades e scripts
           do sistema de gerenciamento de alunos e pets.
Autor: Nome do aluno
Data de Geração: {data}
Hora de Geração: {hora}
==============================================================================
-->
"""

def obter_estrutura_mermaid(base_dir="."):
    estrutura = ["```mermaid", "graph TD"]
    for pasta_raiz, subpastas, _ in os.walk(base_dir):
        if any(pasta_raiz.startswith(os.path.join(base_dir, p)) for p in PASTAS):
            pasta_relativa = os.path.relpath(pasta_raiz, base_dir)
            for subpasta in subpastas:
                estrutura.append(f'    {pasta_relativa.replace(os.sep, "_")} --> {os.path.join(pasta_relativa, subpasta).replace(os.sep, "_")}')
    estrutura.append("```")
    return "\n".join(estrutura)

def ler_arquivo_comentado(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        nome_arquivo = os.path.basename(caminho_arquivo)
        return f"### 📄 {nome_arquivo}\n\n```{nome_arquivo.split('.')[-1]}\n{conteudo}\n```\n"
    except Exception as e:
        return f"> ⚠️ Erro ao ler {caminho_arquivo}: {e}\n"

def incluir_imagem():
    caminho_img = os.path.join("images", "wallpaper.jpg")
    if os.path.exists(caminho_img):
        return "### 🖼️ Wallpaper do Sistema\n\n![Wallpaper](../images/wallpaper.jpg)\n"
    return "> Imagem wallpaper.jpg não encontrada na pasta images.\n"

def gerar_diagramas_mermaid():
    return """
## 📊 Diagramas UML (Mermaid)

### 📦 Diagrama de Pacotes

```mermaid
graph LR
    Main --> View
    Main --> Controller
    Main --> Model
    View -->|usa| Controller
    Controller -->|acessa| Model
    Model -->|conecta| DB[(MySQL)]
```

### 🧭 Diagrama de Navegação

```mermaid
flowchart TD
    Menu[Menu Principal] --> GridAlunos
    Menu --> FormAlunos
    Menu --> GridPets
    Menu --> FormIdade
    Menu --> FormQuantidade
    Menu --> ReportPDF
    Menu --> Sobre
    Menu --> Licenca
```

### 🧱 Diagrama de Classes Simplificado

```mermaid
classDiagram
    class Aluno {
        +matricula: str
        +nome: str
        +curso: str
        +idade: int
        +sexo: str
        +foto: blob
    }
    class Pet {
        +id: int
        +apelido: str
        +raca: str
        +data_nascimento: date
        +cpf_dono: str
    }
    class ConexaoDB {
        +ler_conexao()
        +obter_conexao()
    }
    Aluno --> Pet : "1 tem N"
    ConexaoDB <.. Aluno : usa
    ConexaoDB <.. Pet : usa
```
"""

def gerar_documentacao():
    markdown = [gerar_cabecalho_markdown()]
    markdown.append("# 📚 Documentação do Projeto\n")
    markdown.append("## 🗂️ Estrutura de Pastas\n")
    markdown.append(obter_estrutura_mermaid())

    for pasta in PASTAS:
        markdown.append(f"\n## 📁 Pasta `{pasta}/`\n")
        caminho_absoluto = os.path.join(".", pasta)
        if not os.path.exists(caminho_absoluto):
            markdown.append(f"> Pasta `{pasta}/` não encontrada.\n")
            continue
        for raiz, _, arquivos in os.walk(caminho_absoluto):
            for arquivo in arquivos:
                if arquivo == "logs.csv":
                    continue
                extensao = os.path.splitext(arquivo)[1]
                if extensao in EXTENSOES_DOCUMENTADAS:
                    caminho_arquivo = os.path.join(raiz, arquivo)
                    markdown.append(ler_arquivo_comentado(caminho_arquivo))

    markdown.append(incluir_imagem())
    markdown.append(gerar_diagramas_mermaid())

    markdown.append("\n---\n")
    markdown.append("### 📌 Notas Finais\n")
    markdown.append("- Esta documentação foi gerada automaticamente por `documentador.py`.\n")
    markdown.append("- Diagramas podem ser visualizados em plataformas que suportam Mermaid (GitHub, Obsidian etc).\n")

    os.makedirs("documentacao", exist_ok=True)
    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown))
    print(f"✅ Documentação gerada em: {CAMINHO_SAIDA}")

if __name__ == "__main__":
    gerar_documentacao()
