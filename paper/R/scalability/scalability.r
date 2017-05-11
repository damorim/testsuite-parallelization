pdf(file = "scalability.pdf", width = 5, height = 3)

dataframe <- read.csv(file="scalability.data", header=TRUE, sep=",")

boxplot(time~numcores, data=dataframe, ylab="Time (m)", xlab="# Cores", ylim=c(0,max(dataframe$time)))

aux <- dev.off()