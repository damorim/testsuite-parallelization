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

rq1 <- function(rawdata, plot_path) {
  pdf(plot_path, height = 3.5, width = 5)
  
  # plot layout
  par(
    mfrow = c(1, 3),
    mar = c(1, 1, 1, 1),
    oma = c(0, 0, 0, 0),
    xpd = T
  )
  modes <- c("L0", "ST")
  main_pies <- c("Sequential", "Standard")
  for (i in 1:2) {
    mode <- modes[i]
    filtered_data <- rawdata[rawdata$mode == mode,]
    groups <- compute_groups(filtered_data$elapsed_time)
    groups_distribution <- as.data.frame(table(groups))
    frequencies <- groups_distribution$Freq
    sum_freq <- sum(frequencies)
    
    print(paste("DEBUG: mode=", mode, " total=", sum_freq,
                sep = ""))
    print(groups_distribution)
    pct <- round(frequencies / sum_freq * 100)
    lbls <- paste(pct, "%", sep = "")
    pie(
      frequencies,
      radius = 0.8,
      labels = lbls,
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

name <- "rawdata.csv"
rawdata <- read.csv(name)

rq1(rawdata, "plots/piechart-timecost.pdf")
