import os

def leggi_credenziali():
    file_path = "credenziali.txt"
    if not os.path.exists(file_path):
        print("Errore: Il file specificato non esiste.")
        return (None,None,None)

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            client_id = lines[0].strip()
            client_secret = lines[1].strip()
            redirect_uri = lines[2].strip()
            return (client_id,client_secret,redirect_uri)
    except IndexError:
        print("Errore: Il file non contiene il formato corretto.")
        return (None,None,None)

