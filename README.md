# About the script
This is a web scraping script, written in python, that helped me to look for available padel courts, but it can be used for any sports.  
Basically the script sends messages on a Telegram group with all the courts-slots displayed on a list, each court has its own booking link.   
I scraped the italian application "Prenota un campo" --> https://www.prenotauncampo.it/

In order to parallelize more activities, and thus be faster, I decided to split the project in two scripts: the first has to scrape from 1st to the 4th day forward, the second from the 5th to 12nd day
### Built With
Python  
Selenium webdriver

### Usage
In order to automate the scripts I decided to create 2 batch files (1 for each .py file) and set a windows scheduled task to run in the background the scripts.  
[see my basic batch file](Run_Script_0-4days.bat)
