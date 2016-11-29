check_test_flakiness <- function(df) {
  flaky_subjects = character()
  r_fields <- c("r_skipped", "r_tests", "r_failures")
  for (name in unique(df$name)) {
    df_subject <- df[df$name == name, r_fields]
    for (i in 1:3) {
      col_values <- as.numeric(unlist(df_subject[i]))
      if (!isTRUE(all.equal(min(col_values), max(col_values)))) {
        flaky_subjects <- c(flaky_subjects, name)
        break
      }
    }
  }
  return(flaky_subjects)
}
compare_tcost_modes <- function(df, ref, other, threshold) {
  df_ref <- df[df$mode == ref, ]
  df_other <- df[df$mode == other, ]
  name <- df_ref$name
  r_df <- data.frame(name)
  r_df$delta <- abs(df_ref$elapsed_time - df_other$elapsed_time) 
  return(r_df[r_df$delta >= threshold,])
}
args <- commandArgs(trailingOnly = TRUE)
name <- args[1]
# name <- file.choose()
df <- read.csv(name)

flaky_subjects <- check_test_flakiness(df)
if (length(flaky_subjects) != 0) {
  print("Flaky Subjects:")
  for (subj in flaky_subjects) {
    print(df[df$name == subj, c(-8:-10)])
  }
}

compare_tcost_modes(df, ref="L0", other="ST", threshold=60)