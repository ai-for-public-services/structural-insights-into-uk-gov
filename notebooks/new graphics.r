#Topline questions
##What is the nature of the 'digital' columns in the transactions data 
#problems with the max observed approach - is it the right way to go about it?
#remove passenger transit - right approach?


library(readxl)
library(readr)
library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(pwr)

data_dir <- 'C:/Users/simon/Desktop/Turing/Projects/decision-services-index/data/processed/'

#377 services 
#VS: "these are the services that were live during the time of data collection (i.e., 06-08/2023) and for which we could gather data on; I've added a sentence to the Materials and Methods subsection 'Historical administrative records' to clarify this."
df_services <- read_xlsx(paste0(data_dir,'202308-services-list-processed.xlsx'))


#should change max observed to most recent observed


df_trans_volumes <- read_csv(paste0(data_dir,'201204-201703-service-transactions-processed.csv'))
df_trans_volumes_short <- 
  df_trans_volumes %>% 
  select('service', 'max_observed') %>%
  #decided to drop passenger arrivals as not really a service
  filter(service != 'Passenger arrivals at the UK border')

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



##network diagram - shows overlap of types. good potential for services to be shared across departments 


##parallel / correlation between web forms 








#Volumes
##Historic transaction volumes
##Distribution of transaction volumes (Zipf)
##Partial mapping to contemporary services 
##Parallel / correlation between web visits 

df_sum <- df_trans_volumes %>%
  group_by(Servicetype) %>%
  summarise(
    n = n(),
    sum = sum(max_observed)
  )

#total service volume
sum(df_sum$sum)
ggplot(df_sum, aes(x=Servicetype, y=sum)) + 
  geom_bar(stat='identity') +
  coord_flip() + scale_y_continuous(labels = comma_format()) 
  

#power law distribution of services 
#annotate graphic and make nice as in VS example
df_trans_volumes$rank <- rank(-df_trans_volumes$max_observed)
ggplot(df_trans_volumes, aes(x = rank, y = max_observed+1)) + 
  geom_point() + coord_trans(y = "log10", x = "log10") +
  abline(a=-1,b=1)


#map to current data


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
