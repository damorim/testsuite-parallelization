args <- commandArgs(trailingOnly = TRUE)

out_name <- args[2]
    pdf(paste(out_name,".pdf",sep=""), height=4)

name <- args[1]
data <- read.csv(name, sep=",", header=T)

dist <- as.data.frame(table(data$group))

slices <- dist$Freq
pct <- round(slices / sum(slices) * 100)
lbls <- paste(pct, "%", sep="")
colors <- c("gray10", "gray30", "gray80", "white")

pie(slices, radius=0.8, labels=lbls, col=colors)
legend_lbls <- names(table(dist$Var1))
legend("topright", legend_lbls, fill=colors, cex=0.8)

