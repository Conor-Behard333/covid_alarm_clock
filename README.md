# Covid Alarm Clock
## Introduction
This program is an alarm clock which when alarms are activated notifies the user with covid, weather and news updates.

## Installation
This program uses the text to speech module pyttsx3, the requests module, the flask module and 
the UK Covid 19 module. 

To run the program you need to make sure that these modules are installed by doing: 
```bash
pip install pyttsx3 
```
```bash
pip install requests
```
```bash
pip install flask
```
```bash
pip install uk-covid19
```

## Getting started tutorial
To start the program run main.py in the terminal from the project directory using:
```bash
python main.py
```
In a browser go to 127.0.0.1:5000
 
You will then be able to set the date and label (title) for your alarm. 
If you want news updates for that particular alarm then you can select the news checkbox. Similarly, if you want
weather updates for that alarm then you can select the weather checkbox. The alarm will then be displayed on the left
hand side, showing the title, when the alarm is set and if there will be any news/weather updates. 

Clicking the 'X' at the top of the alarm or notification will remove it.

Once the alarm goes off, the covid updates will be announced and if the news and/or the weather checkboxes were selected
then those notification will be listed on right hand side.

The covid announcement will mention the current cases for that day in the UK and the number of overall cases in the UK.  

In news notifications the title, description and source of the article will be displayed in the content as well as a link
that will open the news article in another tab.

In weather notifications the current temperature and what temperature it feels like is displayed.

## Testing
```bash
pip install pytest 
```
```bash
python -m pytest
```
## Developer documentation
### Using the config file
#### API keys
In the config file under "API_Keys" set "weather_key" and "news_key" to the appropriate API key. 

#### News API
In the config file you can set which country to search the news by setting the "country" key. You can also pre-define the 
search term for the type of news articles you search for by setting the "search_term" key. 

#### Weather API
In the config file you can set which country you want to get the weather for by setting the "country" key. You can also
set the city you want to get the weather for by setting the "city_name" key. Finally, you can set the units you want
the api to return by setting the "units" key to either metric (Centigrade) or imperial (Fahrenheit).

## Details
Author: Conor Behard Roberts

Github Repo: [here](https://github.com/Conor-Behard333/covid_alarm_clock.git)

Licence: [MIT](https://choosealicense.com/licenses/mit/)