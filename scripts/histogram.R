library("jsonlite")
library("ggplot2")

args <- commandArgs(trailingOnly=TRUE)
data <- fromJSON(args[1])
data$normalised.intensity <- data$total_intensity / data$voxels

ggplot(data, aes(normalised.intensity)) +
  geom_histogram(aes(fill=..x..)) +
  scale_fill_continuous(low="blue", high="yellow")
ggsave(args[2])
