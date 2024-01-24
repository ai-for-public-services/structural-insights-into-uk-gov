library(readxl)
library(ggplot2)

data_dir <- 'C:/Users/simon/Desktop/Turing/Projects/decision-services-index/data/processed/'


df <- read_xlsx(paste0(data_dir,'202308-services-list-processed.xlsx'))
