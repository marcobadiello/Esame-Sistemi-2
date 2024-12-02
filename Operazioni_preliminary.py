import subprocess
from Analisi import time_series
from Estrattore import df
def avvia_script_R():
        # Definisci il percorso del file R
    r_script = "Script.R"


    # Esegui lo script R con Rscript
    try:
        subprocess.run(["Script.R"])

    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione dello script R:", e.stderr)

def start():
    time_series(df)
    avvia_script_R()
    print("Operazioni preliminari completate")
    
    
    

