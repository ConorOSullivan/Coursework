library(shiny)
library(plm)

#dataset <- datafd
dataset<-dget("WeatherUnitsDataSet.dput")

# Define UI for application that plots random distributions 
shinyUI(pageWithSidebar(
  
  # Application title
  headerPanel("Panel Linear Model"),
  
  # Sidebar with a slider input for number of observations
  sidebarPanel(
    selectInput('predictUnits', 'Units', colnames(dataset)[c(10,12,14,16,18,20,22,24,26,28)]),
    
    wellPanel(
      p(strong("Variables")),
      checkboxInput(inputId = "inT", label = "Temperature",     value = TRUE),
      checkboxInput(inputId = "inTd", label = "Dewpoint Temperature", value = FALSE),
      checkboxInput(inputId = "inDFN",  label = "Difference From Normal Temperature", value = FALSE),
      checkboxInput(inputId = "inPrecip", label = "Precipitation",    value = TRUE),
      checkboxInput(inputId = "inHumidity", label = "Humidity",     value = FALSE),
      checkboxInput(inputId = "inWind", label = "Wind",     value = FALSE),
      checkboxInput(inputId = "inX..Cloud", label = "% Cloud Cover",     value = FALSE),
      checkboxInput(inputId = "inFlu", label = "Flu Trends Data",     value = FALSE)
      
    ),
    
    wellPanel(
      p(strong("Cities")),
      checkboxInput(inputId = "inATL", label = "Atlanta",     value = TRUE),
      checkboxInput(inputId = "inBOS", label = "Boston", value = FALSE),
      checkboxInput(inputId = "inCHI",  label = "Chicago", value = FALSE),
      checkboxInput(inputId = "inDAL", label = "Dallas",    value = TRUE),
      checkboxInput(inputId = "inDET", label = "Detroit",    value = FALSE),
      checkboxInput(inputId = "inLA", label = "Los Angeles",     value = FALSE),
      checkboxInput(inputId = "inMIN", label = "Minneapolis",     value = FALSE),
      checkboxInput(inputId = "inNYC", label = "New York City",     value = FALSE),
      checkboxInput(inputId = "inPHX", label = "Phoenix",     value = FALSE),
      checkboxInput(inputId = "inSEA", label = "Seattle",     value = FALSE)
    )
    
  ),
  mainPanel(
    
    plotOutput("plot", height="7in")
  )
  
  
))