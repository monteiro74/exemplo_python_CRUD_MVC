# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_licenca.py - Tela de informações da licença
# Descrição: Este script exibe informações sobre a licença de uso do software,
#            incluindo termos e direitos de uso.
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

# view/form_licenca.py
# Tela de informações sobre a Licença de Uso

import customtkinter as ctk

class FormLicenca(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Licença de Uso")
        self.geometry("500x400")

        ctk.CTkLabel(self, text="""Este software é de uso acadêmico e educacional.
                     O código é aberto para estudos e melhorias.
                     Proibida a distribuição comercial sem autorização.
                     © 2025 - Sistema de Gerenciamento de Alunos""" ,
                     font=("Arial", 12)).pack(pady=10)
        ctk.CTkLabel(self, text="""Este é um software de exemplo para demonstração de tela de licença.""", font=("Arial", 12)).pack(pady=10)
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