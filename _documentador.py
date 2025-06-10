# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: gerar_documentacao.py - Gerador de documentação técnica em Markdown
# Descrição: Este script percorre as pastas do projeto, extrai os conteúdos relevantes
#            e gera um único arquivo 'documentacao.md' contendo comentários, trechos de código,
#            estrutura em Mermaid e anotações técnicas.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - os: Para percorrer diretórios e manipular caminhos.
# - datetime: Para gerar data e hora no cabeçalho da documentação.
#
# Uso: Execute este script a partir da raiz do projeto para gerar a documentação:
#      $ python gerar_documentacao.py
#      O arquivo será salvo em: documentacao/documentacao.md
# ==============================================================================

import os
from datetime import datetime

PASTAS = [
    "db_script", "model", "controller", "view", "images", "logs", "documentacao"
]

EXTENSOES_DOCUMENTADAS = [".py", ".sql", ".md", ".txt"]
CAMINHO_SAIDA = os.path.join("documentacao", "documentacao.md")

def obter_estrutura_mermaid(base_dir="projeto"):
    estrutura = ["```mermaid", "graph TD"]
    for pasta_raiz, subpastas, _ in os.walk(base_dir):
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

def gerar_documentacao():
    markdown = [gerar_cabecalho_markdown()]
    markdown.append("# 📚 Documentação do Projeto\n")

    markdown.append("## 🗂️ Estrutura de Pastas\n")
    markdown.append(obter_estrutura_mermaid())

    for pasta in PASTAS:
        markdown.append(f"\n## 📁 Pasta `{pasta}/`\n")
        caminho_absoluto = os.path.join(os.getcwd(), pasta)
        if not os.path.exists(caminho_absoluto):
            markdown.append(f"> Pasta `{pasta}/` não encontrada.\n")
            continue
        for raiz, _, arquivos in os.walk(caminho_absoluto):
            for arquivo in arquivos:
                extensao = os.path.splitext(arquivo)[1]
                if extensao in EXTENSOES_DOCUMENTADAS:
                    caminho_arquivo = os.path.join(raiz, arquivo)
                    markdown.append(ler_arquivo_comentado(caminho_arquivo))

    markdown.append("\n---\n")
    markdown.append("### 📌 Notas Finais\n")
    markdown.append("- Esta documentação foi gerada automaticamente.\n")
    markdown.append("- Modifique `gerar_documentacao.py` para personalizar a extração ou filtros.\n")

    os.makedirs("documentacao", exist_ok=True)
    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown))
    print(f"✅ Documentação gerada em: {CAMINHO_SAIDA}")

if __name__ == "__main__":
    gerar_documentacao()
