netflix_info <- readxl::read_excel("넷플릭스 콘텐츠 정보_최종본 (1).xlsx")
 netflix.df <- as.data.frame(netflix_info)                                                                                            
 netflix.df <- subset(netflix.df, select = -c(running_time))
 netflix.df <- netflix.df %>%
       distinct(netflix.df$origin_keyword, .keep_all = TRUE)
 netflix.df <- netflix.df[1:2000,]
 
# rated 정제
library(dplyr)
convert_rating_to_number <- function(rating) {
rating_map <- list(
  "PG" = 0,
  "G" = 0,
  "TV-PG" = 0,
  "TV-14" = 14,
  "TV-G" = 0,
  "PG-13" = 13,
  "Request" = 17,  # 요청에 따른 추가
  "R" = 17,
  "TV-MA" = 17,
  "TV-Y7" = 7,
  "TV-Y" = 0,
  "TV-Y7-FV" = 7,
  "(Banned)" = 18,
  "All" = 0,
  "16+" = 16,
  "Approved" = 0,
  "Youth not allowed" = 18,
  "Limited" =18,
  "M/PG" = 12,
  "NC-17" = 17,
  "Passed" = 0,
  "7" = 7,
  "12" = 12,
  "13" = 13,
  "13+" = 13,
  "15" = 15,
  "18" =18,
  "18+" = 18,
  "19" = 19
)
return(rating_map[[rating]])
}
netflix.df <- netflix.df %>%mutate(rated = sapply(rated, convert_rating_to_number))
#Null값 제거
netflix.df <- netflix.df[sapply(netflix.df$rated, function(x) !is.null(x)), ]
netflix.df$rated <- as.character(netflix.df$rated)

#released.date를 2023년1월1일로부터 몇일 차이나는지 계산
netflix.df$released_date <- as.Date(netflix.df$released_date, format="%B %d, %Y")
reference_date <- as.Date("2023-01-01")
netflix.df$days_from_reference <- as.integer(difftime(netflix.df$released_date, reference_date, units = "days")) # 파생변수 생성

# content 종류 Movie와 Tv Series를 수치화
#Tv-Series -1 / Movie - 0
netflix.df$content_type[is.na(netflix.df$content_type)] <- 'Movie'
netflix.df$content_type <- factor(netflix.df$content_type)
netflix.df$content_type_numeric <- as.integer(netflix.df$content_type) - 1

## isGolbally 수치화
netflix.df$isGlobal <- factor(netflix.df$isGlobal)
 netflix.df$isGlobal <- as.integer(netflix.df$isGlobal)
 netflix.df$isGlobal <- netflix.df$isGlobal-1

netflix.df <- na.omit(netflix.df)
# 나라 원핫 인코딩
library(caret)
dummy_model <- dummyVars("~ country", data=netflix.df)
netflix.df_encoded_country <- predict(dummy_model, newdata = netflix.df)
netflix.df_encoded_country <- as.data.frame(netflix.df_encoded_country)
colnames(netflix.df_encoded_country) <- gsub(" ", "_", colnames(netflix.df_encoded_country))
# 원핫 인코딩된 데이터프레임과 원래 데이터 프레임 합치기

#언어 원 핫 인코딩
dummy_model <- dummyVars("~ language", data=netflix.df)
netflix.df_encoded_language <- predict(dummy_model, newdata = netflix.df)
netflix.df_encoded_language <- as.data.frame(netflix.df_encoded_language)
colnames(netflix.df_encoded_language) <- gsub(" ", "_", colnames(netflix.df_encoded_language))

#배우1 원 핫 인코딩
dummy_model <- dummyVars("~ actor1", data=netflix.df)
netflix.df_encoded_actor1 <- predict(dummy_model, newdata = netflix.df)
netflix.df_encoded_actor1 <- as.data.frame(netflix.df_encoded_actor1)
colnames(netflix.df_encoded_actor1) <- gsub(" ", "_", colnames(netflix.df_encoded_actor1))


#배우2 원 핫 인코딩
dummy_model <- dummyVars("~ actor2", data=netflix.df)
netflix.df_encoded_actor2 <- predict(dummy_model, newdata = netflix.df)
netflix.df_encoded_actor2 <- as.data.frame(netflix.df_encoded_actor2)
colnames(netflix.df_encoded_actor2) <- gsub(" ", "_", colnames(netflix.df_encoded_actor2))


#감독 원 핫 인코딩
#dummy_model <- dummyVars("~ director", data=netflix.df)
#netflix.df_encoded_director <- predict(dummy_model, newdata = netflix.df)
#netflix.df_encoded_director <- as.data.frame(netflix.df_encoded_director)
#colnames(netflix.df_encoded_director) <- gsub(" ", "_", colnames(netflix.df_encoded_director))
library(tidyr)
netflix.df <- netflix.df %>%
  separate_rows(director, sep = ", ")
dummy_model <- dummyVars("~ director", data=netflix.df)
netflix.df_encoded_director <- predict(dummy_model, newdata = netflix.df)
netflix.df_encoded_director <- as.data.frame(netflix.df_encoded_director)
netflix.df_encoded_director$origin_keyword <- netflix.df$origin_keyword
library(dplyr)
library(data.table)
setDT(netflix.df_encoded_director)
netflix.df_encoded_director <- netflix.df_encoded_director[, lapply(.SD, sum), by = origin_keyword]
#netflix.df_encoded_director <- netflix.df_encoded_director %>%
#  group_by(origin_keyword) %>%
#  summarise_all(sum)
netflix.df_encoded_director <- subset(netflix.df_encoded_director, select = -c(origin_keyword))
colnames(netflix.df_encoded_director) <- gsub(" ", "_", colnames(netflix.df_encoded_director))


#장르 원 핫 인코딩
library(tidyr)
netflix.df <- netflix.df %>%
       separate_rows(genre, sep = ", ")
dummy_model <- dummyVars("~ genre", data=netflix.df)
netflix.df_encoded_genre <- predict(dummy_model, newdata = netflix.df)
netflix.df_encoded_genre <- as.data.frame(netflix.df_encoded_genre)
netflix.df_encoded_genre$origin_keyword <- netflix.df$origin_keyword
library(dplyr)
netflix.df_encoded_genre <- netflix.df_encoded_genre %>%
    group_by(origin_keyword) %>%
     summarise_all(sum)
netflix.df_encoded_genre <- subset(netflix.df_encoded_genre, select = -c(origin_keyword))
colnames(netflix.df_encoded_genre) <- gsub(" ", "_", colnames(netflix.df_encoded_genre))

#회사
library(tidyr)
netflix.df <- netflix.df %>%
  separate_rows(company, sep = ", ")
dummy_model <- dummyVars("~ company", data=netflix.df)
netflix.df_encoded_company <- predict(dummy_model, newdata = netflix.df)
netflix.df_encoded_company <- as.data.frame(netflix.df_encoded_company)
netflix.df_encoded_company$origin_keyword <- netflix.df$origin_keyword
library(dplyr)
library(data.table)
setDT(netflix.df_encoded_company)
netflix.df_encoded_company <- netflix.df_encoded_company[, lapply(.SD, sum), by = origin_keyword]

#netflix.df_encoded_company <- netflix.df_encoded_company %>%
#  group_by(origin_keyword) %>%
#  summarise_all(sum)
netflix.df_encoded_company <- subset(netflix.df_encoded_company, select = -c(origin_keyword))
colnames(netflix.df_encoded_company) <- gsub(" ", "_", colnames(netflix.df_encoded_company))

##
netflix.df <- subset(netflix.df, select = -c(content_type, genre, actor1, actor2, director,released_date, country, language, company, origin_keyword, title))

netflix.df <- cbind(netflix.df, c(netflix.df_encoded_country,netflix.df_encoded_actor1,netflix.df_encoded_actor2,netflix.df_encoded_company,netflix.df_encoded_director,netflix.df_encoded_genre,netflix.df_encoded_language))

#컬럼 이름에서 공백 및 특수문자 없애기
names(netflix.df) <- gsub("[^[:alnum:] ]", "_", names(netflix.df))
names(netflix.df) <- gsub(" ", "_", names(netflix.df))

# 학습
set.seed(123) # 재현 가능한 결과를 위해 시드 설정
index <- createDataPartition(netflix.df$viewed, p = 0.7, list = FALSE)
 train_data <- netflix.df[index, ]
 test_data <- netflix.df[-index, ]
rf_model <- randomForest(viewed ~ ., data = train_data, ntree = 500)

#결과
predictions <- predict(rf_model, test_data)