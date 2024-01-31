library(readxl)
library(ggplot2)

data_dir <- 'C:/Users/simon/Desktop/Turing/Projects/decision-services-index/data/processed/'

df <- read_xlsx(paste0(data_dir,'202308-services-list-processed.xlsx'))

table(df$organisation)

table(df$service_type, useNA = 'always')

sum(table(df$service_type, useNA = 'always'))



#Number of services currently on offer
##by type
##by department
##digital sign on required or not
##network diagram - shows overlap of types. good potential for services to be shared across departments 
##parallel / correlation between web forms 

#Volumes
##Historic transaction volumes
##Distribution of transaction volumes (Zipf)
##Partial mapping to contemporary services 
##Parallel / correlation between web visits 

#Automation 
##Share of routine tasks overall (Fig3b)
##breakdown by task type (Fig3A)
