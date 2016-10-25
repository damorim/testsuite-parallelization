args <- commandArgs(trailingOnly = TRUE)

out_name <- args[2]
pdf(paste(out_name,".pdf",sep=""))

name <- args[1]
data <- read.csv(name, sep=",", header=T)

# FIXME: this file was copied from RQ1 so it's necessary to adjust
# according to what we want in this plot
#
#barplot(table(data$group),
#        ylab="Frequency",
#        xlab="Elapsed time groups",
#        space=0)

