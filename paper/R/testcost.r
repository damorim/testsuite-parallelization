library(ggplot2)

pdf(file = "testcost.pdf", width = 5, height = 2.5)

dat <- read.csv("testcost.csv", header = F) 

p <- ggplot(dat, aes(x=factor(V1), y=V2))

p + geom_boxplot() +
theme(axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank()
) +
labs(y="Time (s)")

aux <- dev.off()