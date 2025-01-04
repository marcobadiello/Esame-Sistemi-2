import streamlit as st
from Estrattore import df

''''
In qeusto file è contenuto il codice per la schermata HOME del progetto
'''

# creo una funzione che avvia la schermata
def run_home():
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
        - **reason_start**: Motivo per cui è iniziata la stream
        - **reason_end**: Motivo per cui è terminata la stream
        - **shuffle**: Variabile dicotomica. La stram era o non era n riproduzione casuale
        - **skipped**: Variabile dicotomica. La canzone è o non è stata skippata.
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
    