library(ggplot2)

pdf(file = "testcost-long.pdf", width = 5, height = 2)
dat <- read.csv("testcost-long.csv", header = F) 
p <- ggplot(dat[dat$V2<10,], aes(x=factor(V1), y=V2))
p + geom_boxplot() +
theme(axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank()
) +
labs(y="Time (s)")

aux <- dev.off()

pdf(file = "testcost-med.pdf", width = 5, height = 2)
dat <- read.csv("testcost-med.csv", header = F) 
p <- ggplot(dat[dat$V2<10,], aes(x=factor(V1), y=V2))
p + geom_boxplot() +
theme(axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank()
) +
labs(y="Time (s)")

aux <- dev.off()
