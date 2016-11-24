compute_groups <- function(elapsed_times) {
  groups <- character()
  for (time in elapsed_times) {
    group <- NULL
    # Group 1: t <= 1 min
    if (time <= 60) {
      group <- "short"
    }
    # Group 2: 1 min < t <= 5 min
    else if (time <= (5 * 60)) {
      group <- "regular"
    }
    # Group 3: 5 min < t
    else {
      group <- "long"
    }
    groups <- c(groups, group)
  }
  return(groups)
}

rq1_timecost <- function(rawdata, plot_path) {
  pdf(plot_path, height = 3.5, width = 5)
  
  # plot layout
  par(
    mfrow = c(1, 3),
    # plot matrix
    mar = c(1, 1, 1, 1),
    # margin
    oma = c(0, 0, 0, 0),
    # outer margin
    xpd = T
  )
  modes <- c("L0", "ST")
  main_pies <- c("Sequential", "Standard")
  for (i in 1:2) {
    mode <- modes[i]
    df <- rawdata[rawdata$mode == mode,]
    groups <- compute_groups(df$elapsed_time)
    groups_distribution <- as.data.frame(table(groups))
    frequencies <- groups_distribution$Freq
    sum_freq <- sum(frequencies)

    print(paste("DEBUG: mode=", mode, " total=", sum_freq, sep = ""))
    print(groups_distribution)

    perct_values <- round(frequencies / sum_freq * 100)
    pie(
      frequencies,
      radius = 0.8,
      labels = paste(perct_values, "%", sep = ""),
      col = c("gray30", "gray50", "gray90")
    )

    # bring pie title down
    title(main_pies[i], line = -6)
  }

  # plot legend
  plot.new()
  legend(
    "topleft",
    inset = c(0, 0.35),
    c("long", "regular", "short"),
    fill = c("gray30", "gray50", "gray90")
  )
}

rq1_tests_time <- function(rawdata, plot_path) {
  mode <- "L0"
  column_filter <- c("name", "elapsed_time", "r_tests")
  df <- rawdata[rawdata$mode == mode, column_filter]

  # eliminates some unnecessary points
  df <- df[df$r_tests <= 10000, ]

  # Convert seconds to minutes
  minutes <- double()
  for (t in df$elapsed_time) {
    minutes <- c(minutes, (t / 60))
  }
  print(paste("DEBUG: mode=", mode, " N=", length(df$name), sep = ""))
  print(df[order(df[, 2]), ])

  pdf(plot_path)
  plot(
    y = minutes,
    x = df$r_tests,
    ylab = "Elapsed Time (min)",
    xlab = "# of Tests",
    pch = 16 # changes dot type
  )
}

name <- "rawdata.csv"
rawdata <- read.csv(name)

rq1_timecost(rawdata, "plots/piechart-timecost.pdf")
rq1_tests_time(rawdata, "plots/scatter-tests-time.pdf")

print(paste("Experiment cost:",
            round(sum(
              rawdata$elapsed_time
            )) / 3600, "hr"))
