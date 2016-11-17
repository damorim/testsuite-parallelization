args <- commandArgs(trailingOnly = TRUE)

out_name <- args[2]
out_path <- paste(out_name,".pdf",sep="")
pdf(out_path, height=3.5, width=5)

name <- args[1]
data <- read.csv(name, sep=",", header=T)

dist <- as.data.frame(table(data$group))
colors <- c("gray30", "gray50", "gray90")

par(mfrow=c(1,3), mar=c(1,1,1,1), oma=c(0,0,0,0), xpd=T)

sequential_t <- dist$Freq
pct <- round(sequential_t / sum(sequential_t) * 100)
lbls <- paste(pct, "%", sep="")
pie(sequential_t, radius=0.8, labels=lbls, col=colors)

default_t <- dist$Freq
pct <- round(default_t / sum(default_t) * 100)
lbls <- paste(pct, "%", sep="")
pie(default_t, radius=0.8, labels=lbls, col=colors)

plot.new()
legend_lbls <- names(table(dist$Var1))
legend("topleft", inset=c(0, 0.35), legend_lbls, fill=colors)

