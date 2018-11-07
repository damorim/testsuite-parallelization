library("ggplot2")
library("grDevices")

df <- read.csv("survey/survey-answers.csv")
cairo_pdf("survey.pdf", width = 2, height = 2)
ggplot(df, aes(x = factor(1), y = value, fill = options)) +
  theme_void() +
  theme(legend.position = "none") +
  scale_fill_grey(start = 0.85, end = 1, name = "") +
  geom_bar(stat = "identity", width = 1, colour = "black") +
  geom_text(aes(x = 1.65, label = value), position = position_stack(vjust = 0.5)) +
  geom_text(aes(x = 1.1, label = options), position = position_stack(vjust = 0.5)) +
  coord_polar("y")

