# this script plots the realizations obtained
# while considereing CYCLIC graphs
dt <- read.table("rrwg.dat", header=T)
t <- nrow(dt)
n <- seq(1,t)
nboxes <- ncol(dt)/2
if ((nboxes %% 2) == 1) nboxes <- nboxes + 1
par(mfrow=c(nboxes/2,2),mar=c(0.5,1,0.1,0.5))
for (i in seq(1,ncol(dt),2)) {
    plot.new()
    polygon(c(0,t,t,0),c(0,0,1,1),col="#f5f5f5",
            border=NA)
    par(new=T)
    plot(n,dt[,i],type="l",ylim=c(0,1),axes=F,
         frame.plot=F,lwd=2);
    axis(1,labels=F)
    axis(2,labels=F)
    abline(h=c(0.2,0.4,0.6,0.8), lty=3)
    lines(n,dt[,i+1], type="l", col="#a5a5f1", lwd=2);
}
rm(list=ls())
