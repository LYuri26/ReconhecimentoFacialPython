import mysql.connector
from mysql.connector import Error
from utils.my_connection import mysql_get_mydb


def create_table(cnx):
    cursor = cnx.cursor()
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS reconhecimento_facial_senai")
        cursor.execute("USE reconhecimento_facial_senai")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pessoas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                sobrenome VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except Error as err:
        print("Erro ao criar a tabela:")
        print(err)
    else:
        print("Tabela criada com sucesso")
    finally:
        cursor.close()


if __name__ == "__main__":
    cnx = mysql_get_mydb()
    if cnx:
        create_table(cnx)
        cnx.close()
