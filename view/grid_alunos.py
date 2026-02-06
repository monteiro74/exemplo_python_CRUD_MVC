# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: grid_alunos.py - Grade de Alunos
# Descrição: Este script exibe uma grade (Treeview) listando todos os alunos
#            e fornece botões para adicionar, editar, excluir ou fechar.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - tkinter.ttk: Para widget Treeview.
# - controller.aluno_controller: Para operações de banco de dados de alunos.
# - view.form_alunos: Para abrir o formulário de cadastro/edição.
# - logger: Para registro de logs de eventos.
#
# Uso: Execute a partir da janela principal no menu 'Arquivo' para visualizar a grade.
# ==============================================================================

# view/grid_alunos.py
# Grid de alunos com listagem, botões de CRUD e logging

import os, sys
# Garante que a raiz do projeto (pasta exemplo2/) esteja no sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import customtkinter as ctk
from tkinter import ttk, messagebox
from controller.aluno_controller import obter_alunos, deletar_aluno
from view.form_alunos import FormAlunos
from logger import log_event

class GridAlunos(ctk.CTkToplevel):
    """
    Janela modal que exibe uma grade (Treeview) com todos os alunos cadastrados.

    Fornece botões para adicionar, editar e excluir registros, além de
    suporte a duplo-clique para edição. A lista é atualizada automaticamente
    após cada operação CRUD via callback.

    Parâmetros:
        master: Janela principal que chama esta grade.
    """

    def __init__(self, master=None):
        """
        Inicializa a grade de alunos, configura a Treeview com as colunas
        (matrícula, nome, curso, idade, sexo), botões de ação e
        carrega a lista de alunos do banco de dados.
        """
        super().__init__(master)
        log_event("grid_alunos", "__init__")
        self.title("Lista de Alunos")
        self.geometry("800x400")

        # Título da grade
        ctk.CTkLabel(self, text="Alunos Cadastrados", font=("Arial", 16)).pack(pady=10)

        # ─── Treeview com colunas de dados dos alunos ────────────────────
        self.tree = ttk.Treeview(
            self,
            columns=("matricula", "nome", "curso", "idade", "sexo"),
            show="headings"
        )
        self.tree.heading("matricula", text="Matrícula")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("curso", text="Curso")
        self.tree.heading("idade", text="Idade")
        self.tree.heading("sexo", text="Sexo")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.editar_selecionado)  # Duplo-clique abre edição

        # ─── Botões de ação ──────────────────────────────────────────────
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)

        ctk.CTkButton(frame, text="Adicionar", command=self.adicionar).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Editar", command=self.editar_selecionado).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Excluir", command=self.excluir).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Fechar", command=self.destroy).pack(side="left", padx=5)

        self.atualizar_lista()  # Carrega os dados iniciais

        # Centraliza a janela na tela
        self._center_window()

    def _center_window(self):
        """
        Centraliza a janela no centro da tela do usuário.
        """
        self.update_idletasks()
        w = 800
        h = 400
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def atualizar_lista(self):
        """
        Recarrega a lista de alunos do banco de dados e atualiza a Treeview.
        Limpa todos os itens existentes antes de inserir os novos.
        """
        log_event("grid_alunos", "atualizar_lista")
        for i in self.tree.get_children():
            self.tree.delete(i)  # Limpa a tabela
        for aluno in obter_alunos():
            self.tree.insert(
                "",
                "end",
                values=(
                    aluno["matricula"],
                    aluno["nome"],
                    aluno["curso"],
                    aluno["idade"], aluno.get("sexo", "")
                )
            )

    def adicionar(self):
        """
        Abre o formulário de cadastro de um novo aluno (FormAlunos),
        passando o callback de atualização da lista.
        """
        log_event("grid_alunos", "adicionar")
        FormAlunos(self, atualizar_callback=self.atualizar_lista)

    def editar_selecionado(self, event=None):
        """
        Abre o formulário de edição do aluno selecionado na Treeview.
        Exibe aviso se nenhum item estiver selecionado.

        Args:
            event: Evento de duplo-clique (opcional, None se via botão).
        """
        log_event("grid_alunos", "editar_selecionado")
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione um aluno.")
            return
        matricula = self.tree.item(item)["values"][0]  # Obtém a matrícula da primeira coluna
        FormAlunos(self, matricula=matricula, atualizar_callback=self.atualizar_lista)

    def excluir(self):
        """
        Exclui o aluno selecionado na Treeview após confirmação do usuário.
        Exibe aviso se nenhum item estiver selecionado.
        """
        log_event("grid_alunos", "excluir")
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione um aluno.")
            return
        matricula = self.tree.item(item)["values"][0]  # Obtém a matrícula da primeira coluna
        if messagebox.askyesno("Confirmação", f"Deseja excluir o aluno {matricula}?"):
            deletar_aluno(matricula)
            self.atualizar_lista()  # Recarrega a lista após exclusão
