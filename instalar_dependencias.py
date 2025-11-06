"""
Script para instalar todas as dependências do projeto
Execute este script antes de rodar o main.py
"""

import subprocess
import sys

def instalar_pacotes():
    """
    Instala todos os pacotes necessários para o projeto
    """
    pacotes = [
        'customtkinter',
        'Pillow',
        'mysql-connector-python',
        'matplotlib',
        'fpdf2'
    ]

    print("="*60)
    print("Instalando dependências do projeto...")
    print("="*60)
    print(f"\nPython executável: {sys.executable}")
    print(f"Versão do Python: {sys.version}\n")

    for pacote in pacotes:
        print(f"\n>>> Instalando {pacote}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
            print(f"✓ {pacote} instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Erro ao instalar {pacote}: {e}")

    print("\n" + "="*60)
    print("Instalação concluída!")
    print("="*60)
    print("\nVerificando pacotes instalados:")
    subprocess.check_call([sys.executable, "-m", "pip", "list"])

if __name__ == "__main__":
    instalar_pacotes()
