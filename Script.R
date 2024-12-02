#Script R per il progetto di Sistemi di elaborazione 2
setwd("C:\\Users\\Utente\\Desktop\\Esame-Sistemi-2")
library(ggplot2)
################################################################################
#DEFINIZIONE DI FUNZIONI
################################################################################
#funzione per creare dummy stagionali
make.dummy <- function(n, freq=12, start=1)
{
  dv=matrix(0,nrow=n, ncol=freq)
  for (i in 1:freq)
    if (start==1) {dv[,i][seq(i,n,freq)]=1} 
  else if (i < start) {dv[,i][seq(i+1-start+freq,n,freq)]=1}
  else {dv[,i][seq(i+1-start,n,freq)]=1}
  return(dv)
}

################################################################################
#SCRIPT
################################################################################
#TIME SERIES
data = read.csv("dati.time.series")
y = (data$total_seconds_played)
y = y/(60*60)



# Funzione corretta per modellare con un polinomio di grado specifico
modello_polinomiale <- function(y, grado) {
  # Controllo dei parametri
  if (!is.numeric(y) || !is.vector(y)) stop("Il parametro 'y' deve essere un vettore numerico.")
  if (!is.numeric(grado) || grado < 0) stop("Il parametro 'grado' deve essere un numero intero non negativo.")
  
  # Creazione delle variabili temporali e dei polinomi
  n <- length(y)
  tempo <- seq(1, n, 1)
  
  # Creazione del dataset per il modello
  dati <- data.frame(y = y, tempo = tempo)

    for (g in 1:grado) {
    dati[[paste0("tempo", g)]] <- tempo^g
  }
  
  # Formula dinamica in base al grado scelto
  if (grado == 0) {
    formula <- as.formula("y ~ 1") # Modello con solo intercetta
  } else {
    formula <- as.formula(paste("y ~", paste(paste0("tempo", 1:grado), collapse = "+")))
  }
  
  # Adattamento del modello
  modello <- lm(formula, data = dati)
  
  
  # Grafico dei dati e valori stimati
  plot(y, type = "l", xlab = "t", xaxp = c(0, n, 9), main = paste("Polinomio di grado", grado),ylab="Ore ascoltate")
  lines(modello$fitted.values, col = "red", lwd = 2)
  
  # Restituzione del modello
  return(modello)
}


fit <- modello_polinomiale(y, grado = 3) # Modello con polinomio di grado 2
saveRDS(fit, "modello_polinomiale.rds")

