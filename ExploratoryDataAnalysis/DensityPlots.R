# Code for exercise 4
# This should produce two plots as described in ex 4a,b
# exchange_density_a.png
# exchange_density_b.png
exchange_rate_densities <- function() {
  require(Ecdat)
  data(Garch)#include the data and proper package
  firstdiff<-diff(Garch$dy)
  #the same length as the frame
  m<-mean(firstdiff)#take statistics from original exchange rates
  s<-sd(firstdiff)
  j<-data.frame(firstdiff)
  g1<-ggplot(j)+
    geom_density(aes(x=firstdiff))+
    stat_function(fun=dnorm,#add normal distribution
                  args=list(mean=m, sd=s), 
                  linetype="dashed", 
                  color="red")
  ggsave("exchangeratedensity1.png",g1) #save plot
  g1
  
  md<-median(firstdiff)#take additional statistics
  mad<-mad(firstdiff) #MAD
  g2<-ggplot(j) +
    geom_density(aes(x=firstdiff)) +
    stat_function(fun=dnorm,
                  args=list(mean=md, sd=mad), 
                  linetype="dashed", 
                  color="red")
  ggsave("exchangeratedensity2.png",g2) #save plot
  g2
  
}
exchange_rate_densities()