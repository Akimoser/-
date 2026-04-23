# client.py - клиент чата (два потока: приём и отправка)
import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5001):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.running = True

    def receive_messages(self):
        """Поток для чтения входящих сообщений от сервера"""
        while self.running:
            try:
                data = self.client.recv(1024)
                if not data:
                    break
                print(data.decode('utf-8'))
            except:
                break
        print("Соединение с сервером разорвано.")
        self.running = False
        self.client.close()

    def send_messages(self):
        """Поток для чтения ввода пользователя и отправки на сервер"""
        while self.running:
            try:
                message = input()
                if message.lower() == '/quit':
                    break
                self.client.send(message.encode('utf-8'))
            except:
                break
        self.running = False
        self.client.close()

    def start(self):
        # Запускаем поток приёма сообщений
        recv_thread = threading.Thread(target=self.receive_messages)
        recv_thread.daemon = True
        recv_thread.start()

        # Запускаем поток отправки сообщений (основной поток можно использовать для отправки,
        # но для единообразия сделаем отдельный поток)
        send_thread = threading.Thread(target=self.send_messages)
        send_thread.daemon = True
        send_thread.start()

        # Ждём завершения потока отправки (он завершится при /quit или разрыве)
        send_thread.join()
        self.running = False
        # После завершения отправки закрываем сокет и завершаем приём
        self.client.close()

if __name__ == "__main__":
    client = ChatClient()
    client.start()