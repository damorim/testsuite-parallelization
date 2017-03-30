library(ggplot2)

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  name = args[1]
}

# ## coefficient of variation function
# co.var <- function(x,na.rm=TRUE) sd(x,na.rm=na.rm)/mean(x,na.rm=na.rm)

output <- paste("out", name, sep="/")
pdf(file=paste(output,".pdf",sep=""), width = 5, height = 1.5)

input <- paste("gen", name, sep="/")
dat <- read.csv(paste(input,".csv",sep=""), header = T)

# to compute median values across plots
median <- aggregate(dat$time, list(dat$project), median)
print("==sd==>")
sd <- aggregate(dat$time, list(dat$project), sd)
print(sd)
 
ggplot(dat, aes(x=factor(project), y=time)) +
    geom_boxplot(outlier.shape=NA) +
    theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
    labs(y="Time cost (in secs)")+
    geom_hline(aes(yintercept=mean(median$x)), colour = "red", linetype = 2)+
    coord_cartesian(ylim = c(0,7.5))
 
aux <- dev.off()

