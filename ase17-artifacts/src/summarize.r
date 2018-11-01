library("dplyr")

# main
df <- read.csv("dataset-detailed.csv")

df <- df %>%
  group_by(name, compiled, tested, tests, suites, failures) %>%
    summarise(runs = length(xml_time),
              mvn_time_avg = mean(mvn_test_time),
              mvn_time_sd = sd(mvn_test_time),
              xml_time_avg = mean(xml_time),
              xml_time_sd = sd(xml_time))


# serialize data
df %>% write.csv(., file = "dataset-aggregated.csv", row.names = F)

