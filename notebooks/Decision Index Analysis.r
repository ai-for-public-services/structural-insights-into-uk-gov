#Topline questions


library(readxl)
library(readr)
library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(pwr)
library(lme4)
library(MuMIn)

#Load Data----

data_dir <- 'C:/Users/simon/Desktop/Turing/Projects/decision-services-index/data/processed/'

#377 services 
#VS: "these are the services that were live during the time of data collection (i.e., 06-08/2023) and for which we could gather data on; I've added a sentence to the Materials and Methods subsection 'Historical administrative records' to clarify this."
df_services <- read_xlsx(paste0(data_dir,'202308-services-list-processed-final.xlsx'))

#Data Preprocessing and transaction model----

#Set unique clicks to average if not available
df_services$unique_clicks_final <- df_services$unique_clicks_2022
table(is.na(df_services$unique_clicks_final))
table(df_services$unique_clicks_final==0)

df_services$unique_clicks_final[is.na(df_services$unique_clicks_final)==TRUE] <- median(df_services$unique_clicks_final, na.rm=TRUE) 

#*Transaction Model----

#turn X into NA
table(df_services$final_transactions_value=='x')
df_services$final_transactions_value <- as.numeric(df_services$final_transactions_value)
table(is.na(df_services$final_transactions_value))

#create model
trans_model <- lm(log10(final_transactions_value) ~ log10(unique_clicks_final), data=df_services)

trans_model_lmer <- lmer(formula = log10(final_transactions_value) ~ log10(unique_clicks_final) + (1|topic), data = df_services) 
r.squaredGLMM(trans_model_lmer)#best fit

#predict results 
df_services$predicted_transactions <- 10**predict(trans_model_lmer, df_services, allow.new.levels = TRUE)

#make a final column with either the actual value or predicted one
df_services$transaction_value <- 
  case_when(
    is.na(df_services$final_transactions_value) ~ df_services$predicted_transactions,
    TRUE ~ df_services$final_transactions_value
  )

sum(df_services$transaction_value)
sum(df_services$final_transactions_value, na.rm=TRUE)


#Results----

#*1 Types----

##by type, topic
table(df$topic)
table(df$service_type, useNA = 'always')

ggplot(df, aes(x=topic)) + geom_bar() + coord_flip()

##by department
table(df$organisation)


##network diagram - shows overlap of types. good potential for services to be shared across departments 


##parallel / correlation between web forms? 



#*2 Volumes----
##Distribution of transaction volumes (Zipf)
##Partial mapping to contemporary services 
##Parallel / correlation between web visits 

#transactions and transaction distribution
df_sum <- df_services %>%
  group_by(topic) %>%
  summarise(
    n = n(),
    sum = sum(transaction_value)
  )

ggplot(df_sum, aes(x=topic, y=sum)) + 
  geom_bar(stat='identity') +
  coord_flip() + scale_y_log10(labels = scales::comma_format())
  

#power law distribution of services 
df_services$rank <- rank(-df_services$transaction_value)
ggplot(df_services, aes(x = rank, y = transaction_value)) + 
  geom_point() + coord_trans(y = "log10", x = "log10") 


#*3 Automation---- 
##Share of routine tasks overall (Fig3b)
##breakdown by task type (Fig3A)

df_ast <- read_csv(paste0(data_dir,'AST Assignments.csv'))

df_ast_short <- df_ast %>%
  select('RTI', 'govuk_start_page_url')

df_services <- 
  df_services %>% left_join(df_ast_short, by='govuk_start_page_url')

table(is.na(df_services$RTI), useNA='always')#8 more services should be matched - need to check the matching
