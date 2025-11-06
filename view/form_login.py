"""
Módulo: form_login.py
Descrição: Formulário de login do sistema
Autor: Sistema
Data: 2025-11-04
"""

import customtkinter as ctk
from tkinter import messagebox
from controller.user_controller import autenticar_usuario
from logger import log_event

class FormLogin(ctk.CTkToplevel):
    """
    Classe que representa o formulário de login
    """

    def __init__(self, parent, on_success_callback):
        """
        Inicializa o formulário de login

        Args:
            parent: Janela pai
            on_success_callback: Função a ser chamada quando login for bem-sucedido
        """
        super().__init__(parent)

        log_event("FormLogin", "__init__")

        self.on_success_callback = on_success_callback
        self.autenticado = False

        # Configurações da janela
        self.title("Login - Sistema de Gerenciamento")
        self.geometry("400x300")
        self.resizable(False, False)

        # Centraliza a janela
        self.centralizar_janela()

        # Define como modal
        self.transient(parent)
        self.grab_set()

        # Criar interface
        self.criar_widgets()

        # Protocolo para fechar a janela
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Foco no campo de login
        self.entry_login.focus()

    def centralizar_janela(self):
        """
        Centraliza a janela na tela
        """
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f'{largura}x{altura}+{x}+{y}')

    def criar_widgets(self):
        """
        Cria os widgets do formulário
        """
        log_event("FormLogin", "criar_widgets")

        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        label_titulo = ctk.CTkLabel(
            main_frame,
            text="Sistema de Gerenciamento",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label_titulo.pack(pady=(20, 10))

        # Subtítulo
        label_subtitulo = ctk.CTkLabel(
            main_frame,
            text="Faça login para continuar",
            font=ctk.CTkFont(size=12)
        )
        label_subtitulo.pack(pady=(0, 30))

        # Campo Login
        label_login = ctk.CTkLabel(
            main_frame,
            text="Login:",
            font=ctk.CTkFont(size=14)
        )
        label_login.pack(pady=(0, 5))

        self.entry_login = ctk.CTkEntry(
            main_frame,
            width=300,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.entry_login.pack(pady=(0, 15))

        # Campo Senha
        label_senha = ctk.CTkLabel(
            main_frame,
            text="Senha:",
            font=ctk.CTkFont(size=14)
        )
        label_senha.pack(pady=(0, 5))

        self.entry_senha = ctk.CTkEntry(
            main_frame,
            width=300,
            height=35,
            show="*",
            font=ctk.CTkFont(size=12)
        )
        self.entry_senha.pack(pady=(0, 20))

        # Bind Enter para fazer login
        self.entry_login.bind("<Return>", lambda e: self.entry_senha.focus())
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())

        # Botões
        frame_botoes = ctk.CTkFrame(main_frame, fg_color="transparent")
        frame_botoes.pack(pady=(10, 0))

        self.btn_login = ctk.CTkButton(
            frame_botoes,
            text="Entrar",
            width=140,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.fazer_login
        )
        self.btn_login.pack(side="left", padx=5)

        self.btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            width=140,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="gray",
            hover_color="darkgray",
            command=self.on_closing
        )
        self.btn_cancelar.pack(side="left", padx=5)

    def fazer_login(self):
        """
        Realiza o processo de autenticação
        """
        log_event("FormLogin", "fazer_login")

        login = self.entry_login.get().strip()
        senha = self.entry_senha.get()

        # Validações
        if not login:
            messagebox.showwarning(
                "Campo Obrigatório",
                "Por favor, informe o login.",
                parent=self
            )
            self.entry_login.focus()
            return

        if not senha:
            messagebox.showwarning(
                "Campo Obrigatório",
                "Por favor, informe a senha.",
                parent=self
            )
            self.entry_senha.focus()
            return

        # Tenta autenticar
        if autenticar_usuario(login, senha):
            self.autenticado = True
            log_event("FormLogin", f"login_sucesso_usuario:{login}")
            messagebox.showinfo(
                "Login Bem-Sucedido",
                f"Bem-vindo(a), {login}!",
                parent=self
            )
            self.destroy()
            if self.on_success_callback:
                self.on_success_callback()
        else:
            log_event("FormLogin", f"login_falhou_usuario:{login}")
            messagebox.showerror(
                "Erro de Autenticação",
                "Login ou senha incorretos.",
                parent=self
            )
            self.entry_senha.delete(0, "end")
            self.entry_senha.focus()

    def on_closing(self):
        """
        Fecha a janela de login
        """
        log_event("FormLogin", "on_closing")

        if not self.autenticado:
            if messagebox.askokcancel(
                "Sair",
                "Deseja realmente sair do sistema?",
                parent=self
            ):
                self.destroy()
                # Fecha a aplicação inteira se não autenticou
                self.master.quit()
        else:
            self.destroy()
