# view/grid_pets.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from controller.pet_controller import obter_pets, deletar_pet
from view.form_pets import FormPets
from logger import log_event

class GridPets(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        log_event("grid_pets", "__init__")
        self.title("Lista de Pets")
        self.geometry("800x400")

        ctk.CTkLabel(self, text="Pets Cadastrados", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "apelido", "raca", "data_nascimento", "cpf"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.editar_selecionado)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)

        ctk.CTkButton(frame, text="Adicionar", command=self.adicionar).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Editar", command=self.editar_selecionado).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Excluir", command=self.excluir).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Fechar", command=self.destroy).pack(side="left", padx=5)

        self.atualizar_lista()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        w = 800
        h = 400
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for pet in obter_pets():
            self.tree.insert("", "end", values=(pet["Id"], pet["apelido"], pet["raca"], pet["data_nascimento"], pet["cpf"]))

    def adicionar(self):
        FormPets(self, atualizar_callback=self.atualizar_lista)

    def editar_selecionado(self, event=None):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione um pet.")
            return
        pet_id = self.tree.item(item)["values"][0]
        FormPets(self, pet_id=pet_id, atualizar_callback=self.atualizar_lista)

    def excluir(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione um pet.")
            return
        pet_id = self.tree.item(item)["values"][0]
        if messagebox.askyesno("Confirmação", "Deseja excluir este pet?"):
            deletar_pet(pet_id)
            self.atualizar_lista()
