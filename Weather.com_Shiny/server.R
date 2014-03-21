library(shiny)
library(tseries)
library(ggplot2)
library(plm)

# Define server logic required to generate and plot a random distribution
shinyServer(function(input, output) {
  
  dataset <- dget("WeatherUnitsDataSet.dput")
  #dataset<-dataset[,-which(colnames(dataset)=="Date")] # remove date
  dataset<-cbind(dataset[,c(1:8)],dataset[,ncol(dataset)],dataset[,c(9:(ncol(dataset)-1))])
  colnames(dataset)[9]<-"Flu"
  
  dataset$Date<-as.Date(dataset$Date, "%m/%d/%y")
  # Expression that generates a plot of the distribution. The expression
  # is wrapped in a call to renderPlot to indicate that:
  #
  #  1) It is "reactive" and therefore should be automatically 
  #     re-executed when inputs change
  #  2) Its output type is a plot 
  #
  
  
  output$plot <- renderPlot({
    # removing variables from the dataset so they aren't included in the model
    
    #now just to start I'm going to delete every other units column besides soup
    
    #add selector to UI and then delete all columns from 10 onwards that do not have colname=selector
    units<-dataset[,which(colnames(dataset)==input$predictUnits)]
    dataset<-dataset[,-c(11:ncol(dataset))]
    dataset<-cbind(dataset,units)
    ###experiment
    dataset$Orig<-c(rep("ATL_actual",156),rep("BOS_actual",156),rep("CHI_actual",156),rep("DAL_actual",156),
                    rep("DET_actual",156),rep("LA_actual",156),rep("MIN_actual",156),rep("NYC_actual",156),
                    rep("PHX_actual",156),rep("SEA_actual",156))
    
    if (!input$inT){
      dataset<-dataset[,-which(colnames(dataset)=="T")]
    }    
    if (!input$inTd){
      dataset<-dataset[,-which(colnames(dataset)=="Td")]
    }
    if (!input$inDFN){
      dataset<-dataset[,-which(colnames(dataset)=="DFN")]
    }
    if (!input$inPrecip){
      dataset<-dataset[,-which(colnames(dataset)=="Precip")]
    }
    if (!input$inHumidity){
      dataset<-dataset[,-which(colnames(dataset)=="Humidity")]
    }
    if (!input$inWind){
      dataset<-dataset[,-which(colnames(dataset)=="Wind")]
    }
    if (!input$inX..Cloud){
      dataset<-dataset[,-which(colnames(dataset)=="X..Cloud")]
    }
    if (!input$inFlu){
      dataset<-dataset[,-which(colnames(dataset)=="Flu")]
    }
    
    #remove cities from the dataset so they aren't included in the model
    if (!input$inATL){
      dataset<-dataset[-which(dataset$CITY=="ATL"),]
    }
    if (!input$inBOS){
      dataset<-dataset[-which(dataset$CITY=="BOS"),]
    }
    if (!input$inCHI){
      dataset<-dataset[-which(dataset$CITY=="CHI"),]
    }
    if (!input$inDAL){
      dataset<-dataset[-which(dataset$CITY=="DAL"),]
    }
    if (!input$inDET){
      dataset<-dataset[-which(dataset$CITY=="DET"),]
    }
    if (!input$inLA){
      dataset<-dataset[-which(dataset$CITY=="LA"),]
    }
    if (!input$inMIN){
      dataset<-dataset[-which(dataset$CITY=="MIN"),]
    }
    if (!input$inNYC){
      dataset<-dataset[-which(dataset$CITY=="NYC"),]
    }
    if (!input$inPHX){
      dataset<-dataset[-which(dataset$CITY=="PHX"),]
    }
    if (!input$inSEA){
      dataset<-dataset[-which(dataset$CITY=="SEA"),]
    }
    
    fmla <- as.formula(paste(colnames(dataset)[ncol(dataset)-1], paste(colnames(dataset)[2:(ncol(dataset)-3)],collapse="+"),sep="~"))

    model<-plm(fmla,data=dataset,index="CITY")
    
    X<-dataset[,c(2:(ncol(dataset)-3))]
    X<-as.matrix(X,ncol=ncol(X))
    yhat<-X %*% model$coef
    fixed<-NULL
    fixed<-rep(fixef(model), each=156)
    yhat<-yhat+fixed
    dataset$yhat<-yhat
    p<-ggplot(dataset)+geom_line(aes(x=Date,y=yhat,color=CITY))+
      geom_line(aes(x=Date,y=units,color=Orig))+
      ylab("Unit Predictions")+
      labs(title="Predictions for Selected Cities Using Selected Variables for Chosen Units")
    print(p)
  })
})