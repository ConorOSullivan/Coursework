# Code for exercise 1
# This should produce three plots
# Histogram for earconch measurements.
# histo_earconch.png
# Side-by-side box plots of the male and female earconch measurements.
# box_plot_earconch_gender.png
# Side-by-side histograms of the male and female earconch measurements.
# histo_earconch_gender.png
earconch_plots <- function() {

  conchhist<-ggplot(possum, aes(x=earconch))+geom_histogram(color="white")
  ggsave("conchhist.png",conchhist) #single histogram
  
  conchbox<-ggplot(possum, aes(x=sex, y=earconch))+geom_boxplot()+
            labs(title="Box Plot of Ear Conchs of Males and Females")
  ggsave("conchbox.png",conchbox) #side by side box plots
  
  conchtwohist<-ggplot(possum, aes(x=earconch))+geom_histogram(color="white")+
                facet_grid(. ~ sex) +
                labs(title="Histogram of Ear Conchs of Males (m) and Females (f)")
  ggsave("conchtwohist.png",conchtwohist) #side by side histograms

}
earconch_plots()