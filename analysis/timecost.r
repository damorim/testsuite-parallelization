library("dplyr")
library("ggplot2")

# df <- read.csv(file.choose())
args <- commandArgs(trailingOnly = TRUE)
rq1_df <- read.csv(args[1])
#rq2_df <- read.csv(args[2], sep = ";")
#rq3_df <- read.csv(args[3], sep = ",")

###################
# Analysis
###################

summarise(
  group_by(rq1_df, test_success),
  n = length(project_path),
  tmin_xml = min(xml_test_time),
  tmax_xml = max(xml_test_time),
  tmin_mvn = min(maven_test_time),
  tmax_mvn = max(maven_test_time)
)

###################
# RQ1
###################
print("Investigate: Build success but builder time = 0")
select(filter(rq1_df, test_success == "true" &
                maven_test_time <= 0),
       project_path)
print("Investigate: build success but xml time = 0")
select(filter(rq1_df, test_success == "true" &
                xml_test_time <= 0),
       project_path)

rq1_df$tmin <- sapply(rq1_df$xml_test_time, FUN = function(v) {return(v / 60)})
rq1_df <- filter(rq1_df, xml_test_time > 0)

# Cost groups barplot
pdf("out/barplot-timecost.pdf", height = 3, width = 3)
ggplot(data = rq1_df, aes(x = timecost_group, fill = test_success)) +
  geom_bar(width = .8, position = "dodge", colour = "black") +
  geom_text(
    size = 3,
    position = position_dodge(width = .75),
    stat = "count",
    aes(label = ..count.. , y = ..count.. + 8)
  ) +
  scale_fill_brewer(labels = c("tests fail", "tests pass")) +
  theme(legend.background = element_rect(),
        legend.margin = margin(0),
        legend.position = "top",
        legend.title = element_blank()) +
  labs(y = "Frequency", x = "Group")

# Time cost boxplots
pdf("out/boxplot-timecost.pdf", height = 3, width = 3)
ggplot(data = rq1_df, aes(x = timecost_group, y = tmin, fill = test_success)) +
  geom_boxplot() +  theme(strip.text = element_blank(),
                          strip.background = element_blank(),
                          legend.background = element_rect(),
                          legend.margin = margin(0),
                          legend.title = element_blank(),
                          legend.position = "top") +
  scale_fill_brewer(labels = c("tests fail", "tests pass")) +
  facet_wrap( ~ timecost_group, scales = "free") +
  labs(y = "Time cost (in minutes)", x = "Group")
