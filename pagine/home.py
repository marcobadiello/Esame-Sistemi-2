import streamlit as st
from Estrattore import df
import Tools

def run_home():
    """
    Configura e visualizza la home page del progetto Spotify Wrapped Statistico utilizzando Streamlit.

    La home page include:
    - Configurazione della pagina con layout ampio e barra laterale ridotta.
    - Logo di Spotify e titolo.
    - Descrizione del progetto e degli obiettivi.
    - Descrizione del dataset con spiegazioni dettagliate dei campi.
    - Bottone per visualizzare il dataframe.
    - Link alla pagina README e alla pagina del progetto su GitHub.
    - Descrizione delle varie pagine disponibili nel progetto, tra cui:
        - Profilo
        - Readme
        - TOP Canzoni
        - TOP Artisti
        - Serie storica
        - Serie storica artisti
        - Shuffle?
        - Giornata tipo
        - Generi musicali
        - HeetMap
        - Scopri artisti
        - Scopri brani
        - Scarica playlist
    - Footer con il nome del creatore.

    Nota:
    - La funzione presuppone che la libreria Streamlit sia importata come `st`.
    - Il dataframe `df` dovrebbe essere definito altrove nel codice.
    """

    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )

    # metto il titolo e il logo di spotify
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    
    st.markdown("## **Descrizione del progetto**")
    st.markdown("---")
    st.subheader("Obbiettivi")
    st.write('''
Gli obiettivi di questo progetto sono la presentazione dei miei dati personali di Spotify
            , cercando di avere un riassunto il più chiaro possibile di quelli che sono i miei gusti musicali e di come sono 
             variati nel corso del tempo.
             Inoltre il progetto è interamente strutturato da essere indipendente dai dati, questo lo rende versatile
             poichè qualora si volessero cambiare i dati con quelli di un altra persona il progetto si adatterebbe di conseguenza 
             senza bisogno di ulteriori aggiustamenti.
''')


    st.subheader("Il dataset")
    st.write('''
            Il dataset raccoglie tutte le mie strem eseguite su Spotify.
''')
    st.markdown('''
        - **ts**: Istante temporale in cui è stata eseguita la stream.
        - **s_played**: Aggiungi altre descrizioni qui.
        - **master_metadata_track_name**: Titolo della canzone
        - **master_metadata_album_artist_name**: Titolo dell'artista
        - **master_metadata_album_album_name**: Titolo dell'album
        - **spotify_track_uri**: Codice identificativo del brano
        - **shuffle**: Variabile dicotomica. La stram era o non era n riproduzione casuale
    ''')
    
    # creo un bottone per mostrare il dataframe
    if st.button("Mostra dataframe"):
        st.write(df)
        
    
    
    st.markdown("---")
    st.subheader("Per maggiori informazioni consiglio vivamente di leggere la pagina 'Readme' o visitare la [pagina GitHub del progetto](https://github.com/marcobadiello/Esame-Sistemi-2).")
    st.markdown("---")
    st.title("📒Le pagine")
    st.subheader("Profilo")
    st.write('''
In questa pagina puoi trovare una panoramica del profilo spotify associato alle API Spotify utilizzate, inoltre è possibile vedere una top canzoni e artisti molto generale.
    ''')
    st.subheader("Readme")
    st.write('''
In questa pagina è riportato il file Readme ovvero la documentazione del progetto, consiglio vivamente di leggerlo.           
''')
    st.subheader("TOP Canzoni")
    st.write('''
In questa pagina puoi vedere una classifica delle canzoni molto dettaglaita. Viene offerta la possibilità di scegliere quante posizioni vedere e in quel periodo di tempo.
''')
    st.subheader("TOP Artisti")
    st.write('''
In questa pagina puoi vedere una classifica degli artisti molto dettaglaita. Viene offerta la possibilità di scegliere quante posizioni vedere e in quel periodo di tempo.
''')
    st.subheader("Serie storica")
    st.write('''
In questa pagina puoi vedere la serie storica, da quando hai creato l'account spotify a quando hai scaricato i dati, con periodicità mensile.
''')
    st.subheader("Serie storica artisti")
    st.write('''
In questa pagina puoi vedere la serie storica suddivisa per artisti, da quando hai creato l'account spotify a quando hai scaricato i dati, con periodicità mensile. Vi è anceh la possibilità di confrontare le serie storiche di diversi artisti fino ad un massimo di 10.
''')
    st.subheader("Shuffle?")
    st.write('''
In queswta pagina puoi vedere un riassunto del tuo utilizzo della funzione shuffle.
''')
    st.subheader("Giornata tipo")
    st.write('''
In questa pagina puoi vedere come gli ascolti sono distribuiti nell'arco di una giornata
''')
    st.subheader("Generi musicali")
    st.write('''
In questa pagina puoi vedere la top 10, in percentuale, dei tuoi generi musicali più ascoltati in un periodo di tempo determinato.
''')
    st.subheader("HeetMap")
    st.write('''
In questa pagina puoi vedere la Heet Map realztiva agli ascolti giornalieri relativi ad un anno specifico.
''')
    st.subheader("Scopri artisti")
    st.write('''
In questa pagina puoi scoprire nuovi artisti e avere informazioni a riguardo.
''')
    st.subheader("Scopri brani")
    st.write('''
In questa pagina puoi scoprire nuovi brani e avere informazioni a riguardo.
''')
    st.subheader("Scarica playlist")
    st.write('''
In questa pagina puoi vedere tutte le playlist presenti nel tuo profilo e decidere di scaricarle. Le canzoni scaricate le puoi ritrovare nella cartella 'DOWNLOAD'.
''')
    st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f5f5f5;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
        border-top: 1px solid #ddd;
    }
    </style>
    <div class="footer">
    Creato con ❤️ da <b>Marco Badiello</b>
    </div>
    """,
    unsafe_allow_html=True
)

