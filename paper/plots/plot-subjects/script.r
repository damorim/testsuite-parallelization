library("dplyr")
library("ggplot2")

df <- read.csv("mocked-data.csv")
pdf("subjs.pdf", width = 2.8, height = 2)

df <- summarise(group_by(df, group), length = length(group)) 
ggplot(df, aes(x = factor(1), y = length, fill = group)) +
    theme_void() +
    geom_bar(stat = "identity", width = 1) +
    geom_text(aes(label = length), position = position_stack(vjust = 0.5)) +
    coord_polar("y")
