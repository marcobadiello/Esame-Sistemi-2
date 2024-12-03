import subprocess
from Analisi import time_series
from Estrattore import df
import os
def avvia_script_R():
     # Percorso dello script R
    script_path = "Script.R"  # Assicurati che il file abbia estensione .R
    
    # Verifica se il file esiste
    if not os.path.isfile(script_path):
        print(f"Errore: Lo script '{script_path}' non esiste.")
        return
    
    # Esegui lo script R
    try:
        result = subprocess.run(["Rscript", script_path], check=True, text=True, capture_output=True)
        print("Output dello script R:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione dello script R:")
        print(e.stderr)

def start():
    time_series(df)
    avvia_script_R()
    print("Operazioni preliminari completate")
    
    
avvia_script_R()

