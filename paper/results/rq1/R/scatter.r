args <- commandArgs(trailingOnly = TRUE)

out_name <- args[5]
pdf(paste(out_name,".pdf",sep=""), height=4.5)

input_file <- args[1]
type <- args[2]

max_y <- as.numeric(args[3])
max_x <- as.numeric(args[4])

print(max_x)

data <- read.csv(input_file, sep=",", header=T)

values = subset(data, group == type)
plot(values$elapsed_t, values$tests,
     frame.plot=F,
     pch=4,
     xlab="Elapsed time (in secs)",
     ylab="# of tests",
     xlim=c(50, max_x),
     ylim=c(1, max_y))

