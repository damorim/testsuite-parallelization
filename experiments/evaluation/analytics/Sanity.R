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
  df_l0 <- df[df$mode == ref, ]
  df_st <- df[df$mode == other, ]
  subjects_inspect = character()
  deltas <- double()
  for (subject in df_l0$name) {
    t_l0 <- df_l0[df_l0$name == subject, ]$elapsed_t
    t_st <- df_st[df_st$name == subject, ]$elapsed_t
    delta <- abs(t_l0 - t_st)
    if (delta >= threshold) {
      subjects_inspect <- c(subject, subjects_inspect)
      deltas <- c(delta, deltas)
    }
  }
  deltas <- sapply(deltas, FUN = function(t) {return(t / 60)})

}
args <- commandArgs(trailingOnly = TRUE)
name <- args[1]
df <- read.csv(name)

flaky_subjects <- check_test_flakiness(df)
if (length(flaky_subjects) != 0) {
  print("Flaky Subjects:")
  for (subj in flaky_subjects) {
    print(df[df$name == subj, c(-8:-10)])
  }
}

compare_tcost_modes(df, ref="L0", other="ST", threshold=60)
