library(ggplot2)

pdf(file = "relativeSD.pdf", width = 5, height = 1.5)

dat <- read.table("relativeSD.data", sep = "", header = TRUE) 

p <- ggplot(dat, aes(factor(dummy), RSD))

p +
geom_boxplot() +
coord_flip() +
theme(axis.title.y=element_blank(),
      axis.text.y=element_blank(),
      axis.ticks.y=element_blank()
)

aux <- dev.off()