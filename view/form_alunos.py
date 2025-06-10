# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: form_alunos.py - Formulário de cadastro e edição de aluno
# Descrição: Este script exibe um formulário modal para operações CRUD de aluno,
#            incluindo seleção e exibição de foto 3×4.
#
# Autor: Nome do aluno
# Data de Criação: 
# Hora de Criação: 
#
# Dependências:
# - customtkinter: Para criação da interface gráfica.
# - PIL: Para manipulação e redimensionamento de imagens.
# - controller.aluno_controller: Para operações de banco de dados de alunos.
#
# Uso: Abra a grade de alunos e clique em 'Adicionar' ou 'Editar' para usar este formulário.
# ==============================================================================

# view/form_alunos.py
# Formulário modal para operações CRUD de aluno com exibição de foto 3×4 e logging

import os, sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import customtkinter as ctk
from tkinter import filedialog, messagebox
from controller.aluno_controller import salvar_aluno, obter_aluno_por_matricula, deletar_aluno
from PIL import Image, ImageTk
from io import BytesIO
from logger import log_event

class FormAlunos(ctk.CTkToplevel):
    """
    Janela modal para cadastro, edição e visualização de alunos.
    Permite inserir, atualizar, excluir, limpar e cancelar operações de CRUD,
    além de selecionar e exibir foto 3x4 do aluno.

    Parâmetros:
        master: Janela principal que chama este formulário.
        matricula: Matrícula do aluno para edição (opcional).
        atualizar_callback: Função callback para atualizar a lista após salvar/editar.
    """

    def __init__(self, master=None, matricula=None, atualizar_callback=None):
        """
        Inicializa o formulário de aluno, montando todos os campos de entrada,
        botões de ação e carregando dados se for edição.
        """
        super().__init__(master)
        log_event("form_alunos", "__init__")
        self.title("Cadastro de Aluno")
        self.geometry("420x640")
        self.resizable(False, False)
        self.matricula = matricula
        self.atualizar_callback = atualizar_callback
        self.foto_bytes = None
        self._photo_image = None  # Referência para ImageTk

        # Torna este form modal
        self.transient(master)
        self.grab_set()

        # ─── Campos de entrada ─────────────────────────────────────────────────

        # Matrícula
        ctk.CTkLabel(self, text="Matrícula:", anchor="w").pack(fill="x", padx=20, pady=(20, 0))
        self.entry_matricula = ctk.CTkEntry(self)
        self.entry_matricula.pack(fill="x", padx=20, pady=(0, 10))

        # Nome
        ctk.CTkLabel(self, text="Nome:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(self)
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 10))

        # Curso
        ctk.CTkLabel(self, text="Curso:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.entry_curso = ctk.CTkEntry(self)
        self.entry_curso.pack(fill="x", padx=20, pady=(0, 10))

        # Sexo
        ctk.CTkLabel(self, text="Sexo:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.option_sexo = ctk.CTkComboBox(self, values=["Masculino", "Feminino"])
        self.option_sexo.pack(fill="x", padx=20, pady=(0, 10))

        # Idade
        ctk.CTkLabel(self, text="Idade:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.entry_idade = ctk.CTkEntry(self)
        self.entry_idade.pack(fill="x", padx=20, pady=(0, 10))

        # ─── Exibição de Foto 3×4 ───────────────────────────────────────────────
        ctk.CTkLabel(self, text="Foto 3×4:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))

        self.photo_label = ctk.CTkLabel(self, text="Sem foto", width=120, height=160)
        self.photo_label.pack(padx=20, pady=(0, 10))

        self.botao_foto = ctk.CTkButton(self, text="Selecionar Foto", command=self.selecionar_foto)
        self.botao_foto.pack(pady=(0, 20))

        # ─── Botões CRUD ────────────────────────────────────────────────────────
        botoes_frame = ctk.CTkFrame(self)
        botoes_frame.pack(pady=(10, 10))

        self.botao_inserir = ctk.CTkButton(botoes_frame, text="Inserir", width=80, command=self.inserir)
        self.botao_inserir.grid(row=0, column=0, padx=5)

        self.botao_atualizar = ctk.CTkButton(botoes_frame, text="Atualizar", width=80, command=self.atualizar)
        self.botao_atualizar.grid(row=0, column=1, padx=5)

        self.botao_excluir = ctk.CTkButton(botoes_frame, text="Excluir", width=80, fg_color="red", command=self.excluir)
        self.botao_excluir.grid(row=0, column=2, padx=5)

        self.botao_limpar = ctk.CTkButton(botoes_frame, text="Limpar", width=80, command=self.limpar_campos)
        self.botao_limpar.grid(row=0, column=3, padx=5)

        self.botao_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", width=80, command=self.destroy)
        self.botao_cancelar.grid(row=0, column=4, padx=5)

        # Se for edição (já recebeu matrícula), carrega dados
        if self.matricula:
            self.carregar_dados()
            self.entry_matricula.configure(state="disabled")
        else:
            # Novo cadastro: desabilita botão Excluir
            self.botao_excluir.configure(state="disabled")

        # Centraliza a janela
        self._center_window()

    def _center_window(self):
        """
        Centraliza a janela no centro da tela do usuário.
        """
        self.update_idletasks()
        w = 500
        h = 700
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def selecionar_foto(self):
        """
        Permite ao usuário selecionar uma foto 3x4 do aluno.
        Redimensiona, exibe e armazena a foto em memória.
        """
        log_event("form_alunos", "selecionar_foto")
        caminho = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.jpg *.jpeg *.png")],
            title="Selecione uma foto 3×4"
        )
        if not caminho:
            return
        try:
            img = Image.open(caminho)
            img = img.resize((120, 160), Image.LANCZOS)
            self._photo_image = ImageTk.PhotoImage(img)
            self.photo_label.configure(image=self._photo_image, text="")
            with open(caminho, "rb") as f:
                self.foto_bytes = f.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar imagem: {e}")
            self.foto_bytes = None

    def carregar_dados(self):
        """
        Carrega os dados do aluno selecionado para edição, preenchendo os campos do formulário.
        Também carrega a foto do aluno, se existir.
        """
        log_event("form_alunos", "carregar_dados")
        aluno = obter_aluno_por_matricula(self.matricula)
        if not aluno:
            return
        self.entry_matricula.insert(0, aluno["matricula"])
        self.entry_nome.insert(0, aluno["nome"])
        self.entry_curso.insert(0, aluno["curso"])
        self.entry_idade.insert(0, aluno["idade"])
        self.option_sexo.set(aluno.get("sexo", ""))
        foto_bytes = aluno.get("foto", None)
        if foto_bytes:
            try:
                img = Image.open(BytesIO(foto_bytes))
                img = img.resize((120, 160), Image.LANCZOS)
                self._photo_image = ImageTk.PhotoImage(img)
                self.photo_label.configure(image=self._photo_image, text="")
                self.foto_bytes = foto_bytes
            except Exception as e:
                messagebox.showwarning("Aviso", f"Falha ao exibir foto salva: {e}")
                self.foto_bytes = None

    def salvar(self):
        """
        Salva ou atualiza os dados do aluno no banco de dados.
        Valida os campos obrigatórios e exibe mensagens modais de sucesso ou erro.
        """
        log_event("form_alunos", "salvar")
        matricula = self.entry_matricula.get().strip()
        nome = self.entry_nome.get().strip()
        curso = self.entry_curso.get().strip()
        idade = self.entry_idade.get().strip()

        if not all([matricula, nome, curso, idade]):
            messagebox.showwarning("Validação", "Preencha todos os campos antes de salvar.")
            return

        dados = {
            "matricula": matricula,
            "nome": nome,
            "curso": curso,
            "idade": idade,
            "sexo": self.option_sexo.get(),
            "foto": self.foto_bytes
        }

        try:
            salvar_aluno(dados)
            messagebox.showinfo("Sucesso", "Dados do aluno salvos com sucesso.")
            if not self.matricula:
                self.entry_matricula.configure(state="disabled")
                self.matricula = matricula
                self.botao_excluir.configure(state="normal")
            if self.atualizar_callback:
                self.atualizar_callback()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar aluno: {e}")

    def excluir(self):
        """
        Exclui o aluno atual do banco de dados após confirmação do usuário.
        """
        log_event("form_alunos", "excluir")
        if not self.matricula:
            return
        resposta = messagebox.askyesno("Confirmar Exclusão", "Deseja realmente excluir este aluno?")
        if not resposta:
            return
        try:
            deletar_aluno(self.matricula)
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso.")
            if self.atualizar_callback:
                self.atualizar_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir aluno: {e}")

    def limpar_campos(self):
        """
        Limpa todos os campos do formulário, reseta imagem e estados dos botões.
        """
        log_event("form_alunos", "limpar_campos")
        self.entry_matricula.configure(state="normal")
        self.entry_matricula.delete(0, "end")
        self.entry_nome.delete(0, "end")
        self.entry_curso.delete(0, "end")
        self.entry_idade.delete(0, "end")
        self.option_sexo.set("")
        self.photo_label.configure(image=None, text="Sem foto")
        self.foto_bytes = None
        self._photo_image = None
        self.botao_excluir.configure(state="disabled")
        self.matricula = None

    def inserir(self):
        """
        Realiza o cadastro de um novo aluno usando os dados preenchidos no formulário.
        """
        log_event("form_alunos", "inserir")
        self._salvar_novo()

    def atualizar(self):
        """
        Atualiza os dados do aluno existente no banco de dados.
        """
        log_event("form_alunos", "atualizar")
        if not self.matricula:
            messagebox.showwarning("Aviso", "Nenhum aluno carregado para atualizar.")
            return
        self._salvar_existente()

    def _salvar_novo(self):
        """
        Salva um novo aluno no banco de dados.
        """
        matricula = self.entry_matricula.get().strip()
        nome = self.entry_nome.get().strip()
        curso = self.entry_curso.get().strip()
        idade = self.entry_idade.get().strip()
        sexo = "M" if self.option_sexo.get() == "Masculino" else "F"

        if not all([matricula, nome, curso, idade]):
            messagebox.showwarning("Validação", "Preencha todos os campos antes de salvar.")
            return

        dados = {
            "matricula": matricula,
            "nome": nome,
            "curso": curso,
            "idade": idade,
            "sexo": sexo,
            "foto": self.foto_bytes
        }

        try:
            salvar_aluno(dados)
            messagebox.showinfo("Sucesso", "Aluno inserido com sucesso.")
            self.matricula = matricula
            if self.atualizar_callback:
                self.atualizar_callback()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao inserir aluno: {e}")

    def _salvar_existente(self):
        """
        Atualiza os dados de um aluno já existente no banco de dados.
        """
        nome = self.entry_nome.get().strip()
        curso = self.entry_curso.get().strip()
        idade = self.entry_idade.get().strip()
        sexo = "M" if self.option_sexo.get() == "Masculino" else "F"

        if not all([self.matricula, nome, curso, idade]):
            messagebox.showwarning("Validação", "Preencha todos os campos antes de atualizar.")
            return

        dados = {
            "matricula": self.matricula,
            "nome": nome,
            "curso": curso,
            "idade": idade,
            "sexo": sexo,
            "foto": self.foto_bytes
        }

        try:
            salvar_aluno(dados)
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso.")
            if self.atualizar_callback:
                self.atualizar_callback()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar aluno: {e}")
