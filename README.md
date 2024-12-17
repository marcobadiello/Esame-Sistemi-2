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

I file di interesse del progetto sono i seguenti:
- **my_spotify_data/** : Contiene i dati del progetto.  
- **pagine/**  
  - **giornata.py**: Codice per la pagina "Giornata tipo".
  - **home.py**: Codice per la pagina "Home".
  - **shuffle.py**: Codice per la pagina "Shuffle?".  
  - **time_series_artisti.py**: Codice per la pagina "Serie storica artisti".
  - **time_series.py**: Codice per la pagina "Serie storica".
  - **Top_artisti.py**: Codice per la pagina "TOP Artisti".
  - **Top_canzoni.py**: Codice per la pagina "TOP Canzoni".
- **Analisi.py** : Codice per funzioni di analisi del dataframe.
- **app.py** : Codice principale per avviare il programma (MAIN)
- **Estrattore.py** : Codice per estrarre i dati, ripulirli e convertirli in un dataframe
- **Tools.py** : Codice per funzioni utili.
- **README.md** : Documentazione del progetto.  

---

## Librerie utilizzate
- [Polars](https://github.com/pola-rs/polars)  
Per la gestione dei dataframe
- [Streamlit](https://github.com/streamlit/streamlit)  
Per la creazione dell'applicazione web
- [Altair](https://github.com/vega/altair)
Per la realizzazione dei grafici

---

## Bibliografia
Questo codice è stato scritto utilizzando queste fonti
- https://altair-viz.github.io/
- https://docs.streamlit.io/
- https://www.reddit.com/
- https://chatgpt.com/
- https://www.reddit.com/
- https://github.com/
- Amici e Colleghi


---

## Ringraziamenti