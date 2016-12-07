which_group <- function(time) {
  if (time <= 60) {
    return("short")
  }
  else if (time <= (5 * 60)) {
    return("medium")
  }
  return("long")
}

piechart_timecost <- function(rawdata) {
  # plot layout
  par(
    mfrow = c(1, 2),
    mar = c(1, 1, 1, 1),
    oma = c(0, 0, 0, 0),
    xpd = T
  )
  cols <- c("gray30", "gray50", "gray90")

  df <- rawdata[rawdata$mode == "Standard", ]
  groups_distribution <- as.data.frame(table(df$group))
  frequencies <- groups_distribution$Freq
  sum_freq <- sum(frequencies)

  percents = sapply(frequencies, function(v) {
    return(round(v / sum_freq * 100, 1))
  })
  pie(
    frequencies,
    radius = 0.8,
    main = "Distribution of execution cost",
    labels = sapply(percents, function(v) {
      return(paste(v, "%", sep = ""))
    }),
    col = cols
  )
  # bring pie title down
  # title(main_pies[i], line = -6)

  # plot legend
  plot.new()
  legend(
    "topleft",
    inset = c(0, 0.35),
    c("long", "medium", "short"),
    fill = cols
  )
}

file_input <- "../results/dataset-execution-1612061818.csv"

ds <- read.csv(file_input)
ds <- ds[ds$mode == "Standard",]
ds$minutes <- sapply(ds$elapsed_time, function(v) {
  return(v / 60)
})

# Classify subjects according elapsed time
ds$group <- sapply(ds$elapsed_time, FUN = which_group)
table(ds$group)

piechart_timecost(ds)
temp <- ds[ds$group == "long" & ds$minutes <= 60,]
boxplot(temp$minutes ~ temp$group, data = temp)


# Total cost for Standard execution
print(paste("[ALL]    Total cost in std mode (hours):", round(sum(ds[, "elapsed_time"]) / 3600, 2)))
print(paste("[LONG]   Total cost in std mode (hours):", round(sum(ds[ds$group == "long", "elapsed_time"]) / 3600, 2)))
print(paste("[MEDIUM] Total cost in std mode (hours):", round(sum(ds[ds$group == "medium", "elapsed_time"]) / 3600, 2)))
print(paste("[SHORT]  Total cost in std mode (hours):", round(sum(ds[ds$group == "short", "elapsed_time"]) / 3600, 2)))
