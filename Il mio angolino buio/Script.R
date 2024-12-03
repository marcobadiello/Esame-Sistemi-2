#Script R per il progetto di Sistemi di elaborazione 2
setwd("C:\\Users\\Marco\\Desktop\\Esame-Sistemi-2")
getwd()
library(ggplot2)
################################################################################
#DEFINIZIONE DI FUNZIONI
################################################################################
#funzione per creare dummy stagionali
# Crea una cartella se non esiste
if (!dir.exists("output")) {
  dir.create("output")
}






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
n = dim(data)[1]
primo_periodo = data$month[1]
primo_periodo
primo_anno = data$year[1]
primo_anno

# Funzione corretta per modellare con un polinomio di grado specifico
modello_polinomiale <- function(y, grado, primo_periodo, primo_anno) {
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
  
  # Calcolo delle etichette degli anni
  anni <- primo_anno + (seq(primo_periodo, n + primo_periodo - 1, by = 12) - 1) %/% 12 + 1
  ticks <- seq(13 - primo_periodo, n, by = 12) # Posizione dei mesi di gennaio
  labels <- anni
  
  # Grafico
  png("output/grafico_modello.png", width = 800, height = 600)
  plot(tempo, y, type = "l", xlab = "Anni", xaxt = "n", main = paste("Polinomio di grado", grado), ylab = "Ore ascoltate")
  axis(1, at = ticks, labels = labels) # Aggiungi etichette degli anni
  lines(tempo, modello$fitted.values, col = "red", lwd = 2)
  dev.off()
  
  # Grafico senza salvare
  plot(tempo, y, type = "l", xlab = "Anni", xaxt = "n", main = paste("Polinomio di grado", grado), ylab = "Ore ascoltate")
  axis(1, at = ticks, labels = labels)
  lines(tempo, modello$fitted.values, col = "red", lwd = 2)
  
  # Restituzione del modello
  return(modello)
}




fit <- modello_polinomiale(y, grado = 4,primo_periodo, primo_anno) # Modello con polinomio di grado 2
saveRDS(fit, "modello_polinomiale.rds")


dv=make.dummy(n=n, freq=12, start=primo_periodo)
dv

# Stimo il modello con 4 dummy senza intercetta

fit.stag=lm(y~-1+dv[,1]+dv[,2]+dv[,3]+dv[,4]+dv[,5]+dv[,6]+dv[,7]+dv[,8]+dv[,9]+dv[,10]+dv[,11]+dv[,12])
summary(fit.stag)  # Le stime sono le medie di y nei 4 trimestri

plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(fit.stag$fitted, col="red")
plot(fit.stag$resid,type="l", xlab="t", xaxp=c(0,36,9))
abline(h=0,lty=2)

# Coefficienti grezzi di stagionalità
gamma.star=fit.stag$coef
gamma.star
gamma.bar=mean(gamma.star)
gamma.bar # media non nulla

# Coefficienti ideali di stagionalità
gamma=gamma.star-gamma.bar
gamma

# destagionalizzazione
dvideali=dv%*%gamma  # prodotto matriciale fra dummy e coeff.ideali
dvideali
yd=y-dvideali
yd

plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(yd, col="red")
plot(dvideali,type="l", xlab="t", xaxp=c(0,36,9))
abline(h=0,lty=2)





tempo = seq(1,n,1)
tempo2 = tempo^2
tempo3 = tempo^3
tempo4 = tempo^4



## Stima simultanea di trend (grado 2) e stagionalità
fit.sim2=lm(y~-1+tempo+tempo2+dv[,1]+dv[,2]+dv[,3]+dv[,4]+dv[,5]+dv[,6]+dv[,7]+dv[,8]+dv[,9]+dv[,10]+dv[,11]+dv[,12])
summary(fit.sim2)  # le dummy sono intercette diverse per ogni stagione

plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(fit.sim2$fitted, col="red")
plot(fit.sim2$res,type="l", xlab="t", xaxp=c(0,36,9))
abline(h=0,lty=2)

## Stima simultanea di trend (grado 4) e stagionalità
fit.sim4=lm(y~-1+tempo+tempo2+tempo3+tempo4+dv[,1]+dv[,2]+dv[,3]+dv[,4]+dv[,5]+dv[,6]+dv[,7]+dv[,8]+dv[,9]+dv[,10]+dv[,11]+dv[,12])
summary(fit.sim4)

plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(fit.sim4$fitted, col="red")
plot(fit.sim4$res,type="l", xlab="t", xaxp=c(0,36,9))
abline(h=0,lty=2)


## Confronto tra modelli
plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(fit.sim2$fitted, col="red")
plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(fit.sim4$fitted, col="red")

plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(fit.sim2$fitted, col="red")
lines(fit.sim4$fitted, col="blue")
plot(fit.sim2$resid, type="l",xlab="t", xaxp=c(0,36,9), col="red")
lines(fit.sim4$resid, col="blue")
abline(h=0,lty=2)


# Coefficienti grezzi di stagionalità (grado 2, provare anche grado 4)
gamma.star2=fit.sim2$coef[3:6]
gamma.star2
gamma.bar2=mean(gamma.star2)
gamma.bar2 

# Coefficienti ideali di stagionalità
gamma2=gamma.star2-gamma.bar2
gamma2

# destagionalizzazione
dvideali2=dv%*%gamma2
dvideali2
yd2=y-dvideali2
yd2

plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(yd2, col="red")
plot(dvideali2,type="l", xlab="t", xaxp=c(0,36,9))
abline(h=0,lty=2)

plot(y,type="l", xlab="t", xaxp=c(0,36,9))
lines(yd2, col="red")
lines(yd, col="blue")
plot(dvideali2,type="l", xlab="t", xaxp=c(0,36,9), col="red")
lines(dvideali, col="blue", xlab="t")
abline(h=0,lty=2)

