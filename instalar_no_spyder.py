"""
Script para instalar dependências no ambiente Python do Spyder
Execute este arquivo diretamente no Spyder (F5)
"""

import subprocess
import sys

print("="*70)
print("INSTALANDO DEPENDÊNCIAS NO SPYDER")
print("="*70)
print(f"\nPython sendo usado: {sys.executable}")
print(f"Versão: {sys.version}\n")

# Lista de pacotes necessários
pacotes = [
    'customtkinter',
    'Pillow',
    'mysql-connector-python',
    'matplotlib',
    'fpdf2'
]

print("Instalando pacotes...\n")

for pacote in pacotes:
    print(f">>> Instalando {pacote}...")
    try:
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "install", pacote],
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            print(f"✓ {pacote} instalado com sucesso!\n")
        else:
            print(f"✗ Erro ao instalar {pacote}")
            print(resultado.stderr)
    except Exception as e:
        print(f"✗ Erro: {e}\n")

print("="*70)
print("INSTALAÇÃO CONCLUÍDA!")
print("="*70)
print("\n🔄 IMPORTANTE: Reinicie o Kernel do Spyder antes de executar o main.py")
print("   (Menu: Consoles -> Restart kernel)\n")

# Verifica se os pacotes foram instalados
print("Verificando instalação...")
try:
    import customtkinter
    print("✓ customtkinter OK")
except:
    print("✗ customtkinter NÃO ENCONTRADO")

try:
    from PIL import Image
    print("✓ Pillow OK")
except:
    print("✗ Pillow NÃO ENCONTRADO")

try:
    import mysql.connector
    print("✓ mysql-connector-python OK")
except:
    print("✗ mysql-connector-python NÃO ENCONTRADO")

try:
    import matplotlib
    print("✓ matplotlib OK")
except:
    print("✗ matplotlib NÃO ENCONTRADO")

try:
    import fpdf
    print("✓ fpdf2 OK")
except:
    print("✗ fpdf2 NÃO ENCONTRADO")

print("\n" + "="*70)
