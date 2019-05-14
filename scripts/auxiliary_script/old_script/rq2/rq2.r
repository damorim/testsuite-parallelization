library(ggplot2)
library(dplyr)
library(grDevices)

# Figure 7
df_med <- read.csv("dataset-testcases-medium.csv") %>% mutate(group = "medium")
df_long <- read.csv("dataset-testcases-long.csv") %>% mutate(group = "long")
df <- rbind(df_long, df_med)

df_stats <- df %>%
  group_by(project, group) %>%
    summarize(t = median(time)) %>%
        group_by(group) %>%
           summarise(avg = mean(t),
                     std = sd(t))

df_stats

cairo_pdf("testcost-distribution.pdf", width = 5, height = 2.5)
ggplot(df, aes(x = project, y = time)) +
  geom_boxplot(outlier.shape=NA) +
  geom_hline(
    data = df_stats,
    aes(yintercept = avg),
    colour = "red",
    linetype = 2,
    size = 0.3
  ) +
  theme_bw() +
  theme(strip.background = element_blank(),
    legend.background = element_rect(),
    legend.margin = margin(0),
    legend.title = element_blank(),
    axis.title.x = element_blank(),
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank()) +
  facet_wrap( ~ group, scales = "free", ncol = 1) +
  labs(y = "Time cost (in secs)") +
  coord_cartesian(ylim = c(0, 7))

dat <- summarise(group_by(df, project, group),
         n = length(time),
         time = sum(time))

# Figure 8.b
cairo_pdf("scatter-testcost.pdf", height = 3, width = 3)
ggplot(dat, aes(x = n / 100, y = time / 60)) +
  geom_point(size = 0.5, shape = 1) +
  facet_wrap( ~ group, nrow = 1, ncol = 2, scales = 'free') +
  labs(x = bquote(Number~of~test~cases~(x10^{2})), y = "Time cost (in minutes)") +
  theme_bw() +
  theme(strip.background = element_blank(),
    legend.background = element_rect(),
    legend.margin = margin(0),
    legend.title = element_blank(),
    legend.position = "top") +
  geom_smooth(method = lm)

# Figure 8.a
cairo_pdf("boxplots-testcases.pdf", height = 3, width = 1.5)
ggplot(dat, aes(x = group, y = n / 100)) +
  geom_boxplot() +
  theme_bw() +
  theme(strip.text = element_blank(),
    strip.background = element_blank(),
    axis.text.y = element_text(angle = 90, vjust = 0.5, hjust = 0.5),
    legend.background = element_rect(),
    legend.margin = margin(0),
    legend.title = element_blank(),
    legend.position = "top") +
  labs(y = bquote(Number~of~test~cases~(x10^{2})), x = "Groups")

