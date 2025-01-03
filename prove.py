import wikipedia
wikipedia.set_lang("it") 
testo = wikipedia.summary("Puddle of mudd", sentences=10)
print(testo.split('=')[0])
