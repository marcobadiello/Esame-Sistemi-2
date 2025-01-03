[Italiano](#spotify-wrapped-statistico)

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
### 3. Carica i dati da analizzare:
   Estrai il contenuto della cartella che spotify ti ha fornito (sarà una sola cartella chiamiamola 'Cartella A'). Inserisci la 'Cartella A' all'inteno della cartella [Dati](#Struttura-del-Progetto). Nella cartella dati dovrà esserci SOLAMENTE la 'Cartella A' che puoi comunque rinominare a tuo piacimento. Se non sai come scaricare i tuoi dati leggi [qui](#Ottenere-i-dati-da-Spotify). Se non hai dei dati o stai aspettando che Spotify ti consegni i tuoi puoi utilizzare dei dati di esempio reperibili nella cartella [ESEMPIO DI DATI](## Struttura del Progetto ). Prendi una delle cartelle presenti e mettila nella cartella [Dati](#Struttura-del-Progetto) non preoccuparti del nome della cartella.

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
   Seguire questo [link](https://www.spotify.com/it/account/privacy)
   Scorrere in basso
   Selezionare solo 'Cronologia di ascolto estesa'
   Premere il bottone 'Richiedi i dati'
   Ti arriverà una email di conferma
   Segui le istruzioni su quella mail per confermare la richiesta
   Attendere
   Congratulazioni hai i tuoi dati ora segui questi [passaggi](#-3.-Carica-i-dati-da-analizzare:)

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
   Congratulazioni hai le tue credenziali ora segui questi [passaggi](#-4.-**Inserisci-le-credenziali**:)

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

