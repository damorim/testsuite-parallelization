library("ggplot2")
library("dplyr")
library("grDevices")

df <- read.csv("dataset-sanitized.csv")

print("DISTRIBUTION ACCORDING TO THRESHOLD")
df %>%
  group_by(timecost_group, below_threshold) %>%
    summarise(n = length(perc_failures),
              avg = mean(perc_failures),
              sd = sd(perc_failures))

# Subject barplot - Fig 6.a
cairo_pdf("barplot-timecost.pdf", height = 3, width = 2.2)
ggplot(filter(df, below_threshold == T), aes(x = timecost_group)) +
  geom_bar(width = .8, position = "dodge", colour = "black", fill = "white") +
  geom_text(
    size = 3,
    stat = "count",
    aes(label = ..count..),
    position = position_stack(),vjust = 0.5) +
  theme_bw() +
  labs(y = "Number of projects", x = "Group")
 
# Subject boxplot - Fig 6.b
cairo_pdf("boxplot-timecost.pdf", height = 3, width = 3)
ggplot(filter(df, below_threshold == T), aes(x = timecost_group, y = xml_time_avg / 60)) +
  geom_boxplot() +
  theme_bw() +
  theme(strip.text = element_blank(),
    strip.background = element_blank(),
    legend.background = element_rect(),
    legend.margin = margin(0),
    legend.title = element_blank(),
    legend.position = "top") +
  facet_wrap( ~ timecost_group, scales = "free") +
  labs(y = "Time cost (in minutes)", x = "Group")
