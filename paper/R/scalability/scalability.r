pdf(file = "scalability.pdf", width = 7, height = 4)

dataframe <- read.csv(file="scalability.data", header=TRUE, sep=",")

boxplot(time~numcores, data=dataframe, ylab="time (m)", xlab="# cores", ylim=c(0,max(dataframe$time)), cex.lab=1.8, cex.axis=1.8)

aux <- dev.off()