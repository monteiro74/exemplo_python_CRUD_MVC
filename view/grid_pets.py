# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: grid_pets.py - Grade de Pets
# Descrição: Este script exibe uma grade (Treeview) listando todos os pets
#            e fornece botões para adicionar, editar, excluir ou fechar.
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - tkinter.ttk: Para widget Treeview.
# - controller.pet_controller: Para operações de banco de dados de pets.
# - view.form_pets: Para abrir o formulário de cadastro/edição.
# - logger: Para registro de logs de eventos.
#
# Uso: Execute a partir da janela principal no menu 'Arquivo' para visualizar a grade.
# ==============================================================================

# view/grid_pets.py
# Grid de pets com listagem, botões de CRUD e logging

import customtkinter as ctk
from tkinter import ttk, messagebox
from controller.pet_controller import obter_pets, deletar_pet
from view.form_pets import FormPets
from logger import log_event


class GridPets(ctk.CTkToplevel):
    """
    Janela modal que exibe uma grade (Treeview) com todos os pets cadastrados.

    Fornece botões para adicionar, editar e excluir registros, além de
    suporte a duplo-clique para edição. A lista é atualizada automaticamente
    após cada operação CRUD via callback.

    Parâmetros:
        master: Janela principal que chama esta grade.
    """

    def __init__(self, master=None):
        """
        Inicializa a grade de pets, configura a Treeview com as colunas
        (id, apelido, raca, data_nascimento, cpf), botões de ação e
        carrega a lista de pets do banco de dados.
        """
        super().__init__(master)
        log_event("grid_pets", "__init__")
        self.title("Lista de Pets")
        self.geometry("800x400")

        # Título da grade
        ctk.CTkLabel(self, text="Pets Cadastrados", font=("Arial", 16)).pack(pady=10)

        # ─── Treeview com colunas de dados dos pets ──────────────────────
        self.tree = ttk.Treeview(self, columns=("id", "apelido", "raca", "data_nascimento", "cpf"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
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
        Recarrega a lista de pets do banco de dados e atualiza a Treeview.
        Limpa todos os itens existentes antes de inserir os novos.
        """
        for i in self.tree.get_children():
            self.tree.delete(i)  # Limpa a tabela
        for pet in obter_pets():
            self.tree.insert("", "end", values=(pet["Id"], pet["apelido"], pet["raca"], pet["data_nascimento"], pet["cpf"]))

    def adicionar(self):
        """
        Abre o formulário de cadastro de um novo pet (FormPets),
        passando o callback de atualização da lista.
        """
        FormPets(self, atualizar_callback=self.atualizar_lista)

    def editar_selecionado(self, event=None):
        """
        Abre o formulário de edição do pet selecionado na Treeview.
        Exibe aviso se nenhum item estiver selecionado.

        Args:
            event: Evento de duplo-clique (opcional, None se via botão).
        """
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione um pet.")
            return
        pet_id = self.tree.item(item)["values"][0]  # Obtém o ID da primeira coluna
        FormPets(self, pet_id=pet_id, atualizar_callback=self.atualizar_lista)

    def excluir(self):
        """
        Exclui o pet selecionado na Treeview após confirmação do usuário.
        Exibe aviso se nenhum item estiver selecionado.
        """
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione um pet.")
            return
        pet_id = self.tree.item(item)["values"][0]  # Obtém o ID da primeira coluna
        if messagebox.askyesno("Confirmação", "Deseja excluir este pet?"):
            deletar_pet(pet_id)
            self.atualizar_lista()  # Recarrega a lista após exclusão
