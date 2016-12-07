which_group <- function(time) {
  if (time <= 60) {
    return("short")
  }
  else if (time <= (5 * 60)) {
    return("medium")
  }
  return("long")
}
file_input <- "../results/dataset-execution-1612061818.csv"

ds <- read.csv(file_input)
ds <- ds[ds$mode == "Standard",]

# Classify subjects according elapsed time
ds$group <- sapply(ds$elapsed_time, FUN = which_group)
table(ds$group)

# Total cost for Standard execution
print(paste("[ALL]    Total cost in std mode (hours):", round(sum(ds[, "elapsed_time"]) / 3600, 2)))
print(paste("[LONG]   Total cost in std mode (hours):", round(sum(ds[ds$group == "long", "elapsed_time"]) / 3600, 2)))
print(paste("[MEDIUM] Total cost in std mode (hours):", round(sum(ds[ds$group == "medium", "elapsed_time"]) / 3600, 2)))
print(paste("[SHORT]  Total cost in std mode (hours):", round(sum(ds[ds$group == "short", "elapsed_time"]) / 3600, 2)))
