import socket   
import threading

#DATOS DE CONEXION
host = '127.0.0.1'
port = 55555

#CREAMOS EL SOCKET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#PASAMOS LOS DATOS DE CONEXION
server.bind((host, port))
server.listen()
print(f"El server esta en funcionamiento {host}:{port}")

#almacenamiento
clients = []
usernames = []
#ENVIA A TODOS LOS CLIENTES
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)
#aqui manejo los mensajes de cada cliente
def handle_messages(client):
    while True: #nuevos mensajes
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChaidezServidor: {username} se ha desconectado".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break


def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} se ha conectado con {str(address)}")

        message = f"ChaidezServidor: {username} Se ha unido al chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Se ha conectado a ChaidezServidor".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()


