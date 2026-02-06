# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_report_alunos.py - Gerador de Relatório de Alunos em PDF
# Descrição: Este script permite gerar um relatório em PDF com a lista de alunos
#            cadastrados, salvando-o no disco.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - fpdf: Para geração de arquivos PDF.
# - controller.aluno_controller: Para obter dados de alunos.
#
# Uso: Execute a partir da janela principal no menu 'Relatórios' para gerar o PDF.
# ==============================================================================

# view/form_report_alunos.py
# Geração de relatório em PDF com a lista de alunos

import customtkinter as ctk
from fpdf import FPDF
from tkinter import messagebox
from controller.aluno_controller import obter_alunos

class FormReportAlunos(ctk.CTkToplevel):
    """
    Janela modal para geração de relatório de alunos em formato PDF.

    Exibe um botão para gerar o PDF e outro para fechar. O relatório
    é criado com fpdf2 e salvo como 'relatorio_alunos.pdf' na raiz do projeto.

    Parâmetros:
        master: Janela principal que chama este formulário.
    """

    def __init__(self, master=None):
        """
        Inicializa a janela de relatório com título, botão de geração
        de PDF e botão de fechar.
        """
        super().__init__(master)
        self.title("Relatório de Alunos")
        self.geometry("400x200")

        # Título e botões de ação
        ctk.CTkLabel(self, text="Gerar Relatório de Alunos", font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(self, text="Gerar PDF", command=self.gerar_pdf).pack(pady=10)
        ctk.CTkButton(self, text="Fechar", command=self.destroy).pack(pady=10)

        # Centraliza a janela na tela
        self._center_window()

    def _center_window(self):
        """
        Centraliza a janela no centro da tela do usuário.
        """
        self.update_idletasks()
        w = 400
        h = 200
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def gerar_pdf(self):
        """
        Gera o relatório de alunos em formato PDF usando a biblioteca fpdf2.

        Consulta todos os alunos via controller, monta uma tabela com
        colunas (Matrícula, Nome, Curso, Idade, Sexo) e salva o arquivo
        'relatorio_alunos.pdf' na raiz do projeto. Exibe mensagem de
        sucesso ou informação caso não haja alunos cadastrados.
        """
        # Consulta todos os alunos via controller
        alunos = obter_alunos()
        if not alunos:
            messagebox.showinfo("Informação", "Não há alunos cadastrados para gerar o relatório.")
            return

        # Inicializa o documento PDF com fpdf2
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório de Alunos", ln=True, align="C")
        pdf.ln(10)

        # Cabeçalhos da tabela com bordas
        pdf.cell(40, 10, "Matrícula", border=1)
        pdf.cell(60, 10, "Nome", border=1)
        pdf.cell(40, 10, "Curso", border=1)
        pdf.cell(20, 10, "Idade", border=1)
        pdf.cell(20, 10, "Sexo", border=1)
        pdf.ln()

        # Itera sobre os alunos e preenche as linhas da tabela
        for aluno in alunos:
            pdf.cell(40, 10, aluno["matricula"], border=1)
            pdf.cell(60, 10, aluno["nome"], border=1)
            pdf.cell(40, 10, aluno["curso"], border=1)
            pdf.cell(20, 10, str(aluno["idade"]), border=1)
            pdf.cell(20, 10, aluno.get("sexo", ""), border=1)
            pdf.ln()

        # Salva o arquivo PDF na raiz do projeto
        pdf.output("relatorio_alunos.pdf")
        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")