#!/usr/bin/env Rscript

library(ggplot2)

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  name = args[1]
}

pdf(file=paste(name,".pdf",sep=""), width = 5, height = 2)

dat <- read.csv(paste(name,".csv",sep=""), header = F)

## to compute mean across plots
datasel <- aggregate(dat[, 2:2], list(dat$V1), mean)

p <- ggplot(dat[dat$V2>1,], aes(x=factor(V1), y=V2))

p + geom_boxplot(outlier.shape=NA) +
theme(axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank()
) +
labs(y="Time (s)")+
geom_hline(aes(yintercept=mean(datasel$x, linetype = 2, colour = "red")))+
coord_cartesian(ylim = c(1,25))

aux <- dev.off()


