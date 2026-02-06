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
    """
    Retorna a lista de todos os alunos cadastrados no banco de dados.

    Realiza uma consulta SELECT na tabela 'alunos' retornando os campos:
    matricula, nome, cpf, curso, idade e sexo.

    Returns:
        list[dict]: Lista de dicionários, onde cada dicionário representa
                    um aluno com as chaves: matricula, nome, cpf, curso,
                    idade e sexo.
    """
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários
    cursor.execute("SELECT matricula, nome, cpf, curso, idade, sexo FROM alunos")
    alunos = cursor.fetchall()  # Obtém todos os registros de uma vez
    cursor.close()
    conn.close()
    return alunos


def obter_aluno_por_matricula(matricula):
    """
    Retorna os dados completos de um aluno específico pela matrícula.

    Realiza uma consulta SELECT * na tabela 'alunos' filtrando pelo
    campo matrícula. Utiliza query parametrizada para evitar SQL injection.

    Args:
        matricula (str): Número de matrícula do aluno a ser consultado.

    Returns:
        dict or None: Dicionário com todos os campos do aluno (incluindo
                      foto em LONGBLOB), ou None se não encontrado.
    """
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alunos WHERE matricula = %s", (matricula,))
    aluno = cursor.fetchone()  # Retorna apenas um registro ou None
    cursor.close()
    conn.close()
    return aluno


def salvar_aluno(dados):
    """
    Insere um novo aluno ou atualiza um aluno existente no banco de dados.

    Verifica se o dicionário 'dados' contém uma matrícula preenchida.
    Se sim, executa um UPDATE; caso contrário, executa um INSERT.
    Utiliza conn.commit() para confirmar a transação no banco.

    Args:
        dados (dict): Dicionário com os dados do aluno contendo as chaves:
                      - matricula (str): Número de matrícula.
                      - nome (str): Nome completo do aluno.
                      - curso (str): Nome do curso.
                      - idade (int): Idade do aluno.
                      - sexo (str): Sexo do aluno ('M' ou 'F').
                      - foto (bytes ou None): Imagem em formato binário (LONGBLOB).
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    if dados.get("matricula"):
        # Atualiza os dados de um aluno existente com base na matrícula
        cursor.execute("""
            UPDATE alunos SET nome=%s, curso=%s, idade=%s, sexo=%s, foto=%s WHERE matricula=%s
        """, (dados["nome"], dados["curso"], dados["idade"], dados["foto"], dados["sexo"], dados["matricula"]))
    else:
        # Insere um novo registro de aluno na tabela
        cursor.execute("""
            INSERT INTO alunos (matricula, nome, curso, idade, foto, sexo) VALUES (%s, %s, %s, %s, %s, %s)
        """, (dados["matricula"], dados["nome"], dados["curso"], dados["idade"], dados["foto"], dados["sexo"]))
    conn.commit()  # Confirma a transação no banco de dados
    cursor.close()
    conn.close()


def deletar_aluno(matricula):
    """
    Remove um aluno do banco de dados pela matrícula.

    Executa um DELETE na tabela 'alunos' filtrando pelo campo matrícula.
    A exclusão é confirmada com conn.commit().

    Args:
        matricula (str): Número de matrícula do aluno a ser removido.
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE matricula = %s", (matricula,))
    conn.commit()  # Confirma a exclusão no banco de dados
    cursor.close()
    conn.close()


def contar_alunos():
    """
    Conta o total de alunos cadastrados no banco de dados.

    Executa um SELECT COUNT(*) na tabela 'alunos' e retorna o valor
    inteiro do primeiro campo da primeira linha do resultado.

    Returns:
        int: Número total de alunos cadastrados.
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM alunos")
    total = cursor.fetchone()[0]  # Extrai o valor escalar do resultado
    cursor.close()
    conn.close()
    return total


def obter_idades_alunos():
    """
    Retorna uma lista com as idades de todos os alunos cadastrados.

    Utilizada para alimentar gráficos de distribuição etária.
    Executa um SELECT na coluna 'idade' e converte o resultado
    em uma lista simples de inteiros via list comprehension.

    Returns:
        list[int]: Lista contendo a idade de cada aluno cadastrado.
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT idade FROM alunos")
    idades = [row[0] for row in cursor.fetchall()]  # Extrai apenas o valor de cada tupla
    cursor.close()
    conn.close()
    return idades
