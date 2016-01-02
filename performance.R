perf = function(cut, y, fitted)
{
  # cut is the cutting point
  # fitted is the probability calculated from the model for each observation in
  # the training dataset
  class <- ifelse(fitted>cut, 1, 0)
  
  temp1 = 0
  for(i in 1:length(y))
    if(y[i]==1&class[i]==1)
      temp1 = temp1 + 1
  
  temp2 = 0
  for(i in 1:length(y))
    if(y[i]==0&class[i]==0)
      temp2 = temp2 + 1
  
  # Precision
  precision <- ifelse(length(which(class==1))>0, temp1/length(which(class==1)), NA)
  
  # Recall
  recall <- ifelse(length(which(y==1))>0, temp1/length(which(y==1)), NA)
  
  # F-score
  fscore <- 2*precision*recall/(precision + recall)
  
  # Specificity
  specificity <- ifelse(length(which(y==0))>0, temp2/length(which(y==0)), NA)
  
  # proportion of true negatives
  tn <- ifelse(length(which(class==0))>0, temp2/length(which(class==0)), NA)
  
  # Classification Rate
  cr <- length(which(class == y))/length(y)
  
  return_value <- list("Precision" = precision, "Recall" = recall, "F_Score" = fscore,
                       "Specificity" = specificity, "trueNegatives" = tn,
                       "ClassificationRate" = cr)
  return(return_value)
}