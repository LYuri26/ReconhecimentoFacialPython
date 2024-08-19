import mysql.connector
from mysql.connector import errorcode


def mysql_get_mydb():
    try:
        # Conectar ao MySQL sem especificar o banco de dados
        cnx = mysql.connector.connect(
            user='root', password='', host='localhost')
        print("Conexão estabelecida")

        # Cria o banco de dados se não existir
        cursor = cnx.cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS reconhecimento_facial_senai")
        cursor.execute("USE reconhecimento_facial_senai")
        cursor.close()

        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está errado com seu nome de usuário ou senha")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database não existe")
        else:
            print(err)
        return None
