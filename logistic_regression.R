#########################Preparation###########################
# train_smote_x2$dayoftask <- as.numeric(train_smote_x2$dayoftask)
# train_smote_x2$daygroup <- ifelse(train_smote_x2$dayoftask>=1&train_smote_x2$dayoftask<=10,"early",
#                          ifelse(train_smote_x2$dayoftask>10&train_smote_x2$dayoftask<=20,"mid","late"))
# train_smote_x2$daygroup <- as.factor(train_smote_x2$daygroup)
# train_smote_x3$dayoftask <- as.numeric(train_smote_x3$dayoftask)
# train_smote_x3$daygroup <- ifelse(train_smote_x3$dayoftask>=1&train_smote_x3$dayoftask<=10,"early",
#                                   ifelse(train_smote_x3$dayoftask>10&train_smote_x3$dayoftask<=20,"mid","late"))
# train_smote_x3$daygroup <- as.factor(train_smote_x3$daygroup)
# train_smote_x7$dayoftask <- as.numeric(train_smote_x7$dayoftask)
# train_smote_x7$daygroup <- ifelse(train_smote_x7$dayoftask>=1&train_smote_x7$dayoftask<=10,"early",
#                                   ifelse(train_smote_x7$dayoftask>10&train_smote_x7$dayoftask<=20,"mid","late"))
# train_smote_x7$daygroup <- as.factor(train_smote_x7$daygroup)
# 
# train_smote_x2 <- within(train_smote_x2, rm(dayoftask,monthoftask))
# train_smote_x3 <- within(train_smote_x3, rm(dayoftask,monthoftask))
# train_smote_x7 <- within(train_smote_x7, rm(dayoftask,monthoftask))
# 
# test$dayoftask <- as.numeric(test$dayoftask)
# test$daygroup <- ifelse(test$dayoftask>=1&test$dayoftask<=10,"early",
#                         ifelse(test$dayoftask>10&test$dayoftask<=20,"mid","late"))
# test <- within(test,rm(dayoftask,monthoftask))
# 
# table(clean_data$device)
# table(clean_data$os)
# table(clean_data$appname)
# train_smote_x7 <- within(train_smote_x7, rm(device,appname))

source('performance.R')
source('cutoff.R')
source('analysis.R')
library("ggplot2")
library("reshape2")
library("pscl")
library("glmulti")
balance_index <- sample(nrow(train_smote_x7), 50000)
balanced_train <- train_smote_x7[balance_index,]

training <- read.csv("training.csv")
training <- within(training, rm(X))
testing <- read.csv("testing.csv")
testing <- within(testing, rm(X))
logit_train <- training
logit_train$daygroup <- ifelse(logit_train$dayoftask >= 1 & logit_train$dayoftask <= 10, "early",
                               ifelse(logit_train$dayoftask >= 11 & logit_train$dayoftask <= 20, "mid", "late"))
logit_train$aoa <- logit_train$pasttrunksales_amt/logit_train$pasttrunksales
logit_train$aoa[which(is.na(logit_train$aoa))] = 0
logit_train$pr <- logit_train$pasttrunksales/logit_train$pasttrunkssent
logit_train$pr[which(is.na(logit_train$pr))] = 0
logit_train <- within(logit_train, rm(dayoftask, monthoftask, device, appname))
logit_train$requesttype <- as.factor(logit_train$requesttype)
logit_train$yearoftask <- as.factor(logit_train$yearoftask)
logit_train$daygroup <- as.factor(logit_train$daygroup)
logit_train$burstid <- as.factor(logit_train$burstid)
logit_train$allbrands <- as.factor(logit_train$allbrands)
logit_train$tcbrands <- as.factor(logit_train$tcbrands)


#########################Full model for train_smote_x7#######################
full_x7 <- glm(saleoutcome ~ ., data = train_smote_x7, family = binomial)
summary(full_x7)
full_x7_nopast <- glm(saleoutcome ~ ., data = train_smote_x7_nopast, family = binomial)
summary(full_x7_nopast)

# fittedvalue <- fitted(full_x7)
# temp <- cutoff(train_smote_x2$saleoutcome,fittedvalue)
# full_x2_cut_f <- temp$Cutoff_FScore
# full_x2_cut_cr <- temp$Cutoff_ClassRate
# perf(full_x2_cut_f,train_smote_x2$saleoutcome,fittedvalue)
# perf(full_x2_cut_cr,train_smote_x2$saleoutcome,fittedvalue)
# # prediction
# full_x2_prob <- predict(full_x2, newdata = test)
# test$full_x2 <- ifelse(full_x2_prob>full_x2_cut_f, 1, 0)
# table <- table(test$saleoutcome,test$full_x2)
# # performance
# perf(full_x2_cut_f,test$saleoutcome,test$full_x2)
# # pseudo R-squared
# pR2(full_x2)[4] # -- McFadden Pseudo R-squared
# max(length(which(test$full_x2==1))/length(test$saleoutcome),
#     length(which(test$full_x2==0))/length(test$saleoutcome))

#########################Full model for balanced_train########################
full_balance <- glm(saleoutcome ~ ., data = balanced_train, family = binomial)
summary(full_balance)

full_balance_analysis <- analysis(full_balance,balanced_train$saleoutcome,test)
full_balance_analysis$Cutoff
full_balance_analysis$PseudoR2
full_balance_analysis$Threshold

performance <- perf(full_balance_analysis$Cutoff, test$saleoutcome, full_balance_analysis$Prediction)
performance


full_balance_nopast <- glm(saleoutcome ~ ., data = balanced_train_nopast, family = binomial)
summary(full_balance_nopast)

# fittedvalue <- fitted(full_x3)
# temp2 <- cutoff(train_smote_x3$saleoutcome,fittedvalue)
# full_x3_cut_f <- temp2$Cutoff_FScore
# full_x3_cut_cr <- temp2$Cutoff_ClassRate
# perf(full_x3_cut_f,train_smote_x3$saleoutcome,fittedvalue)
# perf(full_x3_cut_cr,train_smote_x3$saleoutcome,fittedvalue)
# # prediction
# full_x3_prob <- predict(full_x3, newdata = test)
# test$full_x3 <- ifelse(full_x3_prob>full_x3_cut_f, 1, 0)
# table <- table(test$saleoutcome,test$full_x3)
# # performance
# perf(full_x3_cut_f,test$saleoutcome,test$full_x3)
# # pseudo R-squared
# pR2(full_x3)[4] # -- McFadden Pseudo R-squared
# max(length(which(test$full_x3==1))/length(test$saleoutcome),
#     length(which(test$full_x3==0))/length(test$saleoutcome))

##########################stepwise regression for train_smote_x7#####################
step_x7 <- step(full_x7)
# step_x7_best <- glm(saleoutcome ~ ?, data = train_smote_x2, family = binomial)

##########################stepwise regression for balanced_train#####################
step_balance <- step(full_balance)
step_balance_best <- glm(saleoutcome ~ requesttype + region + burstid + membernotewc + 
                      membernotewc_common + yearoftask + dayofweek + season + tasktimeofday + 
                      children + num_notes + len_note + allbrands + tcbrands + 
                      os + apptype + pasttrunksales + pasttrunkssent + pasttrunksales_amt,
                    data = balanced_train, family = binomial)
summary(step_balance_best)

step_balance_analysis <- analysis(step_balance_best,balanced_train$saleoutcome,test)
step_balance_analysis$Cutoff
step_balance_analysis$PseudoR2
step_balance_analysis$Threshold

performance <- perf(step_balance_analysis$Cutoff, test$saleoutcome, step_balance_analysis$Prediction)
performance

##########################bestglm for balanced_train#########################
library("bestglm")
balanced_train_glm <- within(balanced_train,
                             {y <- saleoutcome
                             saleoutcome <- NULL})

bestglm_balance <- bestglm(Xy = balanced_train_glm, family = binomial, IC = "AIC", TopModels = 3)
# best_sub <- glm(saleoutcome~, data = train_new, family = binomial)
summary(best_sub)

##########################glmulti for balanced_train#############################
glmulti_balance <- glmulti(full_balance, maxsize = 20, method = "g", family = binomial,
                           confsetsize = 3, plotty = F, report = T)

##########################Create new variables##################################
balanced_train$aoa <- balanced_train$pasttrunksales/balanced_train$pasttrunkssent
balanced_train$aoa[which(is.na(balanced_train$aoa))] = 0
summary(balanced_train$aoa)
boxplot(balanced_train$aoa)
hist(balanced_train$aoa)
test$aoa <- test$pasttrunksales/test$pasttrunkssent
test$aoa[which(is.na(test$aoa))] = 0

logit_index <- sample(1:nrow(logit_train), 0.5*nrow(logit_train))
logit_training <- logit_train[logit_index,]
weights = ifelse(logit_training$saleoutcome == 0, 1, 7)
logit <- glm(saleoutcome ~ ., data = logit_training, family = binomial, weights = weights)
summary(logit)
