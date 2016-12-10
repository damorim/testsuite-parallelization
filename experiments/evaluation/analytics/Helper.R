which_group <- function(time) {
  if (time <= 60) {
    return("short")
  }
  else if (time <= (5 * 60)) {
    return("medium")
  }
  return("long")
}

piechart_timecost <- function(df) {
  cols <- c("gray30", "gray50", "gray90")
  groups_distribution <- as.data.frame(table(df$group))
  frequencies <- groups_distribution$Freq
  sum_freq <- sum(frequencies)
  percents = sapply(frequencies, function(v) {
    return(round(v / sum_freq * 100, 1))
  })
  pie(
    frequencies,
    radius = 0.5,
    col = cols,
    labels = sapply(percents, function(v) {
      return(paste(v, "%", sep = ""))
    })
  )
  # bring pie title down
  # title(main = "Distribution of Subject Groups", line = -3)
  legend(
    "topright",
    inset = c(0, 0.3),
    c("Long", "Medium", "Short"),
    fill = cols
  )
}

args <- commandArgs(trailingOnly = TRUE)
file_input <- args[1] 
output_dir <- args[2]

ds <- read.csv(file_input)
ds <- ds[ds$mode == "Standard",]
ds$minutes <- sapply(ds$elapsed_time, function(v) {
  return(v / 60)
})

# Classify subjects according elapsed time
ds$group <- sapply(ds$elapsed_time, FUN = which_group)
table(ds$group)

# BOX PLOTS - TIMECOST
output_name <- paste(output_dir, "boxplots-timecost.pdf", sep="/")
pdf(output_name, height = 3, width = 4)
par(mfrow = c(1, 3),
    mar = c(5, 5, 0, 0),
    las = 1)
temp <- ds[ds$group == "long",]
boxplot(
  temp$minutes ~ temp$group,
  data = temp,
  frame = F,
  outline = F,
  ylab = "Elapsed time (in minutes)"
)
title(xlab = "Long", line = 0)
temp <- ds[ds$group == "medium", ]
boxplot(temp$minutes ~ temp$group,
        data = temp,
        frame = F)
title(xlab = "Medium", line = 0)
temp <- ds[ds$group == "short", ]
boxplot(temp$minutes ~ temp$group,
        data = temp,
        frame = F)
title(xlab = "Short", line = 0)

output_name <- paste(output_dir, "piechart-timecost.pdf", sep="/")
pdf(output_name)
piechart_timecost(ds)

# Total cost for Standard execution
print(paste("[ALL]    Total cost in std mode (hours):", round(sum(ds[, "elapsed_time"]) / 3600, 2)))
print(paste("[LONG]   Total cost in std mode (hours):", round(sum(ds[ds$group == "long", "elapsed_time"]) / 3600, 2)))
print(paste("[MEDIUM] Total cost in std mode (hours):", round(sum(ds[ds$group == "medium", "elapsed_time"]) / 3600, 2)))
print(paste("[SHORT]  Total cost in std mode (hours):", round(sum(ds[ds$group == "short", "elapsed_time"]) / 3600, 2)))
