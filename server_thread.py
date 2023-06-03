from socket import *
import socket
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address, server):
		self.connection = connection
		self.address = address
		self.server = server
		threading.Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(32)
			if data:
				# perika request apakah berawalan "TIME" dan berakhiran karakter 13 dan 10
				if data.startswith(b'TIME') and data.endswith(b'\r\n'):
					# membuat response
					current_time = time.strftime("%H:%M:%S")
					response = f"JAM {current_time}\r\n"
					logging.warning(f"[SERVER] sending {response}")
					self.connection.sendall(response.encode('utf-8'))
				else:
					break
			else:
				break
		self.connection.close()

# Time Server
class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.client_count = 0
		self.response_count = 0  # Tambahkan counter untuk jumlah response
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0', 45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")

			clt = ProcessTheClient(self.connection, self.client_address, self)
			clt.start()
			self.the_clients.append(clt)
			self.client_count += 1
			logging.warning(f"Total clients connected: {self.client_count}")

	def update_response_count(self):
		self.response_count += 1
		logging.warning(f"Total responses sent: {self.response_count}")

def main():
	svr = Server()
	svr.start()

if __name__ == "__main__":
	main()
