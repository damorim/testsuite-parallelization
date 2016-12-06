which_group <- function(time) {
  if (time <= 60) {
    return("short")
  }
  else if (time <= (5 * 60)) {
    return("medium")
  }
  return("long")
}
file_input <- "../results/dataset-execution-1612051140.csv"

ds <- read.csv(file_input)
ds <- ds[ds$mode == "Standard",]

# Total cost for Standard execution
cost_secs <- sum(ds[, "elapsed_time"])
print(paste("Total cost in std mode (hours):", cost_secs / 3600))

# Classify subjects according elapsed time
ds$group <- sapply(ds$elapsed_time, FUN = which_group)
table(ds$group)
