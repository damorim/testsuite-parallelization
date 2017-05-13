pdf(file = "scalability.pdf", width = 7, height = 4)

dataframe <- read.csv(file="scalability_reduced.data", header=TRUE, sep=",")

boxplot(time~numcores, data=dataframe, ylab="time (m)", xlab="# cores", ylim=c(0,max(dataframe$time)+1), cex.lab=1.8, cex.axis=1.6)

aux <- dev.off()