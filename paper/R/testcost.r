library(ggplot2)

pdf(file = "testcost-long.pdf", width = 5, height = 2)
dat <- read.csv("testcost-long.csv", header = F) 
p <- ggplot(dat[dat$V2>1,], aes(x=factor(V1), y=V2))
p + geom_boxplot(outlier.shape=NA) +
theme(axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank()
) +
labs(y="Time (s)")+
coord_cartesian(ylim = c(1,150))

aux <- dev.off()

pdf(file = "testcost-med.pdf", width = 5, height = 2)
dat <- read.csv("testcost-med.csv", header = F) 
p <- ggplot(dat[dat$V2>1,], aes(x=factor(V1), y=V2))
p + geom_boxplot(outlier.shape=NA) +
theme(axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank()
) +
labs(y="Time (s)") +
coord_cartesian(ylim = c(1,90))

p <- ggplot(dat, aes(x=factor(V1), y=V2), outlier.shape=NA)
aux <- dev.off()
