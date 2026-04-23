# server.py - сервер чата с широковещательной рассылкой
import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5001):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []          # список сокетов подключённых клиентов
        self.lock = threading.Lock()   # блокировка для доступа к списку клиентов

    def broadcast(self, message, sender_socket=None):
        """Отправляет сообщение всем клиентам, кроме отправителя (если указан)"""
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        # Если не удалось отправить, удалим клиента позже
                        pass

    def remove_client(self, client_socket):
        with self.lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)

    def handle_client(self, client_socket, address):
        """Обрабатывает одного клиента в отдельном потоке"""
        # Приветственное сообщение для нового клиента
        try:
            client_socket.send("Добро пожаловать в чат!".encode('utf-8'))
        except:
            pass

        # Оповещаем всех остальных о новом участнике
        self.broadcast(f"Пользователь {address} присоединился к чату.", sender_socket=client_socket)

        # Цикл приёма сообщений от этого клиента
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                # Рассылаем сообщение всем остальным
                self.broadcast(f"{address}: {message}", sender_socket=client_socket)
            except:
                break

        # Клиент отключился
        self.remove_client(client_socket)
        client_socket.close()
        # Оповещаем остальных о выходе
        self.broadcast(f"Пользователь {address} покинул чат.")
        print(f"Клиент {address} отключён")

    def start(self):
        print("Сервер запущен и ожидает подключений...")
        while True:
            try:
                client_socket, client_address = self.server.accept()
                print(f"Подключился клиент: {client_address}")
                with self.lock:
                    self.clients.append(client_socket)
                # Запускаем поток для нового клиента
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.daemon = True   # поток завершится при закрытии сервера
                thread.start()
            except KeyboardInterrupt:
                print("\nСервер завершает работу...")
                break

        # Закрываем все клиентские сокеты и сервер
        with self.lock:
            for client in self.clients:
                client.close()
        self.server.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()