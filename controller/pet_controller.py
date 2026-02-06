# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: pet_controller.py - Operações CRUD para Pets
# Descrição: Este script fornece funções para criar, ler, atualizar e excluir
#            registros de pets no banco de dados.
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - model.conexao_db: Para obter a conexão com o banco de dados.
#
# Uso: Este módulo deve ser importado pelos componentes da camada de view e
#      controller para manipulação de dados de pets.
# ==============================================================================

# controller/pet_controller.py
# Operações CRUD para Pets

from model.conexao_db import obter_conexao


def obter_pets():
    """
    Retorna a lista de todos os pets cadastrados no banco de dados.

    Realiza uma consulta SELECT * na tabela 'pets', retornando todos
    os campos de cada registro.

    Returns:
        list[dict]: Lista de dicionários, onde cada dicionário representa
                    um pet com as chaves: Id, apelido, raca, data_nascimento,
                    foto e cpf (do dono).
    """
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()  # Obtém todos os registros de uma vez
    cursor.close()
    conn.close()
    return pets


def obter_pet_por_id(pet_id):
    """
    Retorna os dados completos de um pet específico pelo ID.

    Realiza uma consulta SELECT * na tabela 'pets' filtrando pelo
    campo id. Utiliza query parametrizada para evitar SQL injection.

    Args:
        pet_id (int): Identificador único do pet a ser consultado.

    Returns:
        dict or None: Dicionário com todos os campos do pet (incluindo
                      foto em LONGBLOB), ou None se não encontrado.
    """
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
    pet = cursor.fetchone()  # Retorna apenas um registro ou None
    cursor.close()
    conn.close()
    return pet


def salvar_pet(dados):
    """
    Insere um novo pet ou atualiza um pet existente no banco de dados.

    Verifica se o dicionário 'dados' contém um ID preenchido.
    Se sim, executa um UPDATE; caso contrário, executa um INSERT.
    Utiliza conn.commit() para confirmar a transação no banco.

    Args:
        dados (dict): Dicionário com os dados do pet contendo as chaves:
                      - id (int ou None): Identificador do pet (None para inserção).
                      - apelido (str): Nome/apelido do pet.
                      - raca (str): Raça do pet.
                      - data_nascimento (date): Data de nascimento do pet.
                      - cpf (str): CPF do dono (FK para tabela alunos).
                      - foto (bytes ou None): Imagem em formato binário (LONGBLOB).
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    if dados.get("id"):
        # Atualiza os dados de um pet existente com base no ID
        cursor.execute("UPDATE pets SET apelido=%s, raca=%s, data_nascimento=%s, cpf=%s, foto=%s WHERE id=%s",
                       (dados["apelido"], dados["raca"], dados["data_nascimento"], dados["cpf"], dados["foto"], dados["id"]))
    else:
        # Insere um novo registro de pet na tabela
        cursor.execute("INSERT INTO pets (apelido, raca, data_nascimento, cpf, foto) VALUES (%s, %s, %s, %s, %s)",
                       (dados["apelido"], dados["raca"], dados["data_nascimento"], dados["cpf"], dados["foto"]))
    conn.commit()  # Confirma a transação no banco de dados
    cursor.close()
    conn.close()


def deletar_pet(pet_id):
    """
    Remove um pet do banco de dados pelo ID.

    Executa um DELETE na tabela 'pets' filtrando pelo campo id.
    A exclusão é confirmada com conn.commit().

    Args:
        pet_id (int): Identificador único do pet a ser removido.
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
    conn.commit()  # Confirma a exclusão no banco de dados
    cursor.close()
    conn.close()
