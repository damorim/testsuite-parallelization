args <- commandArgs(trailingOnly = TRUE)

out_name <- args[3]
pdf(paste(out_name,".pdf",sep=""))

input_file <- args[1]
type <- args[2]
data <- read.csv(input_file, sep=",", header=T)

values = subset(data, group == type)
plot(values$elapsed_t, values$tests,
     xlab="Elapsed time (in secs)",
     ylab="# of tests")
