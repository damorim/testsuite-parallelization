#!/usr/bin/env Rscript

library(ggplot2)
library(raster)

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  name = args[1]
}

# ## coefficient of variation function
# co.var <- function(x,na.rm=TRUE) sd(x,na.rm=na.rm)/mean(x,na.rm=na.rm)

pdf(file=paste(name,".pdf",sep=""), width = 5, height = 1.5)

dat <- read.csv(paste(name,".csv",sep=""), header = F)

## to compute median values across plots
median <- aggregate(dat[, 2:2], list(dat$V1), median)

print("==sd==>")
sd <- aggregate(dat[, 2:2], list(dat$V1), sd)
print(sd)

p <- ggplot(dat, aes(x=factor(V1), y=V2))

p + geom_boxplot(outlier.shape=NA) +
theme(axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank()
) +
labs(y="Time (s)")+
geom_hline(aes(yintercept=mean(median$x)), colour = "red", linetype = 2)+
coord_cartesian(ylim = c(0,7.5))

aux <- dev.off()


