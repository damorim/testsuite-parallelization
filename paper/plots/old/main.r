library("dplyr")
library("ggplot2")

TO_PDF <- T

plot_timecost <- function(df) {
  # Cost groups barplot
  if (TO_PDF) {
    pdf("barplot-timecost.pdf",
        height = 3,
        width = 2.3)
  }
  ggplot(data = df, aes(x = group, fill = test_success)) +
    geom_bar(width = .8, position = "dodge") +
    geom_text(
      position = position_dodge(width = .75),
      stat = "count",
      aes(label = ..count.. , y = ..count.. + 5)
    ) +
    labs(y = "Frequency", x = "Group")
  
  # Time cost boxplots
  if (TO_PDF) {
    pdf("boxplot-timecost.pdf",
        height = 3,
        width = 2.7)
  }
  ggplot(data = df, aes(x = group, y = tmin, fill = test_success)) +
    geom_boxplot() +  theme(strip.text = element_blank(),
                            strip.background = element_blank()) +
    facet_wrap( ~ group, scales = "free") +
    labs(y = "Time cost (in minutes)", x = "Group")
}

# df <- read.csv(file.choose())
df <- read.csv("dataset.csv")

summarise(
  group_by(df, test_success),
  n = length(project_path),
  tmin_xml = min(xml_test_time),
  tmax_xml = max(xml_test_time),
  tmin_mvn = min(maven_test_time),
  tmax_mvn = max(maven_test_time)
)

print("Investigate: Build success but builder time = 0")
select(filter(df, test_success == "true" &
                maven_test_time <= 0),
       project_path)
print("Investigate: build success but xml time = 0")
count(select(
  filter(df, test_success == "true" &
           xml_test_time <= 0),
  project_path
))

df <- df %>% mutate(tmin = round(xml_test_time / 60, 2),
                    group = sapply(xml_test_time, function(v) {
                      if (v < 60) {
                        return("short")
                      }
                      else if (v < 5 * 60) {
                        return("medium")
                      }
                      return("long")
                    }))

plot_timecost(filter(df, xml_test_time > 0))

#ggplot(data = df, aes(x = overhead_time)) +
#  geom_histogram(fill = "black", binwidth = 5) +
#  geom_vline(xintercept = 60, colour = "red") +
#  geom_vline(xintercept = 0, colour = "blue") +
#  theme_bw() +
#  theme(
#    panel.border = element_blank(),
#    axis.text.y = element_blank(),
#    axis.ticks.y = element_blank()
#  ) +
#  # geom_text(size = 2.5, stat = "count", aes(label = paste(round(
#  #   ..count.. / sum(..count..) * 100, 1
#  # ), "%"), y = ..count.. / 2)) +
#  # geom_text(size = 2.8, stat = "count", aes(label = ..count.., y = ..count.. + 10)) +
#  labs(y = "Frequency", x = "Overhead")
#
# temp <- df[df$overhead < 0,]
# temp$speedup <- round(temp$xml_test_time / temp$maven_test_time, 2)
#
# pdf("histo-speedup", height = 3, width = 2.3)
# ggplot(data = temp, aes(x = speedup)) + geom_histogram()
