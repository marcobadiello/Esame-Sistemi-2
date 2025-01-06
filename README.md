[Italiano](#spotify-wrapped-statistico)/[English](#spotify-wrapped-statistical)

# Spotify wrapped Statistico

---

## Introduzione  
Questo progetto ha lo scopo di analizzare e visualizzare i dati relativi agliascolti di Spotify. Utilizza strumenti di analisi dati e visualizzazione per fornire insight sulle informazioni
principali dei dati di ascolto.

---

## Requisiti di sistema e dipendenze
Il progetto è stato realizzato in [Python 3.12](https://www.python.org/downloads/release/python-3120/) e tutte
le dipendenze sono state gestite con [uv](https://github.com/astral-sh/uv)

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
### 3. Carica i dati da analizzare:
   Estrai il contenuto della cartella che spotify ti ha fornito (sarà una sola cartella, chiamiamola 'Cartella A'). Inserisci la 'Cartella A' all'inteno della cartella [Dati](#Struttura-del-Progetto). Nella cartella dati dovrà esserci SOLAMENTE la 'Cartella A' che puoi comunque rinominare a tuo piacimento. Se non sai come scaricare i tuoi dati leggi [qui](#Ottenere-i-dati-da-Spotify). Se non hai dei dati o stai aspettando che Spotify ti consegni i tuoi puoi utilizzare dei dati di esempio reperibili nella cartella [ESEMPIO DI DATI](#Struttura-del-Progetto). Prendi una delle cartelle presenti e mettila nella cartella [Dati](#Struttura-del-Progetto) non preoccuparti del nome della cartella.

### 4. **Inserisci le credenziali**:  
   Inserisci il tuo **client_id** e **client secret** all'interno del file *credenziali.py* e salva le modifiche.
   Se non sai come recuperare tali credenziali leggi [qui](#Ottenere-le-credenziali-Spotify)

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
- **DOWNLOAD**: Cartella nella quale si trovano le canzoni che sono state scaricate.
- **ESEMPIO DI DOWNLOAD**: Cartella nella quale sono presenti degli esempio di canzoni scaricate.
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
  - **download_playlist.py**: Codice per la pagina "Download playlist".
  - **heetmap.py**: Codice per la pagina "HeetMap".
- **Analisi.py**: Codice per funzioni di analisi del dataframe.
- **app.py**: Codice principale per avviare il programma (MAIN).
- **Estrattore.py**: Codice per estrarre i dati, ripulirli e convertirli in un dataframe.
- **Tools.py**: Codice per funzioni utili.
- **credenziali.py**: File che contiene le credenzili per l'utilizzo delle API Spotify
- **README.md**: Documentazione del progetto.  

La comprensione degli altri file non è streattamente necessaria ai fini della comprensione del funzionamento del codice.

---

## Come ottenere i dati necessari al funzionamento del progetto

   ### Ottenere i dati da Spotify
   Seguire questo [link](https://www.spotify.com/it/account/privacy)
   Scorrere in basso
   Selezionare solo 'Cronologia di ascolto estesa'
   Premere il bottone 'Richiedi i dati'
   Ti arriverà una email di conferma
   Segui le istruzioni su quella mail per confermare la richiesta
   Attendere
   Congratulazioni hai i tuoi dati ora segui questi [passaggi](#3-Carica-i-dati-da-analizzare)

   ### Ottenere le credenziali Spotify
   Seguire questo [link](https://developer.spotify.com/documentation/web-api)
   Effettua l'accesso con le tue credenziali spotify
   Clicca sul tuo profilo in alto a destra
   Clicca su 'Dashboard'
   Crea una nuova applicazione
   Inserisci un nome a paicere
   Inserisci una descrizione a piacere
   Alla voce 'Redirect URIs' inserisci 'http://localhost:8888/callback'
   Alla voce 'Which API/SDKs are you planning to use?' spunta la casella 'Web API'
   Accetta termini e condizioni
   Crea la applicazione
   Congratulazioni hai appena creato la tua applicazione
   Ora in altro a destra clicca su 'Settings'
   Ora puoi vedere il client id e se premi su 'View client secret' puoi vedere il client secre
   Congratulazioni hai le tue credenziali ora segui questi [passaggi](#4-Inserisci-le-credenziali)

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
Per utilizzare in modo più semplice le API di Wikipedia.
- [Spotipy](https://github.com/spotipy-dev/spotipy)  
Per utilizzare in modo più semplice le API di Spotify.
- [Pytube](https://github.com/pytube/pytube)  
Per la gestione delle richieste a youtube e il download.

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

# Spotify Wrapped Statistical

---

## Introduction  
This project aims to analyze and visualize Spotify listening data. It uses data analysis and visualization tools to provide insights into the main aspects of listening data.  

---

## System Requirements and Dependencies  
The project was built with [Python 3.12](https://www.python.org/downloads/release/python-3120/), and all dependencies are managed with [uv](https://github.com/astral-sh/uv).  

You don’t need to worry about anything; a virtual environment will be created automatically if all the steps in the next chapter are followed correctly.  

---

## Project Startup  
To run the project, follow these steps:  

### 1. **Clone the repository**:  
   ```bash
   git clone https://github.com/marcobadiello/Esame-Sistemi-2.git
   ```

### 2. **Navigate to the project directory**:  
   ```bash
   cd Esame-Sistemi-2
   ```

### 3. Load the data to analyze:  
   Extract the contents of the folder Spotify provided you (there will be only one folder, let’s call it 'Folder A'). Place 'Folder A' inside the [Data](#Project-Structure) folder. The Data folder must contain ONLY 'Folder A,' which you can rename if desired. If you don’t know how to download your data, read [here](#How-to-Obtain-Data-from-Spotify). If you don’t have data yet or are waiting for Spotify to provide it, you can use sample data available in the [SAMPLE DATA](#Project-Structure) folder. Take one of the folders provided and place it in the [Data](#Project-Structure) folder without worrying about its name.

### 4. **Insert the credentials**:  
   Enter your **client_id** and **client_secret** in the *credenziali.py* file and save the changes.  
   If you don’t know how to retrieve these credentials, read [here](#How-to-Obtain-Spotify-Credentials).

### 5. Save all changes correctly

### 6. **Run the program**:  
   ```bash
   uv run streamlit run app.py
   ```
This command is required to properly start all dependencies.

---

## Project Structure  

The relevant project files are as follows:  
- **DATI**: Folder that must contain the folder (*my_spotify_data/*) with the data you want to analyze.  
- **ESEMPIO DATI**: Folder with sample data.  
- **DOWNLOAD**: Folder where the songs that have been downloaded are located.
- **ESEMPIO DI DOWNLOAD**: Folder containing examples of downloaded songs.
- **pages/**  
  - **discover_artist.py**: Code for the "Scopri artisti" page.  
  - **discover_track.py**: Code for the "Scopri brani" page.  
  - **genery.py**: Code for the "Generi musicali" page.  
  - **profile.py**: Code for the "Profilo" page.  
  - **readme.py**: Code for the "Readme" page.  
  - **day.py**: Code for the "Giornata tipo" page.  
  - **home.py**: Code for the "Home" page.  
  - **shuffle.py**: Code for the "Shuffle?" page.  
  - **time_series_artists.py**: Code for the "Serie storica artisti" page.  
  - **time_series.py**: Code for the "Serie storica" page.  
  - **Top_artists.py**: Code for the "Top Artisti" page.  
  - **Top_tracks.py**: Code for the "Top Canzoni" page.  
  - **download_playlist.py**: Code for the "Download playlist" page.
  - **heetmap.py**: Code for the "HeetMap" page.
- **Analysis.py**: Code for dataframe analysis functions.  
- **app.py**: Main code to run the program (MAIN).  
- **Extractor.py**: Code to extract, clean, and convert data into a dataframe.  
- **Tools.py**: Code for utility functions.  
- **credentials.py**: File containing Spotify API credentials.  
- **README.md**: Project documentation.  

Understanding the other files is not strictly necessary to comprehend how the code works.

---

## How to Obtain Data Required for the Project  

### Obtain Data from Spotify  
Follow this [link](https://www.spotify.com/it/account/privacy)  
Scroll down  
Select only 'Extended listening history'  
Click the 'Request data' button  
You will receive a confirmation email  
Follow the instructions in that email to confirm the request  
Wait  
Congratulations! You have your data. Now follow these [steps](#3-Load-the-data-to-analyze).  

### Obtain Spotify Credentials  
Follow this [link](https://developer.spotify.com/documentation/web-api)  
Log in with your Spotify credentials  
Click on your profile in the top-right corner  
Click 'Dashboard'  
Create a new application  
Enter a name of your choice  
Enter a description of your choice  
Under 'Redirect URIs', enter 'http://localhost:8888/callback'  
Under 'Which API/SDKs are you planning to use?', check 'Web API'  
Accept terms and conditions  
Create the application  
Congratulations! You just created your application.  
Now, in the top-right corner, click 'Settings'.  
You can now see the client ID, and if you click 'View client secret', you can see the client secret.  
Congratulations! You have your credentials. Now follow these [steps](#4-Insert-the-credentials).  

---

## Possible Future Implementations  

- **Ability to upload data directly from the app** (Not before Streamlit allows folders to be uploaded directly instead of individual files).  
- **Integration of machine learning models for a recommendation system** (Recommendation systems using Spotify APIs have become obsolete and unusable; an alternative system must be found).  
- **Ability to adapt the application to Apple Music data**.  

---

## Libraries Used  
- [Polars](https://github.com/pola-rs/polars)  
  For dataframe management.  
- [Streamlit](https://github.com/streamlit/streamlit)  
  For web application development.  
- [Altair](https://github.com/vega/altair)  
  For graph creation.  
- [Wikipedia](https://github.com/goldsmith/Wikipedia)  
  To simplify the use of Wikipedia APIs.  
- [Spotipy](https://github.com/spotipy-dev/spotipy)  
  To simplify the use of Spotify APIs.  
- [Pytube](https://github.com/pytube/pytube)  
For managing requests to YouTube and downloading.
---

## Bibliography  
This code was written using these sources:  
- https://altair-viz.github.io/  
- https://docs.streamlit.io/  
- https://www.reddit.com/  
- https://chatgpt.com/  
- https://github.com/  
- https://youtube.com/  
- https://developer.spotify.com/documentation/web-api  
- Friends and colleagues  

---

## Acknowledgments  
- Thanks to [Spotify](https://www.spotify.com/) for allowing me to obtain the data through this [page](https://www.spotify.com/it/account/privacy).  
- Thanks to anyone who contributed to the project, including pull requests or issue reports.  
- Special thanks to Professor [Ceccarello Matteo](https://www.dei.unipd.it/~ceccarello/).  
