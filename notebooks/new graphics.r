library(readxl)
library(readr)
library(ggplot2)
library(dplyr)
library(tidyr)

data_dir <- 'C:/Users/simon/Desktop/Turing/Projects/decision-services-index/data/processed/'

#377 services 
#VS: "these are the services that were live during the time of data collection (i.e., 06-08/2023) and for which we could gather data on; I've added a sentence to the Materials and Methods subsection 'Historical administrative records' to clarify this."
df_services <- read_xlsx(paste0(data_dir,'202308-services-list-processed.xlsx'))
df_trans_volumes <- read_csv(paste0(data_dir,'201204-201703-service-transactions-processed.csv'))
df_trans_volumes_short <- 
  df_trans_volumes %>% 
  select('service', 'max_observed')

df_services <- 
  df_services %>% left_join(df_trans_volumes_short, by=c('historical_service_equiv' = 'service'))
cor(df_services$unique_clicks_2022, df_services$max_observed, use='complete.obs')

#Number of services currently on offer----
##by type, topic
table(df$topic)
table(df$service_type, useNA = 'always')

ggplot(df, aes(x=topic)) + geom_bar() + coord_flip()

##by department
table(df$organisation)

##digital sign on required or not
#ask VS about this 
#maybe just send to Mat - not sure if it fits in the paper 


##network diagram - shows overlap of types. good potential for services to be shared across departments 


##parallel / correlation between web forms 








#Volumes
##Historic transaction volumes
##Distribution of transaction volumes (Zipf)
##Partial mapping to contemporary services 
##Parallel / correlation between web visits 

#DELETE PIP
#DOUBLE CHECK ALL ASSIGNMENT
#MODEL

l <- lm(log(max_observed+1) ~ log(unique_clicks_2022+1), data=df_services)

#predictive model for unique clicks 

df_services$predicted_transactions <- predict(l, df_services)

#set unknown values to mean / median 

sum(df_services$predicted_transactions)

#Automation 
##Share of routine tasks overall (Fig3b)
##breakdown by task type (Fig3A)
