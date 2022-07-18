# EgyBest Movie Downloader

## How it work for developers

 ### Create by combine of pyqt and selenium
  - create design of the application with pyqt5 designer application
  - create module to scrap egybest by selenium and beutifull soup to get the source of the movie
  - combine between the module and design to make it work successfully
  
 ### The Problems that I faced
  - when you use another operation out of the application (in my case: run selenium to get movie source url)
  - when you try to scrap egybest will face the problems that is egybest show pop-up ads & if you use adblocker egybest detect it
  
 ### The Solutions
  - Use the thread that make you to run more than one operation at the same time (e.g: run more funtion in the same time)
  - for more detail about threads: https://realpython.com/intro-to-python-threading/ && https://realpython.com/python-pyqt-qthread/
  
  - use unefective way that close each page that display (this make the operations slower) but I didn't find another way to skip it.
  
  


## How it work for enduser
 - search for movie on egybest
 - choose quality 
 - download the movie 
