import subprocess
from Analisi import time_series
from Estrattore import df
import os
def avvia_script_R():
    res = subprocess.call("Rscript Script.r", shell=True)
    res

def start():
    time_series(df)
    avvia_script_R()
    print("Operazioni preliminari completate")
    
    
avvia_script_R()

