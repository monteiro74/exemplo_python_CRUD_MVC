# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_mestre_detalhe.py - Formulário Mestre-Detalhe (Aluno/Pets)
# Descrição: Este script exibe um formulário de navegação mestre-detalhe,
#            mostrando os dados do aluno (mestre) e seus pets associados (detalhe).
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - tkinter.ttk: Para widget Treeview na tabela de pets.
# - controller.aluno_controller: Para obter a lista de alunos.
# - controller.pet_controller: Para obter a lista de pets.
#
# Uso: Execute a partir da janela principal no menu 'Arquivo' > 'Mestre-Detalhe'.
# ==============================================================================

# view/form_mestre_detalhe.py
# Formulário modal com padrão mestre-detalhe (Aluno → Pets)

import customtkinter as ctk
from tkinter import messagebox
from controller.aluno_controller import obter_alunos
from controller.pet_controller import obter_pets
from tkinter import ttk


class FormMestreDetalhe(ctk.CTkToplevel):
    """
    Janela modal que implementa o padrão mestre-detalhe.

    A seção mestre exibe os dados do aluno (nome, curso, CPF) em campos
    somente leitura, com botões de navegação (Anterior/Próximo).
    A seção detalhe exibe uma Treeview com os pets associados ao aluno
    atual, filtrados pelo CPF do dono.

    Parâmetros:
        master: Janela principal que chama este formulário.
    """

    def __init__(self, master=None):
        """
        Inicializa o formulário mestre-detalhe, carrega a lista de alunos,
        monta os campos de exibição, botões de navegação e a tabela de pets.
        """
        super().__init__(master)
        self.title("Aluno e seus Pets")
        self.geometry("800x500")
        self.alunos = obter_alunos()  # Carrega todos os alunos do banco
        self.indice = 0  # Índice do aluno atualmente exibido

        # ─── Seção Mestre: Campos do aluno (somente leitura) ─────────────
        ctk.CTkLabel(self, text="Nome:").pack(pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(self, state="disabled")
        self.entry_nome.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Curso:").pack(pady=(10, 0))
        self.entry_curso = ctk.CTkEntry(self, state="disabled")
        self.entry_curso.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="CPF:").pack(pady=(10, 0))
        self.entry_cpf = ctk.CTkEntry(self, state="disabled")
        self.entry_cpf.pack(fill="x", padx=20)

        # ─── Botões de navegação entre alunos ────────────────────────────
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(pady=10)
        ctk.CTkButton(nav_frame, text="<< Anterior", command=self.anterior).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Próximo >>", command=self.proximo).pack(side="left", padx=10)

        # ─── Seção Detalhe: Tabela de Pets do aluno ─────────────────────
        ctk.CTkLabel(self, text="Pets do aluno:").pack(pady=(20, 0))
        self.tree_pets = ttk.Treeview(self, columns=("id", "apelido", "raca", "data_nascimento"), show="headings")
        for col in self.tree_pets["columns"]:
            self.tree_pets.heading(col, text=col.capitalize())
        self.tree_pets.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        self._center_window()
        self.mostrar_aluno()  # Exibe o primeiro aluno da lista

    def _center_window(self):
        """
        Centraliza a janela no centro da tela do usuário.
        """
        self.update_idletasks()
        w = 800
        h = 500
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def mostrar_aluno(self):
        """
        Exibe os dados do aluno na posição atual do índice de navegação.

        Preenche os campos nome, curso e CPF (habilitando temporariamente
        para escrita) e atualiza a tabela de pets do aluno.
        """
        if not self.alunos:
            return
        aluno = self.alunos[self.indice]

        # Atualiza campo nome (habilita → insere → desabilita)
        self.entry_nome.configure(state="normal")
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, aluno["nome"])
        self.entry_nome.configure(state="disabled")

        # Atualiza campo curso
        self.entry_curso.configure(state="normal")
        self.entry_curso.delete(0, "end")
        self.entry_curso.insert(0, aluno["curso"])
        self.entry_curso.configure(state="disabled")

        # Atualiza campo CPF
        self.entry_cpf.configure(state="normal")
        self.entry_cpf.delete(0, "end")
        self.entry_cpf.insert(0, aluno["cpf"])
        self.entry_cpf.configure(state="disabled")

        # Atualiza a tabela de pets filtrada pelo CPF do aluno
        self.mostrar_pets(aluno["cpf"])

    def mostrar_pets(self, cpf):
        """
        Filtra e exibe na Treeview apenas os pets cujo CPF do dono
        corresponde ao CPF do aluno atualmente selecionado.

        Args:
            cpf (str): CPF do aluno para filtrar os pets associados.
        """
        self.tree_pets.delete(*self.tree_pets.get_children())  # Limpa a tabela
        for pet in obter_pets():
            # Compara como string para garantir compatibilidade de tipos
            if str(pet["cpf"]) == str(cpf):
                self.tree_pets.insert("", "end", values=(pet["Id"], pet["apelido"], pet["raca"], pet["data_nascimento"]))

    def proximo(self):
        """
        Avança para o próximo aluno na lista, se não estiver no último.
        Atualiza a exibição do mestre e detalhe.
        """
        if self.indice < len(self.alunos) - 1:
            self.indice += 1
            self.mostrar_aluno()

    def anterior(self):
        """
        Retorna ao aluno anterior na lista, se não estiver no primeiro.
        Atualiza a exibição do mestre e detalhe.
        """
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_aluno()
