compute_group <- function(time) {
  if (time <= 60) {
    return("short")
  }
  else if (time <= (5 * 60)) {
    return("medium")
  }
  return("long")
}

rq1_timecost <- function(rawdata, plot_path) {
  pdf(plot_path, height = 3.5, width = 5)
  
  # plot layout
  par(
    mfrow = c(1, 3),
    mar = c(1, 1, 1, 1),
    oma = c(0, 0, 0, 0),
    xpd = T
  )
  modes <- c("L0", "Standard")
  main_pies <- c("Sequential", "Standard")
  cols <- c("gray30", "gray50", "gray90")
  for (i in 1:2) {
    mode <- modes[i]
    df <- rawdata[rawdata$mode == mode, ]
    groups_distribution <- as.data.frame(table(df$groups))
    frequencies <- groups_distribution$Freq
    sum_freq <- sum(frequencies)
    
    print(paste("DEBUG: mode=", mode, " total=", sum_freq, sep = ""))
    print(groups_distribution)
    percents = sapply(frequencies, function(v) {
      return(round(v / sum_freq * 100, 1))
    })
    pie(
      frequencies,
      radius = 0.8,
      labels = sapply(percents, function(v) {
        return(paste(v, "%", sep = ""))
      }),
      col = cols
    )
    # bring pie title down
    title(main_pies[i], line = -6)
  }
  # plot legend
  plot.new()
  legend(
    "topleft",
    inset = c(0, 0.35),
    c("long", "medium", "short"),
    fill = cols
  )
}

rq1_tests_time <- function(rawdata, plot_path) {
  pdf(plot_path)
  par(mfrow = c(2, 1))
  df <-
    rawdata[rawdata$mode == "Standard" & rawdata$r_tests < 10000, ]
  types <- c("Medium", "Long")
  for (i in 1:2) {
    plot(
      y = df[df$groups == tolower(types[i]), c("minutes")],
      x = df[df$groups == tolower(types[i]), c("r_tests")],
      ylab = "Elapsed Time (min)",
      xlab = "# of Tests",
      main = types[i],
      pch = 16 # changes dot type
    )
  }
}

rq2_prevalence <- function(df, output) {
  print(df)
}

args <- commandArgs(trailingOnly = TRUE)
rawdata <- read.csv(args[1])
parprev <- read.csv(args[2])
output <- args[3]
# rawdata <- read.csv("../results/dataset-execution-1612031032.csv")
# parprev <- read.csv("../results/dataset-parprev-1612031032.csv")
# output <- "plots"

rawdata$minutes <- sapply(rawdata$elapsed_time, function(v) {
  return(v / 60)
})
rawdata$groups <- sapply(rawdata$elapsed_time, FUN = compute_group)
parprev$groups <-
  sapply(
    parprev$name,
    FUN = function(v) {
      return(rawdata[rawdata$mode == "Standard" &
                       rawdata$name == v, c("groups")])
    }
  )

rq1_timecost(rawdata, paste(output, "piechart-timecost.pdf", sep = "/"))
rq1_tests_time(rawdata, paste(output, "scatter-tests-time.pdf", sep = "/"))
rq2_prevalence(parprev, paste(output, "barplot-parprev.pdf", sep = "/"))
# print(paste("Experiment cost:",
#             round(sum(
#               rawdata$elapsed_time
#             )) / 3600, "hr"))
