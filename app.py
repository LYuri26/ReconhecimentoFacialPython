import cv2
import numpy as np
import os
from utils.my_connection import mysql_get_mydb
from utils.create_table import create_table
from utils.data_insert import cadastro, choose

# Conectando com o MySQL e criando a tabela
cnx = mysql_get_mydb() 
create_table(cnx)

#################################################################
# Inicializando o reconhecimento facial
def creatDir(name, path=''):
    # Cria o caminho absoluto baseado no diretório atual do aplicativo
    full_path = os.path.join(os.getcwd(), path, name)
    # Verifica se o diretório não existe e, se não, cria-o
    if not os.path.exists(full_path):  
        os.makedirs(full_path)  

def saveFace():
    global saveface  
    global lastName
    saveface = True  
    creatDir('USUARIO')  
    print("CADASTRANDO..")  
    name = Nome  
    lastName = name  
    creatDir(name, 'USUARIO')  
    print(f"Diretório criado para {name}: USUARIO/{name}")
    
def saveImg(img):
    global lastName  
    user_dir = f'USUARIO/{lastName}'
    if not os.path.exists(user_dir):
        print(f"Erro: O diretório {user_dir} não existe.")
        return
    qtd = os.listdir(user_dir)  
    img_path = f'{user_dir}/{str(len(qtd))}.jpg'
    cv2.imwrite(img_path, img)
    print(f"Imagem salva em {img_path}")
        
def trainData():
    global recognizer  
    global trained
    global persons
    trained = True
    persons = os.listdir('USUARIO')  
    
    if len(persons) == 0:
        print("Nenhum usuário encontrado para treinamento.")
        return

    ids = []  
    faces = []  
    
    for i, p in enumerate(persons):  
        i += 1  
        user_folder = os.path.join('USUARIO', p)
        user_faces = os.listdir(user_folder)
        
        print(f"Usuário {p} tem {len(user_faces)} fotos.")
        
        if len(user_faces) < 2:
            print(f"Usuário {p} não tem fotos suficientes para treinamento.")
            continue
        
        for f in user_faces:  
            img = cv2.imread(os.path.join(user_folder, f), 0)  
            faces.append(img) 
            ids.append(i)  
    
    if len(faces) < 2:
        print("Não há fotos suficientes para treinamento.")
        return
    
    recognizer.train(faces, np.array(ids))  
    print("Treinamento concluído.")

    
    #################################################################

# Selecionador de opções
choose = choose()
response = cadastro(choose)
if choose == '1':
    Nome = response[0]
    cpf = response[1]
elif choose == '2':
    print("Vamos iniciar o reconhecimento facial")


# Variáveis globais
lastName = ''
saveface = False
savefaceC = 0
trained = False
persons = []

# Inicia a leitura do vídeo
cap = cv2.VideoCapture(0)
# Carrega o classificador Haar Cascade
face_cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(), 'haarcascade_frontalface_default.xml'))
# Carrega o recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Criando um loop
while(True):
    # Realiza a leitura do frame
    _, frame = cap.read()
    # Frame em cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detectando rostos no frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 6)
    
    for i, (x,y,w,h) in enumerate(faces):
        # Desenha um quadrado nos rostos
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Corta o rosto
        roi_gray = gray[y:y+h, x:x+w]
        # Ajusta a foto para 50x50
        resize = cv2.resize(roi_gray, (400, 400)) 
        # Verifica se o recognizer está treinado
        if trained:
            # Prevendo o rosto
            idf, conf = recognizer.predict(resize)
            # Obtém o nome da pessoa
            nameP = persons[idf-1]
            # Se a confiança for menor que 40, imprime o nome em verde
            if conf < 40:
                cv2.putText(frame, nameP, (x+5, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            # Se for maior que 40, imprime em vermelho
            else:
                cv2.putText(frame, nameP, (x+5, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            # Mostra um texto indicando se está treinado ou não
            cv2.putText(frame, 'TREINADO', (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'NAO TREINADA', (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        # Se a função "save" for pressionada
        if saveface:
            # Desenha o texto de "save"
            cv2.putText(frame, str(savefaceC), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
            # Incrementa o contador
            savefaceC += 1
            # Salva os rostos
            saveImg(resize)
        # Se chegar a 50 fotos, deve parar
        if savefaceC > 100:
            # Retorna o contador para 0
            savefaceC = 0
            # Desativa a variável 
            saveface = False

    # Escreve na tela
    cv2.putText(frame, "Pressione a tecla 'space' para cadastrar um novo perfil.", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "Pressione a tecla 't' para realizar o reconhecimento facial.", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "Pressione a tecla 'q' para fechar.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    # Mostra o frame
    cv2.imshow('frame', frame)
    # Espera pela tecla de comando
    key = cv2.waitKey(10) 
    # Pressionar T para treinar
    if key == 116:
        trainData()
    # Pressionar "espaço" para salvar
    if key == 32:
        saveFace()
    # Pressionar "q" para sair do loop
    if key & 0xFF == ord('q'):
        break
      
# Libera a captura
cap.release()
# Destrói as janelas
cv2.destroyAllWindows()
