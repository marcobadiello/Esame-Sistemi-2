import streamlit as st
from Estrattore import df

def run_home():
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
    if st.button("Mostra dataframe"):
        st.write(df)
    st.subheader("Come è stato ottenuto il dataset")
    qwertyuiop = '''
    Il dataset è stato ottenuto mandando una richiesta di dawnload di tutto lo storico delle mie stream a Spotify. I file ottenuti erano più file .json i queli sono stati letti tutti e
    trasformati in un dataset polars attraverso il file Estrattore.py . Dopodichè sono stati ripuliti da varibili non utili ai fini del progetto e sono stati rimossi tutti gli ascolti relativi ai podcast 
    poichè in questo progetto si procede ad analizzare solo l'ascolto della musica. 
    '''
    st.write(qwertyuiop)
    st.markdown("---")
    st.subheader("📊Le analisi")
    st.subheader("Le classifiche")
    st.write("Nella sezione TOP si possono trovare le classifiche de:")
    st.markdown('''
        - **Canzoni**
        - **Artisti**
    ''')
    
import Tools
# Tools.stampa_ts(df)