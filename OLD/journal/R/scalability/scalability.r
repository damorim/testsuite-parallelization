library("ggplot2")
library("grDevices")

cairo_pdf(file = "scalability.pdf", width = 3, height = 1.5)
dataframe <- read.csv(file="scalability_reduced.data", header=TRUE, sep=",")

#boxplot(time~numcores, data=dataframe, ylab="time (m)", xlab="# cores", ylim=c(0,max(dataframe$time)+1), cex.lab=1.8, cex.axis=1.6)
ggplot(dataframe, aes(numcores, time, group = numcores)) +
  geom_boxplot(outlier.shape = NA) +
  theme_bw() +
  scale_x_continuous(breaks = dataframe$numcores, labels = dataframe$numcores) +
  labs(x = "# cores", y = "Time (m)")

aux <- dev.off()
