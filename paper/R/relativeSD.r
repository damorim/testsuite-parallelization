library(ggplot2)

pdf(file = "relativeSD.pdf", width = 5, height = 2.5)

dat <- read.csv("testcost.csv", header = T) 

p <- ggplot(dat, aes(x=", y=dat$V2))

p +
geom_boxplot() +
coord_flip() +
theme(axis.title.y=element_blank(),
      axis.text.y=element_blank(),
      axis.ticks.y=element_blank()
) +
labs(y="Relative Standard Deviation (RSD)")

aux <- dev.off()
