# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: conexao_db.py - Gerenciamento de Conexão com o Banco de Dados
# Descrição: Este script lê as configurações de conexão em arquivo .con e
#            estabelece a conexão com o banco de dados MySQL.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - mysql-connector-python: Para conectar ao MySQL.
# - os: Para manipulação de caminhos de arquivos.
#
# Uso: Tenha o arquivo 'conexao.con' na mesma pasta deste script.
# ==============================================================================

# model/conexao_db.py
# Conexão com o MySQL lendo as configurações do arquivo conexao.con

# model/conexao_db.py
import mysql.connector
import os

def ler_conexao(arquivo='conexao.con'):
    """Lê as configurações de conexão a partir do arquivo .con dentro da mesma pasta."""
    # Descobre o diretório onde este script (conexao_db.py) está localizado
    pasta_atual = os.path.dirname(__file__)
    # Junta esse diretório com o nome do arquivo
    caminho_completo = os.path.join(pasta_atual, arquivo)

    config = {}
    with open(caminho_completo, 'r', encoding='utf-8') as f:
        for linha in f:
            if '=' in linha:
                chave, valor = linha.strip().strip(';').split('=')
                config[chave.strip()] = valor.strip().strip("'")
    return config

def obter_conexao():
    """Estabelece a conexão com o banco de dados usando as configurações lidas."""
    config = ler_conexao()  # por padrão, 'conexao.con'
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Erro de conexão: {e}")
        raise

