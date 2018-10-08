# Moody

**Moody** is your very own personal mental health assistant. Whether you are sad, angry or depressed, Moody will have a a music/video suggestion for you that will immediately brighten up your day. 

Try it out [here](https://moodysok.eu-gb.mybluemix.net)

## [Video Demonstration](http://bit.do/MoodySOK)

## Documentation 

* [Ideation Document](https://docs.google.com/document/d/10cHPoi-hURe-9KgCUaMn4O1NomwQwXzrUjMgpE3hf3Q/edit?usp=sharing)

* [Presentation](https://docs.google.com/presentation/d/1WWYKNfPc4-kDRt02e4NJjwnK9XX_VsG7kKFslJMYBIE/edit?usp=sharing)

## Problem Statement  

A person’s emotions and moods have direct bearings on his/her daily activities. It is necessary to eliminate negative emotions that our family or friends might be experiencing. Analysing soial media 
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
2. Create a python virtual environment from the root directory and activate it.
```
$ virtualenv -p python3 venv
$ . venv/bin/activate 
```
3. Install the requirements specified in requirements.txt 
```
$ pip install -r requirements.txt 
```
4. Download the env file containing the required environment variables from [here](https://drive.google.com/file/d/18NHa9qQqnZXrhwduuJ6Pd6MeG8k9shKE/view?usp=sharing)
5. Place a copy of the env file in the ```web``` and ```workers``` directories.

6. Rename the env file in both the directories to ```.env``` 

#### To start the web app.

``` 
$ cd web
$ python main.py
 ```

Open any browser window and type in [http://localhost:5000](http://localhost:5000)
#### To start the workers.
```
$ cd workers
$ python <WORKER>.py 
```
## Architecture

![Architecure](https://github.com/aravindbs/moody/blob/master/docs/architecture.png)

## Motivation 

This project was carried out by students from R.V College of Engineering as a part of the IBM Hack Challenge.