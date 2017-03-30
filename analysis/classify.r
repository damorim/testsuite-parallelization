library("dplyr")
library("ggplot2")

args <- commandArgs(trailingOnly = TRUE)
df <- read.csv(args[1])
pdf("out/subjs.pdf", width = 2.8, height = 2)

df <- summarise(group_by(df, group), length = length(group)) 
ggplot(df, aes(x = factor(1), y = length, fill = group)) +
    theme_void() +
    scale_fill_grey(start = 0.3, end = 0.9) +
    geom_bar(stat = "identity", width = 1) +
    geom_text(aes(label = length), position = position_stack(vjust = 0.5)) +
    coord_polar("y")

