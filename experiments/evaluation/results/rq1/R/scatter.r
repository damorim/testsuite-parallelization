args <- commandArgs(trailingOnly = TRUE)

out_name <- args[2]
pdf(paste(out_name,".pdf",sep=""))

name <- args[1]
data <- read.table(name, header=T, sep=",")
plot(data$ELAPSED_T, data$TESTS,
     xlab="Elapsed time (in secs)",
     ylab="# of tests")
