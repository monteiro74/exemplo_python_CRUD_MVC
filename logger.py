# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: logger.py - Registro de Logs da Aplicação
# Descrição: Este script registra eventos de execução dos módulos do sistema em
#            um arquivo CSV localizado na pasta logs.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - os: Para manipulação de diretórios e arquivos.
# - datetime: Para registrar data e hora dos eventos.
# - tkinter.messagebox: Para exibir mensagens pop-up em caso de falha no log.
#
# Uso: Importe a função log_event em outros módulos e chame log_event(app_name, method_name)
# ==============================================================================

import os
import datetime

# O bloco abaixo tenta importar o messagebox do Tkinter, que serve para exibir alertas modais (pop-ups)
try:
    from tkinter import messagebox
except ImportError:
    # Caso a biblioteca Tkinter não esteja disponível (rodando em ambiente sem interface gráfica), define um alerta "mudo"
    def messagebox(*args, **kwargs):
        pass

# Define o caminho para o arquivo de logs, dentro da pasta 'logs' do projeto
LOG_FILE = os.path.join(os.getcwd(), "logs", "logs.csv")

def log_event(app_name, method_name):
    """
    Esta função registra uma linha no arquivo de log sempre que é chamada.
    Ela salva a data, hora, nome da aplicação e o método/ação registrada.
    Tudo é separado por ponto e vírgula.
    Se não conseguir gravar o log, exibe um alerta modal informando o erro.

    Parâmetros:
    app_name (str): nome do módulo ou funcionalidade
    method_name (str): nome do método, função ou ação executada
    """
    # Obtém data e hora atuais para gravar no log
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    line = f"{date};{time};{app_name};{method_name}\n"
    try:
        # Garante que a pasta do log exista, cria se não existir
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        # Abre o arquivo de log no modo 'append' (acrescenta linhas)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        # Em caso de erro na gravação do log, exibe alerta modal ao usuário (se possível)
        try:
            messagebox.showerror(
                "Erro ao registrar log",
                f"Não foi possível registrar o evento no arquivo de log:\n{e}"
            )
        except Exception:
            pass  # Ignora erro caso não tenha interface gráfica
    finally:
        # Este bloco sempre será executado, mesmo em caso de erro.
        # Pode ser usado para registrar em outro local, se necessário (exemplo: impressora, arquivo alternativo etc.)
        pass  # Neste exemplo, apenas deixamos o finally explícito para fins didáticos.

