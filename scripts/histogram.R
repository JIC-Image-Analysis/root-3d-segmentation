library("jsonlite")
library("ggplot2")

args <- commandArgs(trailingOnly=TRUE)
data <- fromJSON(args[1])

ggplot(data, aes("intensity")) + geom_histogram()
ggsave(args[2])
