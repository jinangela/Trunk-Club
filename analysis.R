analysis <- function(model,y,testset)
{
  fittedvalue <- fitted(model)
  temp <- cutoff(y,fittedvalue)
  cutoff_F <- temp$Cutoff_FScore
  
  # prediction
  pred_prob <- predict(model, newdata = testset)
  yhat <- ifelse(pred_prob>cutoff_F, 1, 0)
  
  # pseudo R-squared
  pR2 <- pR2(model)[4] # -- McFadden Pseudo R-squared
  threshold <- max(length(which(yhat==1))/length(yhat),
                   length(which(yhat==0))/length(yhat))
  
  return_value = list("Cutoff" = cutoff_F, "Prediction" = yhat, "PseudoR2" = pR2, "Threshold" = threshold)
  return(return_value)
}
