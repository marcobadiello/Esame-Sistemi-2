# Spotify wrapped Statistico
-english version below-

## Introduzione  
Questo progetto ha lo scopo di analizzare e visualizzare i dati relativi agliascolti di Spotify. Utilizza strumenti di analisi dati e visualizzazione per fornire insight sulle informazioni
principali dei dati di ascolto.

---

## Requisiti di sistema e dipendenze
Il progetto è stato realizzato in **Python 3.12** e tutte
le dipendenze sono state gestite con **uv** "https://github.com/astral-sh/uv"

Non devi preoccuparti di nulla, un ambiente virtuale verra creato automaticamente se verranno eseguiti correttamente tutti i passaggi nel capitolo successivo.


---

## Avvio del Progetto  
Per eseguire il progetto, segui questi passi:  

### 1. **Clona il repository**:  
   ```bash
   git clone https://github.com/marcobadiello/Esame-Sistemi-2.git
   ```

### 2. **Spostati nella directory del progetto**:  
   ```bash
   cd Esame-Sistemi-2
   ```

### 3. **Esegui il programma**:  
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
- Si ringrazia [Spotify](https://www.spotify.com/) che mi ha permesso di ottenre i dati tramite questa [pagina](https://www.spotify.com/it/account/privacy)
- Si rigrazia chiunque abbia contrinuito in qualunque modo al progetto ed eventuali pull request o segnalazioni di issue
- Si ringrazia il professore [Ceccarello Matteo](https://www.dei.unipd.it/~ceccarello/)

---
---
---

# Spotify Wrapped Statistical

## Introduction  
This project aims to analyze and visualize data related to Spotify listening habits. It uses data analysis and visualization tools to provide insights into the main information derived from listening data.

---

## System Requirements and Dependencies  
The project was developed using **Python 3.12**, and all dependencies are managed with **uv** [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv).

You don’t have to worry about anything— a virtual environment will be created automatically if all the steps in the next chapter are followed correctly.

---

## Project Startup  
To run the project, follow these steps:

### 1. **Clone the repository**:  
\`\`\`bash
git clone https://github.com/marcobadiello/Esame-Sistemi-2.git
\`\`\`

### 2. **Move into the project directory**:  
\`\`\`bash
cd Esame-Sistemi-2
\`\`\`

### 3. **Run the program**:  
\`\`\`bash
uv run streamlit run app.py
\`\`\`
This command is necessary to correctly launch all dependencies.

---

## Project Structure  

The project’s key files are as follows:
- **my_spotify_data/** : Contains the project data.  
- **pages/**  
  - **giornata.py**: Code for the "Daily Routine" page.  
  - **home.py**: Code for the "Home" page.  
  - **shuffle.py**: Code for the "Shuffle?" page.  
  - **time_series_artisti.py**: Code for the "Artists Time Series" page.  
  - **time_series.py**: Code for the "Time Series" page.  
  - **Top_artisti.py**: Code for the "TOP Artists" page.  
  - **Top_canzoni.py**: Code for the "TOP Songs" page.  
- **Analisi.py** : Code for dataframe analysis functions.  
- **app.py** : Main code to launch the program (MAIN).  
- **Estrattore.py** : Code to extract, clean, and convert data into a dataframe.  
- **Tools.py** : Code for utility functions.  
- **README.md** : Project documentation.  

---

## Libraries Used
- [Polars](https://github.com/pola-rs/polars)  
For dataframe management.  
- [Streamlit](https://github.com/streamlit/streamlit)  
For creating the web application.  
- [Altair](https://github.com/vega/altair)  
For generating the charts.  

---

## References  
This code was written using the following sources:  
- https://altair-viz.github.io/  
- https://docs.streamlit.io/  
- https://www.reddit.com/  
- https://chatgpt.com/  
- https://github.com/  
- Friends and Colleagues  

---

## Acknowledgments  
- Special thanks to [Spotify](https://www.spotify.com/) for enabling data retrieval through this [page](https://www.spotify.com/it/account/privacy).  
- Thanks to anyone who contributed to the project in any way, and to those submitting pull requests or reporting issues.  
- A special thank you to Professor [Matteo Ceccarello](https://www.dei.unipd.it/~ceccarello/).  
