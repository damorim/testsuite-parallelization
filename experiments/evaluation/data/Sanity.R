check_test_flakiness <- function(df) {
  # check if test execution is consistent
  flaky_subjects = character()
  
  r_fields <- c("r_skipped", "r_tests", "r_failures")
  for (name in df$name) {
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
print("FLAKY SUBJECTS:")
print(check_test_flakiness(df))