
import customtkinter as ctk
from tkinter import messagebox
from controller.aluno_controller import obter_alunos
from controller.pet_controller import obter_pets
from tkinter import ttk

class FormMestreDetalhe(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Aluno e seus Pets")
        self.geometry("800x500")
        self.alunos = obter_alunos()
        self.indice = 0

        # Campos do aluno (mestre)
        ctk.CTkLabel(self, text="Nome:").pack(pady=(10,0))
        self.entry_nome = ctk.CTkEntry(self, state="disabled")
        self.entry_nome.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Curso:").pack(pady=(10,0))
        self.entry_curso = ctk.CTkEntry(self, state="disabled")
        self.entry_curso.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="CPF:").pack(pady=(10,0))
        self.entry_cpf = ctk.CTkEntry(self, state="disabled")
        self.entry_cpf.pack(fill="x", padx=20)

        # Botões de navegação
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(pady=10)
        ctk.CTkButton(nav_frame, text="<< Anterior", command=self.anterior).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Próximo >>", command=self.proximo).pack(side="left", padx=10)

        # Detalhe: Tabela de Pets
        ctk.CTkLabel(self, text="Pets do aluno:").pack(pady=(20, 0))
        self.tree_pets = ttk.Treeview(self, columns=("id", "apelido", "raca", "data_nascimento"), show="headings")
        for col in self.tree_pets["columns"]:
            self.tree_pets.heading(col, text=col.capitalize())
        self.tree_pets.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        self._center_window()
        self.mostrar_aluno()

    def _center_window(self):
        self.update_idletasks()
        w = 800
        h = 500
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def mostrar_aluno(self):
        if not self.alunos:
            return
        aluno = self.alunos[self.indice]
        self.entry_nome.configure(state="normal")
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, aluno["nome"])
        self.entry_nome.configure(state="disabled")

        self.entry_curso.configure(state="normal")
        self.entry_curso.delete(0, "end")
        self.entry_curso.insert(0, aluno["curso"])
        self.entry_curso.configure(state="disabled")

        self.entry_cpf.configure(state="normal")
        self.entry_cpf.delete(0, "end")
        self.entry_cpf.insert(0, aluno["cpf"])
        self.entry_cpf.configure(state="disabled")

        self.mostrar_pets(aluno["cpf"])

    def mostrar_pets(self, cpf):
        self.tree_pets.delete(*self.tree_pets.get_children())
        for pet in obter_pets():
            if str(pet["cpf"]) == str(cpf):
                self.tree_pets.insert("", "end", values=(pet["Id"], pet["apelido"], pet["raca"], pet["data_nascimento"]))

    def proximo(self):
        if self.indice < len(self.alunos) - 1:
            self.indice += 1
            self.mostrar_aluno()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_aluno()
