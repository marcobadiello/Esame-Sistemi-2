# Visualizzazione dei Dati di Spotify

## Introduzione  
Questo progetto ha lo scopo di analizzare e visualizzare i dati relativi agliascolti di Spotify. Utilizza strumenti di analisi dati e visualizzazione per fornire insight sulle informazioni
principali dei dati di ascolto.

---

## Requisiti di Sistema  
Il progetto è stato realizzato in **Python 3.8+** e tutte
le dipendenze sono state gestite con **uv** "https://github.com/astral-sh/uv"


---

## Avvio del Progetto  
Per eseguire il progetto, segui questi passi:  

1. **Clona il repository**:  
   ```bash
   git clone https://github.com/marcobadiello/Esame-Sistemi-2.git
   ```

2. **Spostati nella directory del progetto**:  
   ```bash
   cd Esame-Sistemi-2
   ```

3. **Esegui il programma**:  
   ```bash
   uv run streamlit run app.py
   ```
Questo comando è necessario per avviare correttamente tutte le dipendenze

---

## Struttura del Progetto  

La struttura del progetto è organizzata come segue:

```plaintext
nome-progetto/
│
├── data/                       # Cartella contenente i dati
│   ├── raw/                    # Dati grezzi
│   └── processed/              # Dati elaborati
│
├── src/                        # Codice sorgente
│   ├── main.py                 # Script principale per avviare il progetto
│   ├── utils.py                # Funzioni di supporto
│   └── visualizations/         # Moduli per la visualizzazione dei dati
│       └── charts.py           # Generazione grafici
│
├── requirements.txt            # File delle dipendenze
├── README.md                   # Documentazione del progetto
└── .gitignore                  # File per ignorare i file nel repository Git
```

---

## Bibliografia  
- [Documentazione Spotify API](https://developer.spotify.com/documentation/web-api/)  
- [uv - gestione delle dipendenze](https://github.com/astral-sh/uv)  
- Altre fonti...
