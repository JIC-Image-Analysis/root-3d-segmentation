library("ggplot2")

args <- commandArgs(trailingOnly=TRUE)
data <- read.csv(args[1], header=TRUE)
data$mean.intensity <- data$total_intensity / data$voxels

data$genotype <- sapply(strsplit(as.character(data$series_name), "_"), "[[", 1)

# Merge different seed bags.
data$genotype <- sapply(strsplit(as.character(data$genotype), "-"), "[[", 1)

data$treatment <- sapply(strsplit(as.character(data$file), ".lif"), "[[", 1)
data$treatment <- sapply(strsplit(as.character(data$treatment), "_"), "[[", 2)

ggplot(data, aes(mean.intensity)) +
  geom_histogram(aes(fill=..x..), bins=60) +
  facet_grid(genotype ~ treatment) +
  scale_fill_continuous(low="blue", high="yellow")
ggsave(args[2])
