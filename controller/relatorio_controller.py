# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: relatorio_controller.py - Controlador para geração de relatórios PDF
# Descrição: Este script coleta dados de alunos do banco de dados para gerações
#            de relatórios em formato PDF.
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - model.conexao_db: Para obter a conexão com o banco de dados.
#
# Uso: Este módulo deve ser importado pela camada de view para gerar relatórios PDF.
# ==============================================================================

# controller/relatorio_controller.py
# Controlador para geração de relatórios PDF

from model.conexao_db import obter_conexao


def obter_dados_relatorio():
    """
    Coleta os dados de alunos para geração de relatório em PDF.

    Realiza uma consulta SELECT na tabela 'alunos' retornando os campos
    necessários para o relatório: matricula, nome, curso, idade e sexo.
    O campo foto (LONGBLOB) não é incluído para otimizar a consulta.

    Returns:
        list[dict]: Lista de dicionários, onde cada dicionário representa
                    um aluno com as chaves: matricula, nome, curso, idade
                    e sexo.
    """
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários
    cursor.execute("SELECT matricula, nome, curso, idade, sexo FROM alunos")
    alunos = cursor.fetchall()  # Obtém todos os registros para o relatório
    cursor.close()
    conn.close()
    return alunos
