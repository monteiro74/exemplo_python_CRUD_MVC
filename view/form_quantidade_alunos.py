# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_quantidade_alunos.py - Gráfico de Quantidade de Alunos
# Descrição: Este script gera um gráfico de barras mostrando o número total de
#            alunos cadastrados no banco de dados.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - matplotlib: Para geração de gráficos.
# - controller.aluno_controller: Para obter contagem de alunos.
#
# Uso: Execute a partir da janela principal para visualizar o gráfico de quantidade.
# ==============================================================================

# view/form_quantidade_alunos.py
# Gráfico de Quantidade de Alunos

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from controller.aluno_controller import contar_alunos

class FormQuantidadeAlunos(ctk.CTkToplevel):
    """
    Janela modal que exibe um gráfico de barras com o número total
    de alunos cadastrados no banco de dados.

    Utiliza matplotlib integrado ao CustomTkinter via FigureCanvasTkAgg.

    Parâmetros:
        master: Janela principal que chama este formulário.
    """

    def __init__(self, master=None):
        """
        Inicializa o formulário de gráfico de quantidade, consulta o
        total de alunos via controller e renderiza o gráfico de barras.
        """
        super().__init__(master)
        self.title("Gráfico de Quantidade de Alunos")
        self.geometry("500x400")

        # Consulta a contagem total de alunos via controller
        total_alunos = contar_alunos()

        # Cria o gráfico de barras com matplotlib
        fig, ax = plt.subplots()
        ax.bar(["Alunos"], [total_alunos])
        ax.set_title("Quantidade Total de Alunos")
        ax.set_ylabel("Total")

        # Integra o gráfico matplotlib na janela CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

        # Centraliza a janela na tela
        self._center_window()

    def _center_window(self):
        """
        Centraliza a janela no centro da tela do usuário.
        """
        self.update_idletasks()
        w = 500
        h = 400
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")