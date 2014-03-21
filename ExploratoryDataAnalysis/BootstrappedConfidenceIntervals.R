# Code for exercise 3
# Given a vector of numerical values returns the median and
# the 95% confidence interval for the median 
# Plot the density and the density of the resample medians
# in density_confidence_internal.png
median_confidence_interval <- function(x) {
  
  graphdataf<-data.frame(x=0)
  #bootstrapping algorithm for the median
  #repeat 1000 times
  y<-NULL
  for (i in 1:1000) {
    samp<-sample(x, length(x), replace=TRUE)
    y<-c(y,median(samp)) #continually append new medians
  }
  dataf<-data.frame(low_ci=0,median=0,high_ci=0)
  dataf$low_ci<-quantile(y,.025) #2.5% quartile of samples
  dataf$median<-median(x) #median of orig vector
  dataf$high_ci<-quantile(y,.975) #97.5% q of samples
  
  #create data.frame for plotting
  line1 <- data.frame(Name="Low_CI", vals=dataf$low_ci) #creating data frames
  line2 <- data.frame(Name="Median", vals=dataf$median) #to better display names
  line3 <- data.frame(Name="High_CI", vals=dataf$high_ci) #in ggplot2
  linedf<-rbind(line1,line2,line3) #collecting data frames together
  graphdataf<-data.frame(whichvec=factor(rep(c("origvector","medians"),
                         times=c(length(x),1000))),values=c(x,y)) 
  g<-ggplot(graphdataf, aes(x=values, fill=whichvec)) +
           geom_density(alpha=.3) +
           geom_vline(data=linedf, #here I use the data frame of vertical lines
                      aes(xintercept=vals, 
                          linetype=Name,
                          colour=Name),
                      show_guide = TRUE)
  ggsave("densityplot.png",g) #save plot
  dataf #print data.frame
}
