args <- commandArgs(trailingOnly = TRUE)

pdf(paste("timecost-barplot",".pdf",sep=""),
    width=3,
    height=5)

name <- args[1]
data <- read.table(name, header=F)
barplot(table(data),
        ylab="Frequency",
        xlab="Elapsed time groups")

