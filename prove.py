import os

percorso = 'DATI'
sottocartelle = [nome for nome in os.listdir(percorso) 
                if os.path.isdir(os.path.join(percorso, nome))]
    


# Esempio di uso
percorso = 'DATI'  # Sostituisci con la tua cartella di interesse

directory = 'DATI/'+sottocartelle[0]+'/Spotify Extended Streaming History'

print(directory)