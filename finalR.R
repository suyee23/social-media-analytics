if (!require(rtweet)) {install.packages("rtweet")}
if (!require(tidytext)) {install.packages("tidytext")}
if (!require(ggpubr)) {install.packages("ggpubr")}
if (!require(tidyverse)) {install.packages("tidyverse")}
library(rtweet)
library(tidytext)
library(ggpubr) 
library(tidyverse) 

# Assigned application name
appname <- "Rsuyee"

# API Key 
key <- "ey2s7EinuSjMAKAnHgvVExUad"

# API Secret 
secret <- "a0YHoX0jGZ538LI8MJqh83ObQH4Adq8CtvRDGsyFr6KluL6XL8"

# Access Token
access_token = "1390192394407079936-UHfoksD6hsHxTy8rsmqJumiRs1hhlF"

# Access Secret
access_secret = "zfuPv42Y0nykbnzhUBEzrfNeF2UQm5CrJX1X3RrFiRKpW"

# Create token named "twitter_token"
twitter_token <- create_token(
  app = appname,
  consumer_key = key,
  consumer_secret = secret,
  access_token = access_token,
  access_secret = access_secret)

#lego <- get_timeline("@legogradstudent", n=3200)

# Scrape all recent tweets containing #coronavirus
corona_tweets <- search_tweets(q = "#coronavirus", n = 1000,
                                lang = "en",
                                include_rts = FALSE)

# Look at the dataframe
view(corona_tweets)

# Obtain first few rows
head(corona_tweets)

# Restructure corona_tweets as one-token-per-row format
tidy_tweets <- corona_tweets %>% # pipe data frame 
  filter(is_retweet==FALSE)%>% # only include original tweets
  select(status_id, 
         text)%>% # select variables of interest
  unnest_tokens(word, text) # splits column in one token per row format

view(tidy_tweets)

if (!require(textdata)) {install.packages("textdata")}
library(textdata)

my_stop_words <- tibble( #construct a dataframe
  word = c(
    "https",
    "t.co",
    "rt",
    "amp",
    "rstats",
    "gt"
  ),
  lexicon = "twitter"
)

# Connect stop words
all_stop_words <- stop_words %>%
  bind_rows(my_stop_words) # Connect two data frames

view(all_stop_words)

# Remove numbers
no_numbers <- tidy_tweets %>%
  filter(is.na(as.numeric(word))) # remember filter() returns rows where conditions are true

no_stop_words <- no_numbers %>%
  anti_join(all_stop_words, by = "word")

# Download NRC Emotion Lexicon.zip
nrc <- get_sentiments("nrc") # get specific sentiment lexicons in a tidy format

nrc_words <- no_stop_words %>%
  inner_join(nrc, by="word")

view(nrc_words)

pie_words<- nrc_words %>%
  group_by(sentiment) %>% # group by sentiment type
  tally %>% # counts number of rows
  arrange(desc(n)) # arrange sentiments in descending order based on frequency

ggpubr::ggpie(pie_words, "n", label = "sentiment", 
              fill = "sentiment", color = "white", 
              palette = "rickandmorty")

words_count<- no_stop_words %>% 
  dplyr::count(word, sort = TRUE) # count number of occurences

if (!require(ggwordcloud)) {install.packages("ggwordcloud")}
library(ggwordcloud) # we need to load the ggwordcloud package

set.seed(42)
wordcloudplot<- head(words_count, 50)%>% #select first 50 rows
  ggplot(aes(label = word, size = n, color = word, replace = TRUE)) + # start building your plot 
  geom_text_wordcloud_area() + # add wordcloud geom
  scale_size_area(max_size = 26) + # specify text size
  theme_minimal() # choose theme

wordcloudplot # Show word cloud

if(!require(wordcloud2)) {install.packages("wordcloud2")}
library(wordcloud2)

# Build wordcloud 
wordcloud <- wordcloud2(data = words_count, minRotation = 0, maxRotation = 0, ellipticity = 0.6)
wordcloud