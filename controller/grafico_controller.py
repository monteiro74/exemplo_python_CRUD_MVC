# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: grafico_controller.py - Controlador para gráficos de idade e quantidade de alunos
# Descrição: Este script agrupa e conta alunos por faixa etária para geração
#            de gráficos estatísticos, bem como conta o total de alunos.
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - model.conexao_db: Para obter a conexão com o banco de dados.
#
# Uso: Este módulo deve ser importado pela camada de view para renderizar gráficos
#      baseados em dados de alunos.
# ==============================================================================

# controller/grafico_controller.py
# Controlador para gráficos de idade e quantidade de alunos

from model.conexao_db import obter_conexao


def contar_alunos_por_faixa_etaria():
    """Conta alunos agrupados por faixa etária."""
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT 
        CASE
            WHEN idade BETWEEN 18 AND 25 THEN '18-25'
            WHEN idade BETWEEN 26 AND 30 THEN '26-30'
            WHEN idade BETWEEN 31 AND 40 THEN '31-40'
            WHEN idade BETWEEN 41 AND 50 THEN '41-50'
            ELSE '51+'
        END AS faixa_etaria,
        COUNT(*) AS quantidade
    FROM alunos
    GROUP BY faixa_etaria
    """
    cursor.execute(query)
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def contar_total_alunos():
    """Conta o total de alunos cadastrados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM alunos")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total
