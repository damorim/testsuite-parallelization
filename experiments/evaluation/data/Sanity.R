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

df <- read.csv("rawdata.csv")
flaky_subjects <- check_test_flakiness(df)

if (length(flaky_subjects) != 0) {
  print("Flaky Subjects:")
  print(flaky_subjects)
}
# TODO check elapsed time!
