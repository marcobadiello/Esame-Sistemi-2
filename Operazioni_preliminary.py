import subprocess
from Analisi import time_series
from Estrattore import df
import os
def avvia_script_R():
        # Verifica se il file R esiste nella directory del progetto
    script_path = "Script.R"
    if not os.path.exists(script_path):
        print(f"Errore: il file '{script_path}' non esiste nella directory corrente.")
        return
    subprocess.run(["Rscript", script_path], check=True, capture_output=True, text=True)

def start():
    time_series(df)
    avvia_script_R()
    print("Operazioni preliminari completate")
    
    
avvia_script_R()

