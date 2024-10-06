import socket
import threading
import random
import json

HOST = '127.0.0.1'
PORT = 12001  # Nyt portnummer til JSON

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    
    try:
        while True:
            # Modtag JSON-forespørgsel fra klienten
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received data: {data}")
            
            try:
                # Parse JSON-data
                request = json.loads(data)
                method = request.get("method")
                num1 = request.get("Tal1")
                num2 = request.get("Tal2")

                if method not in ["add", "random", "subtract"] or num1 is None or num2 is None:
                    response = {"error": "Ukendt kommando eller manglende tal"}
                else:
                    if method == "random":
                        result = random.randint(num1, num2)
                    elif method == "add":
                        result = num1 + num2
                    elif method == "subtract":
                        result = num1 - num2

                    # Opret et JSON-svar
                    response = {"result": result}

            except json.JSONDecodeError:
                response = {"error": "Ugyldig JSON-struktur"}

            # Send JSON-svar til klienten
            conn.sendall(json.dumps(response).encode())

    except Exception as e:
        print(f"Fejl ved håndtering af klient {addr}: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()