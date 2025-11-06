# -*- coding: utf-8 -*-
# ==============================================================================
# Nome do Script: main.py - Interface Principal da Aplicação de Gerenciamento de Alunos
# Descrição: Este script exibe a janela principal do sistema, integra menus e
#            registra todas as principais ações e eventos em arquivo de log.
#
# Autor: Nome do aluno
# Data de Criação:
# Hora de Criação:
#
# Dependências:
# - customtkinter: Para interface gráfica moderna.
# - tkinter: Para widgets de menu e manipulação de eventos.
# - PIL: Para manipulação e exibição da imagem de fundo.
# - logger: Para registro dos eventos em log.
#
# Uso: Execute este script a partir da raiz do projeto.
# ==============================================================================

import customtkinter as ctk
import tkinter as tk
from tkinter import Menu, messagebox
from PIL import Image, ImageTk
import os

from view.grid_alunos import GridAlunos
from view.form_alunos import FormAlunos
from view.form_idade_alunos import FormIdadeAlunos
from view.form_quantidade_alunos import FormQuantidadeAlunos
from view.report_alunos import ReportAlunos
from view.form_sobre import FormSobre
from view.form_licenca import FormLicenca
from view.grid_pets import GridPets
from view.form_login import FormLogin

from logger import log_event

def log_and_print(msg):
    """
    Registra uma mensagem no log e imprime no console.
    """
    log_event("main", msg)
    print(f">>> {msg}")

log_and_print("Script main.py iniciado")

class MainView(ctk.CTk):
    """
    Classe principal da aplicação. Exibe a janela principal, gerencia menus,
    carrega a imagem de fundo e responde aos eventos do usuário.

    Métodos:
        - __init__: Inicializa a interface principal.
        - _center_window: Centraliza a janela na tela.
        - _load_original_wallpaper: Carrega a imagem de fundo padrão.
        - _apply_wallpaper: Aplica/redimensiona a imagem de fundo conforme o tamanho da janela.
        - _on_resize: Evento chamado ao redimensionar a janela.
        - configurar_menu: Cria e configura a barra de menus.
        - Funções de abertura de cada formulário e gráfico.
        - exportar_alunos_csv: Exporta lista de alunos para arquivo CSV.
    """
    def __init__(self):
        """
        Inicializa a janela principal, define dimensões, tema, carrega imagem de fundo
        e configura menus.
        """
        log_and_print("Entrando em MainView.__init__")
        super().__init__()
        log_and_print("Chamou super().__init__")

        # Define o modo de aparência claro para toda a interface (CustomTkinter)
        ctk.set_appearance_mode('light')
        self.title("Sistema de Gerenciamento de Alunos e Pets")

        # Define as dimensões padrão da janela principal
        self._window_width = 800
        self._window_height = 600
        self._center_window()

        # Carrega o wallpaper original (imagem de fundo)
        self._load_original_wallpaper()

        # Cria um Label para exibir a imagem de fundo, ocupando toda a janela
        self._bg_label = tk.Label(self)
        self._bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Aplica a imagem de fundo ao iniciar a janela
        self._apply_wallpaper(self._window_width, self._window_height)

        # Liga evento de redimensionamento para redimensionar o wallpaper automaticamente
        self.bind("<Configure>", self._on_resize)

        # Configura a barra de menus superior
        self.configurar_menu()

        # Abre a tela de login após inicializar a janela
        self.after(100, self.mostrar_login)

    def _center_window(self):
        """
        Centraliza a janela principal do aplicativo no centro da tela.
        """
        self.update_idletasks()
        w = self._window_width
        h = self._window_height
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _load_original_wallpaper(self):
        """
        Carrega a imagem do wallpaper padrão do diretório 'images'.
        Caso a imagem não seja encontrada, exibe um erro para o usuário.
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            wallpaper_path = os.path.join(script_dir, "images", "wallpaper.jpg")
            if not os.path.exists(wallpaper_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {wallpaper_path}")
            self._orig_wallpaper = Image.open(wallpaper_path)
        except Exception as e:
            messagebox.showerror("Erro ao carregar wallpaper", f"Ocorreu um erro ao carregar o wallpaper:\n{e}")
            self._orig_wallpaper = None

    def _apply_wallpaper(self, width, height):
        """
        Redimensiona e aplica a imagem de fundo conforme o tamanho atual da janela.
        """
        if not self._orig_wallpaper:
            return
        try:
            resized = self._orig_wallpaper.resize((width, height), Image.LANCZOS)
            self._wallpaper_photo = ImageTk.PhotoImage(resized)
            self._bg_label.configure(image=self._wallpaper_photo)
        except Exception as e:
            messagebox.showerror("Erro ao aplicar wallpaper", f"Ocorreu um erro ao aplicar o wallpaper:\n{e}")

    def _on_resize(self, event):
        """
        Evento disparado ao redimensionar a janela principal.
        Redimensiona o wallpaper conforme novo tamanho.
        """
        new_w = event.width
        new_h = event.height
        # Evita redimensionamentos mínimos (janela minimizada)
        if new_w < 10 or new_h < 10:
            return
        self._apply_wallpaper(new_w, new_h)

    def configurar_menu(self):
        """
        Cria e configura a barra de menus da janela principal, adicionando as opções
        de Arquivo, Gráficos, Relatórios e Sobre, com seus respectivos comandos.
        """
        menu_bar = Menu(self)

        # Menu Arquivo: operações básicas
        menu_arquivo = Menu(menu_bar, tearoff=0)
        menu_arquivo.add_command(label="Abrir Grade de Alunos", command=self.abrir_grid_alunos)
        menu_arquivo.add_command(label="Abrir Formulário de Alunos", command=self.abrir_form_alunos)
        menu_arquivo.add_command(label="Abrir Grade de Pets", command=self.abrir_grid_pets)
        menu_arquivo.add_command(label="Mestre-Detalhe", command=self.abrir_mestre_detalhe)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.destroy)

        # Menu Gráficos: exibição de gráficos estatísticos
        menu_graficos = Menu(menu_bar, tearoff=0)
        menu_graficos.add_command(label="Gráfico de Idade dos Alunos", command=self.abrir_grafico_idade)
        menu_graficos.add_command(label="Gráfico de Quantidade de Alunos", command=self.abrir_grafico_quantidade)

        # Menu Relatórios: geração de PDFs e exportação de dados
        menu_relatorios = Menu(menu_bar, tearoff=0)
        menu_relatorios.add_command(label="Relatório de Alunos", command=self.abrir_relatorio)
        # Nova opção: exportar alunos para CSV
        menu_relatorios.add_command(label="Exportar Alunos para CSV", command=self.exportar_alunos_csv)

        # Menu Sobre: informações do sistema e licença
        menu_sobre = Menu(menu_bar, tearoff=0)
        menu_sobre.add_command(label="Sobre", command=self.abrir_sobre)
        menu_sobre.add_command(label="Licença", command=self.abrir_licenca)

        # Adiciona todos os menus à barra de menus principal
        menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_bar.add_cascade(label="Gráficos", menu=menu_graficos)
        menu_bar.add_cascade(label="Relatórios", menu=menu_relatorios)
        menu_bar.add_cascade(label="Sobre", menu=menu_sobre)

        self.config(menu=menu_bar)

    def abrir_grid_alunos(self):
        """
        Abre a janela de listagem (grade) de alunos em modo modal.
        """
        try:
            form = GridAlunos(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Grade de Alunos", str(e))

    def abrir_form_alunos(self):
        """
        Abre o formulário de cadastro/edição de alunos em modo modal.
        """
        try:
            form = FormAlunos(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Formulário de Alunos", str(e))

    def abrir_grid_pets(self):
        """
        Abre a janela de listagem de pets em modo modal.
        """
        try:
            form = GridPets(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Grade de Pets", str(e))

    def abrir_grafico_idade(self):
        """
        Abre a janela com o gráfico de distribuição de idades dos alunos.
        """
        try:
            form = FormIdadeAlunos(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Gráfico de Idade", str(e))

    def abrir_grafico_quantidade(self):
        """
        Abre a janela com o gráfico de quantidade total de alunos.
        """
        try:
            form = FormQuantidadeAlunos(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Gráfico de Quantidade", str(e))

    def abrir_relatorio(self):
        """
        Abre a janela para geração do relatório PDF dos alunos.
        """
        try:
            form = ReportAlunos(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Relatório", str(e))

    def exportar_alunos_csv(self):
        """
        Exporta a lista de alunos para um arquivo CSV no diretório do script.
        Caso não haja alunos cadastrados, exibe mensagem de informação.
        """
        from controller.aluno_controller import obter_alunos
        import csv

        try:
            alunos = obter_alunos()
            if not alunos:
                messagebox.showinfo("Exportar CSV", "Não há alunos cadastrados para exportar.")
                return
            # Define o nome do arquivo exportado
            arquivo_csv = "alunos_exportados.csv"
            with open(arquivo_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=alunos[0].keys())
                writer.writeheader()
                writer.writerows(alunos)
            messagebox.showinfo("Exportar CSV", f"Alunos exportados para {arquivo_csv}!")
            log_event("main", "Exportação de alunos para CSV realizada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro ao exportar CSV", str(e))
            log_event("main", f"ERRO exportar_alunos_csv: {e}")

    def abrir_mestre_detalhe(self):
        """
        Abre a janela mestre-detalhe (aluno e seus pets).
        Importação dinâmica para evitar problemas de import recursivo.
        """
        try:
            from view.form_mestre_detalhe import FormMestreDetalhe
            form = FormMestreDetalhe(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Mestre-Detalhe", str(e))
            log_event("main", f"ERRO abrir_mestre_detalhe: {e}")

    def abrir_sobre(self):
        """
        Abre a janela com informações sobre o sistema.
        """
        try:
            form = FormSobre(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Sobre", str(e))

    def abrir_licenca(self):
        """
        Abre a janela com informações sobre a licença de uso.
        """
        try:
            form = FormLicenca(self)
            form.transient(self)
            form.grab_set()
            form.focus_set()
        except Exception as e:
            messagebox.showerror("Erro ao abrir Licença", str(e))

    def mostrar_login(self):
        """
        Exibe a tela de login ao iniciar o sistema.
        """
        log_and_print("Abrindo tela de login")
        try:
            login_form = FormLogin(self, self.on_login_success)
        except Exception as e:
            messagebox.showerror("Erro ao abrir Login", str(e))
            self.quit()

    def on_login_success(self):
        """
        Callback chamado quando o login é bem-sucedido.
        """
        log_and_print("Login realizado com sucesso - sistema pronto para uso")

if __name__ == "__main__":
    """
    Ponto de entrada do sistema. Inicializa e executa o loop principal da aplicação.
    Em caso de erro fatal, exibe mensagem ao usuário.
    """
    try:
        app = MainView()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Erro fatal", f"Erro ao iniciar aplicação:\n{e}")
