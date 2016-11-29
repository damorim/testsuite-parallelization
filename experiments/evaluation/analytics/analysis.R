base_dir <- "/home/jbc/projects/regression-test-study/experiments/evaluation/data/"
path <- paste(base_dir, "rawdata.csv", sep="")
mydata <- read.csv(path)

View(mydata)

t <- sum(mydata$elapsed_time) 
sprintf("total time: %.2f hours", t / 360)

diff_tuser_twall <- function(mode_filter, data, captcha) {
    temp <- mydata[data$mode == mode_filter,]
    temp <- temp[temp$t_user > temp$t_wall,]
    for (name in temp$name) {
      print(name)
    }
    diffs <- temp$t_user - temp$t_wall
    p <- barplot(diffs, names.arg=temp$name, col=colors(distinct=T),
                 axes=F, las=2, space=0, main=captcha)
    text(x=p, y=diffs, label=diffs, pos=3)
}

diff_tuser_twall("L0", mydata, "delta of user_t - wall_t for L0")
diff_tuser_twall("ST", mydata, "delta of user_t - wall_t for Standard")
