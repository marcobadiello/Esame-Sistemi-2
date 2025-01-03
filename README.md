[Italiano](#spotify-wrapped-statistico) / [English](#spotify-wrapped-statistical)

# Spotify wrapped Statistico

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
### 3. Carica nella cartella [Dati](##Struttura-del-Progetto) i dati da analizzare:
   Estrai il contenuto della cartella che spotify ti ha fornito (sarà una sola cartella chiamiamola 'Cartella A'). Inserisci la 'Cartella A' all'inteno della cartella [Dati](##Struttura-del-Progetto). Nella cartella dati dovrà esserci SOLAMENTE la 'Cartella A' che puoi comunque rinominare a tuo piacimento. Se non sai come scaricare i tuoi dati leggi [qui](###Ottenere-i-dati-da-Spotify). Se non hai dei dati o stai aspettando che Spotify ti consegni i tuoi puoi utilizzare dei dati di esempio reperibili nella cartella [ESEMPIO DI DATI](## Struttura del Progetto ). Prendi una delle cartelle presenti e mettila nella cartella [Dati](##Struttura-del-Progetto) non preoccuparti del nome della cartella.

### 4. **Inserisci le credenziali**:  
   Inserisci il tuo **client_id** e **client secret** all'interno del file *credenziali.py* e salva le modifiche.
   Se non sai come recuperare tali credenziali leggi [qui](###-Ottenere-le-credenziali-Spotify)

### 5. Salva correttamente tutte le modifiche

### 6. **Esegui il programma**:  
   ```bash
   uv run streamlit run app.py
   ```
Questo comando è necessario per avviare correttamente tutte le dipendenze.

---

## Struttura del Progetto  

I file di interesse del progetto sono i seguenti:
- **DATI**: Cartella che deve contenere la cartella (*my_spotify_data/*) con i dati che vuoi analizzare.
- **ESEMPIO DI DATI**: Cartella con dei dati di esempio
- **pagine/**  
  - **discover_artist.py**: Codice per la pagina "Scopri artisti".
  - **discover_track.py**: Codice per la pagina "Scopri brani".
  - **genery.py**: Codice per la pagina "Generi musicali".
  - **profilo.py**: Codice per la pagina "Profilo".
  - **readme.py**: Codice per la pagina "Readme".
  - **giornata.py**: Codice per la pagina "Giornata tipo".
  - **home.py**: Codice per la pagina "Home".
  - **shuffle.py**: Codice per la pagina "Shuffle?".  
  - **time_series_artisti.py**: Codice per la pagina "Serie storica artisti".
  - **time_series.py**: Codice per la pagina "Serie storica".
  - **Top_artisti.py**: Codice per la pagina "TOP Artisti".
  - **Top_canzoni.py**: Codice per la pagina "TOP Canzoni".
- **Analisi.py** : Codice per funzioni di analisi del dataframe.
- **app.py** : Codice principale per avviare il programma (MAIN).
- **Estrattore.py** : Codice per estrarre i dati, ripulirli e convertirli in un dataframe.
- **Tools.py** : Codice per funzioni utili.
- **README.md** : Documentazione del progetto.  

---

## Come ottenere i dati necessari al funzionamento del progetto

   ### Ottenere i dati da Spotify

   ### Ottenere le credenziali Spotify

---

## Possibili implementazioni furure

- **Possibilità di caricare i dati direttamente dall'app** (Non prima che streamlit permetta di poter caricare direttametne una cartella invece che i file singolarmente)
- **Integrazione di modelli di machine learning per un sistema di raccomandazione** (I sistemi di raccomandazione possibili con le API di Spotify sono diventati obsoleti e non più utilizzabili bisogna trovare un altro sistema)
- **Possibilità di adattare il l'applicazione ai dati di Aplle Music**


---

## Librerie utilizzate
- [Polars](https://github.com/pola-rs/polars)  
Per la gestione dei dataframe.
- [Streamlit](https://github.com/streamlit/streamlit)  
Per la creazione dell'applicazione web.
- [Altair](https://github.com/vega/altair)
Per la realizzazione dei grafici.
- [Wikipedia](https://github.com/goldsmith/Wikipedia)
Per utilizzare in modo più semplice le API di Wikipedia
-[Spotipy](https://github.com/spotipy-dev/spotipy)
Per utilizzare in modo più semplice le API di Spotify

---

## Bibliografia
Questo codice è stato scritto utilizzando queste fonti:
- https://altair-viz.github.io/
- https://docs.streamlit.io/
- https://www.reddit.com/
- https://chatgpt.com/
- https://www.reddit.com/
- https://github.com/
- https://youtube.com/
- https://developer.spotify.com/documentation/web-api
- Amici e Colleghi


---

## Ringraziamenti
- Si ringrazia [Spotify](https://www.spotify.com/) che mi ha permesso di ottenre i dati tramite questa [pagina](https://www.spotify.com/it/account/privacy).
- Si rigrazia chiunque abbia contrinuito in qualunque modo al progetto ed eventuali pull request o segnalazioni di issues.
- Si ringrazia il professore [Ceccarello Matteo](https://www.dei.unipd.it/~ceccarello/).

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
```bash
git clone https://github.com/marcobadiello/Esame-Sistemi-2.git
```

### 2. **Move into the project directory**:  
```bash
cd Esame-Sistemi-2
```

### 3. **Run the program**:  
```bash
uv run streamlit run app.py
```
This command is necessary to correctly launch all dependencies.

---

## Project Structure  

The project’s key files are as follows:
- **my_spotify_data/** : Contains the project data.  
- **pages/**  
  - **giornata.py**: Code for the "Giornata tipo" page.  
  - **home.py**: Code for the "Home" page.  
  - **shuffle.py**: Code for the "Shuffle?" page.  
  - **time_series_artisti.py**: Code for the "Serie storica artisti" page.  
  - **time_series.py**: Code for the "Serie storica" page.  
  - **Top_artisti.py**: Code for the "TOP Artisti" page.  
  - **Top_canzoni.py**: Code for the "TOP Canzoni" page.  
- **Analisi.py** : Code for dataframe analysis functions.  
- **app.py** : Main code to launch the program (MAIN).  
- **Estrattore.py** : Code to extract, clean, and convert data into a dataframe.  
- **Tools.py** : Code for utility functions.  
- **README.md** : Project documentation.  

---

## Possible Future Implementations
- **Ability to upload data directly from the app**
- **Integration of machine learning models for a recommendation system**
- **Adaptation of the application to support Apple Music data**
- **Ability to implement the use of Spotify's [APIs](https://developer.spotify.com/documentation/web-api)**

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
- https://developer.spotify.com/documentation/web-api
- Friends and Colleagues  

---

## Acknowledgments  
- Special thanks to [Spotify](https://www.spotify.com/) for enabling data retrieval through this [page](https://www.spotify.com/it/account/privacy).  
- Thanks to anyone who contributed to the project in any way, and to those submitting pull requests or reporting issues.
- A special thank you to Professor [Matteo Ceccarello](https://www.dei.unipd.it/~ceccarello/).  