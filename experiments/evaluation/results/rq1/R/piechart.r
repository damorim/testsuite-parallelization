args <- commandArgs(trailingOnly = TRUE)

out_name <- args[2]
pdf(paste(out_name,".pdf",sep=""))

name <- args[1]
data <- read.csv(name, sep=",", header=T)

dist <- as.data.frame(table(data$group))

slices <- dist$Freq
pct <- round(slices / sum(slices) * 100)
lbls <- paste(pct, "%", sep="")
colors <- c("gray10", "gray40", "gray80", "gray100")

pie(slices, labels=lbls, col=colors)
legend_lbls <- c("label", "label", "label", "label")
legend("topright", legend_lbls, fill=colors)

