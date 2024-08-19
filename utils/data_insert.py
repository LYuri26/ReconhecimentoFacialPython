import tkinter as tk
from tkinter import messagebox, simpledialog
from utils.my_connection import mysql_get_mydb  # Corrigido o caminho do import
from mysql.connector import Error

cnx = mysql_get_mydb()


def cadastro(nome, sobrenome, email):
    """
    Insere um novo usuário no banco de dados e retorna o ID do usuário.
    """
    try:
        connection = mysql_get_mydb()  # Usa a função de conexão existente
        if connection is None:
            raise Exception("Não foi possível conectar ao banco de dados.")

        cursor = connection.cursor()
        query = "INSERT INTO pessoas (nome, sobrenome, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, sobrenome, email))
        connection.commit()
        user_id = cursor.lastrowid
        return user_id
    except Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def fetch_users(user_id=None):
    """
    Obtém a lista de usuários do banco de dados. Se user_id for fornecido,
    retorna apenas o usuário correspondente.
    """
    try:
        connection = mysql_get_mydb()  # Usa a função de conexão existente
        if connection is None:
            raise Exception("Não foi possível conectar ao banco de dados.")

        cursor = connection.cursor()
        if user_id:
            query = "SELECT id, nome, sobrenome FROM pessoas WHERE id = %s"
            cursor.execute(query, (user_id,))
        else:
            query = "SELECT id, nome, sobrenome FROM pessoas"
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
