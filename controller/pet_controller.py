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
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    cursor.close()
    conn.close()
    return pets

def obter_pet_por_id(pet_id):
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
    pet = cursor.fetchone()
    cursor.close()
    conn.close()
    return pet

def salvar_pet(dados):
    conn = obter_conexao()
    cursor = conn.cursor()
    if dados.get("id"):
        cursor.execute("UPDATE pets SET apelido=%s, raca=%s, data_nascimento=%s, cpf=%s, foto=%s WHERE id=%s",
                       (dados["apelido"], dados["raca"], dados["data_nascimento"], dados["cpf"], dados["foto"], dados["id"]))
    else:
        cursor.execute("INSERT INTO pets (apelido, raca, data_nascimento, cpf, foto) VALUES (%s, %s, %s, %s, %s)",
                       (dados["apelido"], dados["raca"], dados["data_nascimento"], dados["cpf"], dados["foto"]))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_pet(pet_id):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
    conn.commit()
    cursor.close()
    conn.close()
