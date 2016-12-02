check_aborts <- function(df) {
  print("Aborted Subjects:")
  inspect = character()
  for (n in unique(df$name)) {
    tests <- (df[df$name == n, "r_tests"])
    if (min(tests) != max(tests)) {
      inspect <- c(inspect, n)
    }
  }
  return(inspect)
}

compare_tcost_modes <- function(df, ref, other, threshold) {
  print(paste("Checking deltas (threshold=", threshold, "):", sep=""))
  df_ref <- df[df$mode == ref, ]
  df_other <- df[df$mode == other, ]
  name <- df_ref$name
  r_df <- data.frame(name)
  r_df$delta <- abs(df_ref$elapsed_time - df_other$elapsed_time) 
  return(r_df[r_df$delta >= threshold,])
}

args <- commandArgs(trailingOnly = TRUE)
name <- args[1]

df <- read.csv(name)
print(paste("Total subjects:", length(unique(df$name))))
check_aborts(df)
compare_tcost_modes(df, ref="L0", other="Standard", threshold=60)