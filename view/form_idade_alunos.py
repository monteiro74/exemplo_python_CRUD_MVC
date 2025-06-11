# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_idade_alunos.py - Gráfico de Idade dos Alunos
# Descrição: Este script gera um gráfico de barras mostrando a distribuição
#            de idades dos alunos cadastrados no banco de dados.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - matplotlib: Para geração de gráficos.
# - controller.aluno_controller: Para obter dados de idades dos alunos.
#
# Uso: Execute a partir da janela principal para visualizar o gráfico de idades.
# ==============================================================================

# view/form_idade_alunos.py
# Gráfico de Idade dos Alunos

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from controller.aluno_controller import obter_idades_alunos

class FormIdadeAlunos(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gráfico de Idades dos Alunos")
        self.geometry("600x400")

        # Busca os dados
        idades = obter_idades_alunos()
        faixas = ["18-25", "26-30", "31-40", "41-50", "51+"]
        qtd_idades = [0, 0, 0, 0, 0]
        for idade in idades:
            if idade is None:
                continue
            if 18 <= idade <= 25:
                qtd_idades[0] += 1
            elif 26 <= idade <= 30:
                qtd_idades[1] += 1
            elif 31 <= idade <= 40:
                qtd_idades[2] += 1
            elif 41 <= idade <= 50:
                qtd_idades[3] += 1
            else:
                qtd_idades[4] += 1
        fig, ax = plt.subplots()
        ax.bar(faixas, qtd_idades)
        ax.set_title("Distribuição de Idade dos Alunos")
        ax.set_xlabel("Faixa Etária")
        ax.set_ylabel("Quantidade")

        # Inserir no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

        # Centraliza a janela
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        w = 600
        h = 400
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")