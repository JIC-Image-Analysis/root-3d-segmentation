library("jsonlite")
library("ggplot2")

args <- commandArgs(trailingOnly=TRUE)
data <- fromJSON(args[1])
data$normalised.intensity <- data$intensity / data$area

ggplot(data, aes(normalised.intensity)) + geom_histogram()
ggsave(args[2])
