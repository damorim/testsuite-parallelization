library("plyr")

args <- commandArgs(trailingOnly = TRUE)

out_name <- args[2]
pdf(paste(out_name,".pdf",sep=""))

name <- args[1]
data <- read.csv(name, sep=",", header=T)

dist <- count(data, "group")

values <- dist$freq

# TODO
pie(values)
