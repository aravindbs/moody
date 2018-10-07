# Moody

**Moody** is a your very own personal mental health assistant. Whether you are sad, angry or depressed, Moody will have a a music/video suggestion for you that will immediately brighten up your day. 

## [Video Demonstration](http://bit.do/MoodySOK)

 

## Problem Statement  

A person’s emotions and moods have direct bearings on his/her daily activities.It is necessary to eliminate negative emotions that our family or friends might be experiencing. Analysing soial media 
posts is a good way to help improve ones mental health. 

## Tools used 

* Tweepy API to obtain tweets from Twitter. 
* Watson Tone Analyzer to obtain emotions and Natural Language Understanding System to get keywords. 
* Spotify API to suggest music. 
* Youtube API to suggest videos. 
* Watson Assistant as a chatbot for depressed users to communicate with. 
* WebApp built using Flask framework deployed on IBM Cloud Foundry. 

## Instructions to run the code locally 

1. Clone the repository.
2. Create a python virtual environment and activate it.
```
$ virtualenv -p python3 venv
$ . venv/bin/activate 
```
3. Install the requirements specified in requirements.txt 
```
$ pip install -r requirements.txt 
```
4. Download the .env file containing the requirent environment variables from [here](https://drive.google.com/file/d/18NHa9qQqnZXrhwduuJ6Pd6MeG8k9shKE/view?usp=sharing)
5. Place a copy of the .env file in the ```web``` and ```workers``` directories.

#### To start the web app.

``` 
$ cd web
$ python main.py
 ```
#### To start the workers.
```
$ cd workers
$ python <WORKER>.py 
```



## Motivation 

This project was carried out by students from R.V College of Engineering as a part of the IBM Hack Challenge. 

