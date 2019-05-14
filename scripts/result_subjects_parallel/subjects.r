library("ggplot2")
library("stats")
library("dplyr")
library("grDevices")

df <- read.csv("dataset-subjects.csv")

# Subjects piechart
cairo_pdf("piechart-subjs.pdf", width = 3.65, height = 3)
ggplot(df, aes(x = factor(1), y = value, fill = type)) +
  geom_bar(width = 1, stat = "identity", colour = "black") +
  theme_void() +
  scale_fill_manual(values = c("#000000", "#AAAAAA", "#777777", "#333333", "#FFFFFF")) +
  theme(legend.title = element_blank()) +
  geom_text(
    aes(x = 1.7, label = value),
    position = position_stack(),vjust = 0.5,
    size = 3) +
  coord_polar("y")
