import streamlit as st
from Estrattore import df

''''
In qeusto file è contenuto il codice per la schermata HOME del progetto
'''

# creo una funzione che avvia la schermata
def run_home():

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
        
    st.subheader("Come è stato ottenuto il dataset")
    stringhetta = '''
    Il dataset è stato ottenuto mediante una richiesta di dawnload di tutto lo storico 
    delle mie stream a Spotify. I file ottenuti a seguito della richiesta sono più file di tipo 
    .json i queli sono stati letti, analizzati e 
    trasformati in un dataset polars attraverso opportune analisi. Successivamente i dati sono
    stati ripuliti da tutte le 
    varibili non utili ai fini del progetto e dai dati relativi agli ascolti di podcast 
    poichè in questo progetto si procede ad analizzare solo i dati sulla musica. 
    '''
    st.write(stringhetta)
    
    st.markdown("---")
    st.title("📒Le pagine")
    st.subheader("TOP Canzoni")
    st.write('''
In questa pagina puoi vedere una classifica di tutte le canzoni ascoltate in un determinato periodo.
''')
    st.subheader("TOP Artisti")
    st.write('''
In questa pagina puoi vedere una classifica di tutti gli artisti ascoltati in un determinato periodo.
''')
    st.subheader("Serie storica")
    st.write('''
In questa pagina puoi vedere la serie storica di tutti gli ascolti con periodo mensile.
''')
    st.subheader("Serie storica artisti")
    st.write('''
In questa pagina puoi vedere la serie storica degli ascolti con periodo mensile
             e dividerla per artisti.
''')
    st.subheader("Shuffle?")
    st.write('''
In queswta pagina puoi vedere un riassunto dell'utilizzo della funzione Shuffle.
''')
    st.subheader("Giornata tipo")
    st.write('''
In questa pagina puoi vedere come gli ascolti sono distribuiti nell'arco di una giornata
''')