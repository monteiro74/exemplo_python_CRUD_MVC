# view/form_pets.py
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
    def __init__(self, master=None, pet_id=None, atualizar_callback=None):
        super().__init__(master)
        log_event("form_pets", "__init__")
        self.title("Cadastro de Pet")
        self.geometry("600x700")
        self.resizable(False, False)
        self.pet_id = pet_id
        self.atualizar_callback = atualizar_callback
        self.foto_bytes = None
        self._photo_image = None

        self.transient(master)
        self.grab_set()

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

        ctk.CTkLabel(self, text="Foto:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.photo_label = ctk.CTkLabel(self, text="Sem foto", width=120, height=160)
        self.photo_label.pack(padx=20, pady=(0, 10))
        self.botao_foto = ctk.CTkButton(self, text="Selecionar Foto", command=self.selecionar_foto)
        self.botao_foto.pack(pady=(0, 20))

        botoes_frame = ctk.CTkFrame(self)
        botoes_frame.pack(pady=(0, 10))

        self.botao_salvar = ctk.CTkButton(botoes_frame, text="Salvar", command=self.salvar)
        self.botao_salvar.grid(row=0, column=0, padx=5)
        self.botao_excluir = ctk.CTkButton(botoes_frame, text="Excluir", fg_color="red", command=self.excluir)
        self.botao_excluir.grid(row=0, column=1, padx=5)
        self.botao_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", command=self.destroy)
        self.botao_cancelar.grid(row=0, column=2, padx=5)

        if self.pet_id:
            self.carregar_dados()
        else:
            self.botao_excluir.configure(state="disabled")

        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        w = 600
        h = 700
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")], title="Selecionar Foto")
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
            messagebox.showerror("Erro", f"Erro ao carregar imagem: {e}")

    def carregar_dados(self):
        pet = obter_pet_por_id(self.pet_id)
        if not pet:
            return
        self.entry_apelido.insert(0, pet["apelido"])
        self.entry_raca.insert(0, pet["raca"])
        self.entry_nascimento.insert(0, pet["data_nascimento"])
        self.entry_cpf.insert(0, pet["cpf"])
        foto = pet["foto"]
        if foto:
            try:
                img = Image.open(BytesIO(foto))
                img = img.resize((120, 160), Image.LANCZOS)
                self._photo_image = ImageTk.PhotoImage(img)
                self.photo_label.configure(image=self._photo_image, text="")
                self.foto_bytes = foto
            except:
                pass

    def salvar(self):
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
            self.atualizar_callback()
        self.destroy()

    def excluir(self):
        if not self.pet_id:
            return
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este pet?"):
            deletar_pet(self.pet_id)
            if self.atualizar_callback:
                self.atualizar_callback()
            self.destroy()
