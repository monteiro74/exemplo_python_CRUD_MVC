# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: user_controller.py - Operações de autenticação de usuários
# Descrição: Este script fornece funções para autenticar, criar e verificar
#            usuários no banco de dados, utilizando hash SHA-256 para senhas.
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - model.conexao_db: Para obter a conexão com o banco de dados.
# - hashlib: Para geração de hash SHA-256 das senhas.
# - logger: Para registro de eventos do sistema.
#
# Uso: Este módulo deve ser importado pelos componentes da camada de view e
#      controller para manipulação de autenticação de usuários.
# ==============================================================================

# controller/user_controller.py
# Operações de autenticação de usuários

import hashlib
from model.conexao_db import obter_conexao
from logger import log_event

def autenticar_usuario(login, senha):
    """
    Autentica um usuário verificando login e senha no banco de dados

    Args:
        login (str): Login do usuário
        senha (str): Senha em texto plano

    Returns:
        bool: True se autenticado, False caso contrário
    """
    log_event("user_controller", "autenticar_usuario")

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Hash da senha usando SHA-256
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        # Busca usuário com login e senha correspondentes
        sql = "SELECT login FROM users WHERE login = %s AND pswd = %s"
        cursor.execute(sql, (login, senha_hash))

        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        return resultado is not None

    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return False

def criar_usuario(login, senha):
    """
    Cria um novo usuário no sistema

    Args:
        login (str): Login do usuário
        senha (str): Senha em texto plano

    Returns:
        bool: True se criado com sucesso, False caso contrário
    """
    log_event("user_controller", "criar_usuario")

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Hash da senha usando SHA-256
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        # Insere novo usuário
        sql = "INSERT INTO users (login, pswd) VALUES (%s, %s)"
        cursor.execute(sql, (login, senha_hash))

        conexao.commit()
        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False

def verificar_usuario_existe(login):
    """
    Verifica se um usuário já existe no banco de dados

    Args:
        login (str): Login do usuário

    Returns:
        bool: True se existe, False caso contrário
    """
    log_event("user_controller", "verificar_usuario_existe")

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        sql = "SELECT login FROM users WHERE login = %s"
        cursor.execute(sql, (login,))

        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        return resultado is not None

    except Exception as e:
        print(f"Erro ao verificar usuário: {e}")
        return False
