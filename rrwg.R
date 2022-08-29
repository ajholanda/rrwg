df <- read.table("rrwg.dat", header=T)
n <- seq(1,nrow(df))
nboxes <- ncol(df)/2
if ((nboxes %% 2) == 1)
   nboxes <- nboxes + 1
par(mfrow=c(nboxes/2, 2),mar=c(0.5, 1, 0.1, 0.5))
for (i in seq(1, ncol(df), 2)) {
    plot(n,df[,i]/n, type="l", ylim=c(0,1), axes=F, frame.plot=F, lwd=1.5)
    axis(1,labels=F)
    axis(2,labels=F)
    lines(n, df[,i+1], type="l", col="red", lwd=1.5)
}
rm(list=ls())
