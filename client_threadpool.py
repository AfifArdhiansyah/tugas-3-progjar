import sys
import socket
import logging
from concurrent.futures import ThreadPoolExecutor
import time


def send_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('localhost', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] sending {message}")
        sock.sendall(message.encode())
        data = sock.recv(32)
        logging.warning(f"[DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning("closing")
        sock.close()
    return


if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        start_time = time.time()
        request_count = 0
        futures = set()

        while time.time() - start_time < 30:
            future = executor.submit(send_data)
            futures.add(future)
            completed_futures = {f for f in futures if f.done()}
            request_count += len(completed_futures)
            futures -= completed_futures

        for future in futures:
            future.result()
            
        logging.warning(f"Total requests sent: {request_count}")
