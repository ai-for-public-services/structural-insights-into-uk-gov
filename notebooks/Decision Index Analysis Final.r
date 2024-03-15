#Note - this is the final file used for calculations, following updates by JF 13/03/24

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

data_dir <- '../data/processed/'

#377 services 
#VS: "these are the services that were live during the time of data collection (i.e., 06-08/2023) and for which we could gather data on; I've added a sentence to the Materials and Methods subsection 'Historical administrative records' to clarify this."
df_services <- read_xlsx(paste0(data_dir,'202308-services-list-processed-final.xlsx'))

#Data Preprocessing and transaction model----


#*Relabel topics----
#Employing people -> Benefits
#National security - > Citizenship and living in the UK
#"Coronavirus (COVID-19)" -> "Coronavirus"
df_services <- df_services %>% mutate(
  topic = case_when( # recoding some of the samll categories
    topic == "Employing people"~"Benefits", # recode
    topic == "National security"~"Citizenship and living in the UK", # recode
    topic == "Coronavirus (COVID-19)"~"Coronavirus", # recode
    TRUE~topic #keep the rest the same
  ),
  requesting_information = ifelse(service_type=="Requesting information",1,0),
  priority = ifelse(priority==TRUE,1,0)
  
)

#*Set unique clicks to median----
df_services$unique_clicks_final <- df_services$unique_clicks_2022
table(is.na(df_services$unique_clicks_final))#40 services have no click data 
table(df_services$unique_clicks_final==0)

df_services$unique_clicks_final[is.na(df_services$unique_clicks_final)==TRUE] <- median(df_services$unique_clicks_final, na.rm=TRUE) 
table(is.na(df_services$unique_clicks_final))


#*Transaction Model----
#how many services had a "true" transaction value in the data? (where they don't have x here)
table(df_services$final_transactions_value!='x')#118 services have a true transaction value

#change xs to NAs
df_services$final_transactions_value <- as.numeric(df_services$final_transactions_value)#expected NA warning message
table(is.na(df_services$final_transactions_value))

#create model
#trans_model <- lm(log10(final_transactions_value) ~ log10(unique_clicks_final), data=df_services)
#summary(trans_model)#can't use topic because there are some unseen levels
#r2 0.38

#trans_model_lmer <- lmer(formula = log10(final_transactions_value) ~ log10(unique_clicks_final) + (1|topic), data = df_services) 
#r.squaredGLMM(trans_model_lmer)# R2c == 0.4792763

#this is the final used predictive model 
trans_model_lmer <- lmer(formula = log10(final_transactions_value) ~ log10(unique_clicks_final) + (1|topic)+ (1|service_category) + requesting_information, data = df_services) 
r.squaredGLMM(trans_model_lmer)# R2c == 0.8053414



#predict transaction volumes for those services that don't have them 
df_services$predicted_transactions <- 10**predict(trans_model_lmer, df_services, allow.new.levels = TRUE)
#10** to go back from log transform


#make a final column with either the actual value or predicted one
df_services$transaction_value <- 
  case_when(
    is.na(df_services$final_transactions_value) ~ df_services$predicted_transactions,
    TRUE ~ df_services$final_transactions_value
  )

#check results
sum(df_services$transaction_value)
#how much of the overall volume is made up of actual numbers?
sum(df_services$final_transactions_value, na.rm=TRUE)

#median transaction volume
median(df_services$transaction_value)

#*Attach AST data----
df_ast <- read_csv(paste0(data_dir,'AST Assignments.csv'))
df_ast_short <- df_ast %>%
  select('RTI', 'task_count', 'RTI_perc', 'service', 'rubric_score_manual')

df_services$service <- tolower(df_services$service)
df_services <- 
  df_services %>% left_join(df_ast_short, by='service')

table(is.na(df_services$RTI), useNA='always')#201 services should have AST scores (hence should be false for NA)

#*Depts with <10 services----
df_services <- 
  df_services %>%
  group_by(organisation) %>%
  mutate(org_n = n()) %>%
  ungroup() %>%
  mutate(org_name = case_when(
    org_n < 10 ~ 'Other',
    TRUE ~ organisation
  ))

#*Write out data for visualisation----
write.csv(df_services, paste0(data_dir, 'services-list-with-transaction-volumes-final.csv'), 
          fileEncoding = 'utf-8')

#Results----

###NOTE - all graphics are now made in the ipython notebooks

#FIG1 Methods:
##Data collection pathway 
##Transaction volume estimation 
##AST score calculation 
##PGAI Calculation
##Could include number of registered organisations and services. 

##service turnover statistics - average in the python file 
##to present cautiously - missing data likely plays a role

#FIG2 Volumes 
##Service volumes, transaction volumes by type, department(? +10 services)
##Zipf distribution of transactions, annotated. Newwork graphic

#FIG3 AST/PGAIpotential
##Distribution of AST scores, annotated. Bucketised by transaction volume
##Table description of PGAI scores, by transaction volume 



#*Service count and transaction volumes----

##service count by topic and organisation
ggplot(df_services, aes(x=topic)) + geom_bar() + coord_flip()
ggplot(df_services[df_services$org_n>10,], 
       aes(x=org_name)) + geom_bar() + coord_flip()



#transactions and transaction distribution
df_trans_topic <- df_services %>%
  group_by(topic) %>%
  summarise(
    n = n(),
    sum = sum(transaction_value)
  )

df_trans_org <- df_services %>%
  group_by(org_name) %>%
  summarise(
    n = n(),
    sum = sum(transaction_value)
  )

ggplot(df_trans_topic, aes(x=topic, y=sum)) + 
  geom_bar(stat='identity') +
  coord_flip() + scale_y_log10(labels = scales::comma_format())

ggplot(df_trans_org, aes(x=org_name, y=sum)) + 
  geom_bar(stat='identity') +
  coord_flip() + scale_y_log10(labels = scales::comma_format())

##network diagram - shows overlap of topics good potential for services to be shared across departments 
##this is contained in another file 

#power law distribution of services in transaction volume 
df_services$rank <- rank(-df_services$transaction_value)
ggplot(df_services, aes(x = rank, y = transaction_value)) + 
  geom_point() + coord_trans(y = "log10", x = "log10") 

#*Automation---- 
##Share of routine tasks overall (Fig3b)
##breakdown by task type (Fig3A)

#only rti scores for 201 services 
df_services_rti <- df_services %>% filter(!is.na(RTI))

#num transactions for the rti data
sum(df_services_rti$transaction_value)

#as proportion of total
sum(df_services_rti$transaction_value)/sum(df_services$transaction_value)

#tasks per service, sd
summary(df_services_rti$task_count)
sd(df_services_rti$task_count)

#avg routine tasks
mean(df_services_rti$RTI_perc)
nrow(df_services_rti[df_services_rti$RTI_perc==100,])/nrow(df_services_rti)

#how many services with above 75% RTI?
df_services_rti_highly <- df_services_rti[df_services_rti$RTI_perc>=75,]#149
149/201#74%
#how many transactions do they account for?
sum(df_services_rti_highly$transaction_value)
sum(df_services_rti_highly$transaction_value)/sum(df_services_rti$transaction_value)#0.84

#how many transactions above 0.9
sum(df_services_rti$transaction_value[df_services_rti$RTI_perc>=90])/sum(df_services_rti$transaction_value)
71/201#74%


#distribution of routine tasks
ggplot(df_services_rti, aes(x=RTI_perc, y=(..count..)/sum(..count..))) + 
  geom_bar() +
  scale_x_binned() +
  scale_y_continuous(labels=scales::percent_format())

#rti / transaction volume link
df_services_rti <- df_services_rti %>% 
  mutate(rti_bin = cut(RTI_perc, 
                              width=10,
                             breaks=c(30,40,50,60,70,80,90,100)))

rti_summary <- 
  df_services_rti %>%
  group_by(rti_bin) %>%
  summarise(
    n = n(),
    perc_services = n/nrow(df_services_rti),
    num_trans_affected = sum(transaction_value),
    perc_trans_affected = sum(transaction_value)/sum(df_services_rti$transaction_value)
  )

ggplot(rti_summary, aes(x=rti_bin, y=perc_trans_affected)) +
  geom_bar(stat='identity')

#pgenai data 
table(df_services_rti$rubric_score_manual)



#*Potential saving statistics
#How much difference would saving 10 minutes per transactions for these 150 million transactions?
sum(df_services_rti$transaction_value)
#143129315

# if we were only to look at low automatable services..
test_df <- df_services_rti %>% filter(RTI_perc<75)
sum(test_df$transaction_value)



#mil140 <- 143129315
#88% highly automatable
#mil140.88 <- mil140 * 0.88


transactions_addressed <- sum(df_services_rti_highly$transaction_value)

minutes_saved <- transactions_addressed * 1

hours_saved <- minutes_saved / 60
hours_saved

hours_work_year <- 36.4 * 46.5
#https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/ybuy/lms

work_years_saved <- hours_saved / hours_work_year
work_years_saved

#*Service turnover ----
#Recording here how service turnover is estimated

#Look at the spreadsheet 201204-201703-service-transactions-processed

#Check the number of transactions recorded every (non digital) end of year quarter.

#201312 - 393
#201412 - 379
#201512 - 348
#201612 - 293

#However it is really hard to tell which services have changed and which data is just missing. 
#In the end let's not report a hard number on service change.



