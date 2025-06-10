# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_sobre.py - Tela 'Sobre o Sistema'
# Descrição: Este script exibe informações gerais sobre o sistema de gerenciamento
#            de alunos, como versão, desenvolvedor e funcionalidades.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
#
# Uso: Execute a partir da janela principal no menu 'Sobre' para exibir esta tela.
# ==============================================================================

# view/form_sobre.py
# Tela de informações "Sobre o Sistema"

import customtkinter as ctk

class FormSobre(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sobre o Sistema")
        self.geometry("500x400")

        ctk.CTkLabel(self, text="Sistema de Gerenciamento de Alunos", font=("Arial", 18)).pack(pady=20)
        ctk.CTkLabel(self, text="""Desenvolvido para facilitar o controle de alunos.
                                 Interface moderna em CustomTkinter.
                                 Conexão com banco de dados MySQL.
                                 CRUD completo, gráficos e relatórios.""" ,
                                 font=("Arial", 12)).pack(pady=10)

        ctk.CTkButton(self, text="Fechar", command=self.destroy).pack(pady=20)

        # Centraliza a janela
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        w = 500
        h = 400
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")