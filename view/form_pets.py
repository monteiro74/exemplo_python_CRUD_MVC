# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_pets.py - Formulário de cadastro e edição de pets
# Descrição: Este script exibe um formulário modal para operações CRUD de pets,
#            incluindo seleção e exibição de foto e vínculo com o dono (CPF).
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - PIL: Para manipulação e redimensionamento de imagens.
# - controller.pet_controller: Para operações de banco de dados de pets.
# - logger: Para registro de eventos do sistema.
#
# Uso: Abra a grade de pets e clique em 'Adicionar' ou 'Editar' para usar este formulário.
# ==============================================================================

# view/form_pets.py
# Formulário modal para operações CRUD de pets com exibição de foto e logging

import os, sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import customtkinter as ctk
from tkinter import filedialog, messagebox
from controller.pet_controller import salvar_pet, obter_pet_por_id, deletar_pet
from PIL import Image, ImageTk
from io import BytesIO
from logger import log_event


class FormPets(ctk.CTkToplevel):
    """
    Janela modal para cadastro, edição e exclusão de pets.

    Permite inserir, atualizar e excluir registros de pets,
    além de selecionar e exibir foto do pet. Vincula o pet ao
    dono através do campo CPF (FK para tabela alunos).

    Parâmetros:
        master: Janela principal que chama este formulário.
        pet_id: ID do pet para edição (opcional, None para novo cadastro).
        atualizar_callback: Função callback para atualizar a lista após salvar/editar.
    """

    def __init__(self, master=None, pet_id=None, atualizar_callback=None):
        """
        Inicializa o formulário de pet, montando todos os campos de entrada,
        botões de ação e carregando dados se for edição.
        """
        super().__init__(master)
        log_event("form_pets", "__init__")
        self.title("Cadastro de Pet")
        self.geometry("600x700")
        self.resizable(False, False)
        self.pet_id = pet_id
        self.atualizar_callback = atualizar_callback
        self.foto_bytes = None  # Armazena a foto em bytes para gravação no banco
        self._photo_image = None  # Referência para ImageTk (evita garbage collection)

        # Torna este form modal (bloqueia interação com a janela pai)
        self.transient(master)
        self.grab_set()

        # ─── Campos de entrada ─────────────────────────────────────────────────
        ctk.CTkLabel(self, text="Apelido:", anchor="w").pack(fill="x", padx=20, pady=(20, 0))
        self.entry_apelido = ctk.CTkEntry(self)
        self.entry_apelido.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self, text="Raça:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.entry_raca = ctk.CTkEntry(self)
        self.entry_raca.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self, text="Data de Nascimento (YYYY-MM-DD):", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.entry_nascimento = ctk.CTkEntry(self)
        self.entry_nascimento.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self, text="CPF do dono:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.entry_cpf = ctk.CTkEntry(self)
        self.entry_cpf.pack(fill="x", padx=20, pady=(0, 10))

        # ─── Exibição de Foto ──────────────────────────────────────────────────
        ctk.CTkLabel(self, text="Foto:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.photo_label = ctk.CTkLabel(self, text="Sem foto", width=120, height=160)
        self.photo_label.pack(padx=20, pady=(0, 10))
        self.botao_foto = ctk.CTkButton(self, text="Selecionar Foto", command=self.selecionar_foto)
        self.botao_foto.pack(pady=(0, 20))

        # ─── Botões de ação ───────────────────────────────────────────────────
        botoes_frame = ctk.CTkFrame(self)
        botoes_frame.pack(pady=(0, 10))

        self.botao_salvar = ctk.CTkButton(botoes_frame, text="Salvar", command=self.salvar)
        self.botao_salvar.grid(row=0, column=0, padx=5)
        self.botao_excluir = ctk.CTkButton(botoes_frame, text="Excluir", fg_color="red", command=self.excluir)
        self.botao_excluir.grid(row=0, column=1, padx=5)
        self.botao_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", command=self.destroy)
        self.botao_cancelar.grid(row=0, column=2, padx=5)

        # Se for edição (já recebeu pet_id), carrega dados do banco
        if self.pet_id:
            self.carregar_dados()
        else:
            # Novo cadastro: desabilita botão Excluir
            self.botao_excluir.configure(state="disabled")

        # Centraliza a janela na tela
        self._center_window()

    def _center_window(self):
        """
        Centraliza a janela no centro da tela do usuário.
        """
        self.update_idletasks()
        w = 600
        h = 700
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def selecionar_foto(self):
        """
        Permite ao usuário selecionar uma foto do pet via diálogo de arquivo.
        Redimensiona a imagem para 120x160, exibe no label e armazena os
        bytes originais em self.foto_bytes para gravação no banco (LONGBLOB).
        """
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")], title="Selecionar Foto")
        if not caminho:
            return
        try:
            img = Image.open(caminho)
            img = img.resize((120, 160), Image.LANCZOS)  # Redimensiona com filtro de alta qualidade
            self._photo_image = ImageTk.PhotoImage(img)
            self.photo_label.configure(image=self._photo_image, text="")
            # Lê o arquivo original em bytes para armazenar no banco
            with open(caminho, "rb") as f:
                self.foto_bytes = f.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem: {e}")

    def carregar_dados(self):
        """
        Carrega os dados do pet selecionado para edição, preenchendo
        os campos do formulário. Também carrega a foto do pet, se existir.
        """
        pet = obter_pet_por_id(self.pet_id)
        if not pet:
            return
        self.entry_apelido.insert(0, pet["apelido"])
        self.entry_raca.insert(0, pet["raca"])
        self.entry_nascimento.insert(0, pet["data_nascimento"])
        self.entry_cpf.insert(0, pet["cpf"])
        # Carrega a foto armazenada no banco (LONGBLOB) se existir
        foto = pet["foto"]
        if foto:
            try:
                img = Image.open(BytesIO(foto))  # Converte bytes para imagem PIL
                img = img.resize((120, 160), Image.LANCZOS)
                self._photo_image = ImageTk.PhotoImage(img)
                self.photo_label.configure(image=self._photo_image, text="")
                self.foto_bytes = foto
            except:
                pass

    def salvar(self):
        """
        Coleta os dados dos campos do formulário e salva o pet no banco
        de dados (INSERT ou UPDATE conforme existência do pet_id).
        Executa o callback de atualização e fecha o formulário.
        """
        dados = {
            "id": self.pet_id,
            "apelido": self.entry_apelido.get().strip(),
            "raca": self.entry_raca.get().strip(),
            "data_nascimento": self.entry_nascimento.get().strip(),
            "cpf": self.entry_cpf.get().strip(),
            "foto": self.foto_bytes
        }
        salvar_pet(dados)
        if self.atualizar_callback:
            self.atualizar_callback()  # Atualiza a grid de pets na janela pai
        self.destroy()

    def excluir(self):
        """
        Exclui o pet atual do banco de dados após confirmação do usuário.
        Executa o callback de atualização e fecha o formulário.
        """
        if not self.pet_id:
            return
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este pet?"):
            deletar_pet(self.pet_id)
            if self.atualizar_callback:
                self.atualizar_callback()  # Atualiza a grid de pets na janela pai
            self.destroy()
