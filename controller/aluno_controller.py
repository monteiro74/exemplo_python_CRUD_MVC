# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: aluno_controller.py - Operações CRUD para Alunos
# Descrição: Este script fornece funções para criar, ler, atualizar e excluir
#            registros de alunos no banco de dados.
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - model.conexao_db: Para obter a conexão com o banco de dados.
#
# Uso: Este módulo deve ser importado pelos componentes da camada de view e
#      controller para manipulação de dados de alunos.
# ==============================================================================

# controller/aluno_controller.py
# Operações CRUD para Alunos

from model.conexao_db import obter_conexao


def obter_alunos():
    """Retorna a lista de alunos cadastrados."""
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT matricula, nome, cpf, curso, idade, sexo FROM alunos")
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()
    return alunos

def obter_aluno_por_matricula(matricula):
    """Retorna os dados de um aluno específico."""
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alunos WHERE matricula = %s", (matricula,))
    aluno = cursor.fetchone()
    cursor.close()
    conn.close()
    return aluno

def salvar_aluno(dados):
    """Insere ou atualiza um aluno no banco."""
    conn = obter_conexao()
    cursor = conn.cursor()
    if dados.get("matricula"):
        # Atualiza se a matrícula já existe
        cursor.execute("""
            UPDATE alunos SET nome=%s, curso=%s, idade=%s, sexo=%s, foto=%s WHERE matricula=%s
        """, (dados["nome"], dados["curso"], dados["idade"], dados["foto"], dados["sexo"], dados["matricula"]))
    else:
        # Insere um novo aluno
        cursor.execute("""
            INSERT INTO alunos (matricula, nome, curso, idade, foto, sexo) VALUES (%s, %s, %s, %s, %s, %s)
        """, (dados["matricula"], dados["nome"], dados["curso"], dados["idade"], dados["foto"], dados["sexo"]))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_aluno(matricula):
    """Remove um aluno do banco."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE matricula = %s", (matricula,))
    conn.commit()
    cursor.close()
    conn.close()

def contar_alunos():
    """Conta o total de alunos cadastrados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM alunos")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def obter_idades_alunos():
    """Retorna as idades dos alunos para análise de gráficos."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT idade FROM alunos")
    idades = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return idades
