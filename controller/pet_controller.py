# controller/pet_controller.py
from model.conexao_db import obter_conexao

def obter_pets():
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    cursor.close()
    conn.close()
    return pets

def obter_pet_por_id(pet_id):
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
    pet = cursor.fetchone()
    cursor.close()
    conn.close()
    return pet

def salvar_pet(dados):
    conn = obter_conexao()
    cursor = conn.cursor()
    if dados.get("id"):
        cursor.execute("UPDATE pets SET apelido=%s, raca=%s, data_nascimento=%s, cpf=%s, foto=%s WHERE id=%s",
                       (dados["apelido"], dados["raca"], dados["data_nascimento"], dados["cpf"], dados["foto"], dados["id"]))
    else:
        cursor.execute("INSERT INTO pets (apelido, raca, data_nascimento, cpf, foto) VALUES (%s, %s, %s, %s, %s)",
                       (dados["apelido"], dados["raca"], dados["data_nascimento"], dados["cpf"], dados["foto"]))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_pet(pet_id):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
    conn.commit()
    cursor.close()
    conn.close()
