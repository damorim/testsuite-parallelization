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
compute_group <- function(time) {
    if (time <= 60) {
        return("short")
    }
    else if (time <= (5 * 60)) {
        return("medium")
    }
    return("long")
}


print("Investigate: Build success but builder time = 0")
select(filter(rq1_df, test_success == "true" &
                maven_test_time <= 0),
       project_path)
print("Investigate: build success but xml time = 0")
select(filter(rq1_df, test_success == "true" &
                xml_test_time <= 0),
       project_path)

rq1_df$group <- sapply(rq1_df$xml_test_time, FUN = compute_group)
rq1_df$tmin <- sapply(rq1_df$xml_test_time, FUN = function(v) {return(v / 60)})
rq1_df <- filter(rq1_df, xml_test_time > 0)

# Cost groups barplot
pdf("out/barplot-timecost.pdf", height = 3, width = 3)
ggplot(data = rq1_df, aes(x = group, fill = test_success)) +
  geom_bar(width = .8, position = "dodge") +
  geom_text(
    size = 2.5,
    position = position_dodge(width = .75),
    stat = "count",
    aes(label = ..count.. , y = ..count.. + 5)
  ) +
  scale_fill_grey(start = 0.4, end = 0.7, labels = c("tests fail", "tests pass")) +
  theme(legend.background = element_rect(),
        legend.margin = margin(0),
        legend.position = "top",
        legend.title = element_blank()) +
  labs(y = "Frequency", x = "Group")

# Time cost boxplots
pdf("out/boxplot-timecost.pdf", height = 3, width = 3)
ggplot(data = rq1_df, aes(x = group, y = tmin, fill = test_success)) +
  geom_boxplot() +  theme(strip.text = element_blank(),
                          strip.background = element_blank(),
                          legend.background = element_rect(),
                          legend.margin = margin(0),
                          legend.title = element_blank(),
                          legend.position = "top") +
  scale_fill_grey(start = 0.5, end = 0.8, labels = c("tests fail", "tests pass")) +
  facet_wrap( ~ group, scales = "free") +
  labs(y = "Time cost (in minutes)", x = "Group")

###################
# RQ2
###################
# pdf("boxplot-timecost-dist.pdf", height = 2, width = 4)
# ggplot(rq2_df, aes(x = project, y = time)) +
#   geom_boxplot() +
#   theme(axis.text.x =  element_blank())

##################
# RQ3
###################

# pdf("parallel-modes.pdf", height = 2, width = 3)
# 
# # pdf("parallel-modes.pdf", height = 2, width = 3)
# ggplot(data = distinct(select(rq3_df, project, level)), aes(x = level)) +
#   geom_bar(width = .8) +
#   geom_text(
#     size = 2.5,
#     stat = "count",
#     aes(label = ..count.. , y = ..count.. + 0.5)
#   ) +
#   labs(y = "Frequency", x = "Parallelism Level")
# 
