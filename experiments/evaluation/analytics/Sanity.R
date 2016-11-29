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
check_elapsed_time <- function(df) {
  df_l0 <- df[df$mode == "L0", ]
  df_st <- df[df$mode == "ST", ]
  subjects_inspect = character()
  deltas <- double()
  for (subject in df_l0$name) {
    t_l0 <- df_l0[df_l0$name == subject, ]$elapsed_t
    t_st <- df_st[df_st$name == subject, ]$elapsed_t
    delta <- abs(t_l0 - t_st)
    if (delta >= 60) {
      subjects_inspect <- c(subject, subjects_inspect)
      deltas <- c(delta, deltas)
    }
  }
  deltas <- sapply(deltas, FUN = function(t) {return(t / 60)})
  pdf("DEBUG-diff-L0_ST.pdf")
  p <- barplot(deltas, space = 0, border = NA, ylab = "delta (absolute value in minutes)")
  text(
    x = p,
    y = 0,
    labels = subjects_inspect,
    srt = 90,
    xpd = T
  )
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

check_elapsed_time(df)
