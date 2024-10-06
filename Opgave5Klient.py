import socket
import json

HOST = '127.0.0.1'  
PORT = 12001        # Nyt portnummer til JSON serveren

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Forbundet tl serveren på {HOST}:{PORT}")

        try:
            while True:
                method = input("Skriv enten 'add', 'random' eller 'subtract': ")
                num1 = input("Indtast det første tal: ")
                num2 = input("Indtast det andet tal: ")

                # Opret en JSON-forespørgsel
                request = {
                    "method": method,
                    "Tal1": int(num1),
                    "Tal2": int(num2)
                }

                # Send JSON-streng til serveren
                s.sendall(json.dumps(request).encode())

                # Modtag og dekod serverens svar
                data = s.recv(1024).decode()
                response = json.loads(data)
                
                if "error" in response:
                    print(f"Fejl: {response['error']}")
                else:
                    print(f"Resultat: {response['result']}")

        except Exception as e:
            print(f"Fejl: {e}")

if __name__ == "__main__":
    start_client()