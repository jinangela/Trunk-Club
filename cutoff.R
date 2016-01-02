cutoff <- function(y,fitted)
{
  cut <- seq(0.05,0.95,0.05)
  performance <- matrix(0,nrow=length(cut),ncol=6)
  for(i in 1:length(cut))
  {
    performance[i,1] <- cut[i]
    temp <- perf(cut[i],y,fitted)
    performance[i,2] <- temp$Precision
    performance[i,3] <- temp$Recall
    performance[i,4] <- temp$F_Score
    performance[i,5] <- temp$trueNegatives
    performance[i,6] <- temp$ClassificationRate
    
  }
  
  cp <- data.frame(performance)
  colnames(cp) <- c("Cutoff", "Precision","Recall","F_Score","trueNegatives","ClassificationRate")
  mcp <- melt(cp, id.vars = "Cutoff", value.names = "Value", 
              variable.name = "Cutting_Point")
  ggplot(data = mcp, aes(x=Cutoff, y=value, group = Cutting_Point, colour = Cutting_Point)) + 
    geom_line() +
    xlab("Cutting Point") +
    ylab("Value") +
    ggtitle("Performance Analysis")
  
  # choose the cutoff by maximizing performance
  cut_cr = cp[which(cp$ClassificationRate==max(cp$ClassificationRate,na.rm=T))[1],1]
  cut_fscore = cp[which(cp$F_Score==max(cp$F_Score,na.rm=T))[1],1]
  cut_precision = cp[which(cp$Precision==max(cp$Precision,na.rm=T))[1],1]
  cut_recall = cp[which(cp$Recall==max(cp$Recall,na.rm=T))[1],1]
  
  return_value = list("Cutoff_ClassRate" = cut_cr, "Cutoff_Precision" = cut_precision,
                      "Cutoff_Recall" = cut_recall, "Cutoff_FScore" = cut_fscore)
  return(return_value)
}