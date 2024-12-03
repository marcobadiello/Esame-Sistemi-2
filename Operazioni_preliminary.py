import subprocess
from Analisi import time_series
from Estrattore import df
def avvia_script_R():
    # Definisci il percorso del file R
    r_script = "Script.R"  # Aggiungi il percorso completo se non si trova nella stessa cartella

    # Esegui lo script R con Rscript
    try:
        result = subprocess.run(["Rscript", r_script], check=True, capture_output=True, text=True)
        print("Script eseguito correttamente!")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione dello script R:", e.stderr)
def start():
    time_series(df)
   #avvia_script_R()
    print("Operazioni preliminari completate")
    
    
    

