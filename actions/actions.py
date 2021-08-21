# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from elasticsearch import Elasticsearch
from rasa_sdk.events import SlotSet
from random import randrange

MOVIES = {
    "documentary": [
        "Athelete A" ,
        "Three Identical Strangers",
        "Behind the Curve",
        "Hot Girls Wanted",
        "homecoming",
        "the dawn wall"
    ],
    "adventure": [
        "Black Widow",
        "Fast and Furious",
        "Passengers",
        "Interstellar",
        "Fantastic Beasts",
        "Captain Marvel"
    ],
    "animation":[
        "Frozen",
        "Luca",
        "Coco",
        "Big Hero 6",
        "The Lion King",
        "Barbie as the Princess and the Pauper"
    ],
    "comedy":[
        "Ocean's 8",
        "Pitch Perfect",
        "Dr. Dolittle",
        "Clueless",
        "Legally Blonde",
        "Baywatch"
    ],
    "horror": [
        "The Conjuring",
        "Get Out",
        "The Unholy",
        "IT",
        "Anabelle"
    ],
    "drama": [
        "Little Women",
        "Life is Beautiful," 
        "Disobedience",
        "Dunkirk",
        "The Imitation Game",
        "The Greatest Showman",
        "Me Before You"
    ]
}

class ActionGetFunFact(Action):
    def name(self) -> Text:
        return "action_get_fun_fact"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        es = Elasticsearch(HOST="http://localhost", PORT=9200)

        question = tracker.latest_message['text']
        body = {
            "from":0,
            "size":100,
            "query": {
                "match": {
                    "question":question
                }
            }
        }
        response = es.search(index="movies_index", body=body)
        first_answer_score = response['hits']['hits'][0]['_score']
        second_answer_score = response['hits']['hits'][1]['_score']
        final_answer = ""
        if first_answer_score >= 2*second_answer_score:
            final_answer = response['hits']['hits'][0]['_source']['answer']
        else:
            question = response['hits']['hits'][0]['_source']['question']
            answer = response['hits']['hits'][0]['_source']['answer']
            final_answer = f"Hmmm, I didn't find exactly what you're looking for! But look what I found for \n\"{question}\"\n{answer}"
        
        dispatcher.utter_message(text=final_answer)

        return []

class ResetSlotWOA(Action):

    def name(self):
        return "action_reset_woa"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("WORK_OF_ART", None)]

class ResetSlotTickets(Action):

    def name(self):
        return "action_reset_tickets"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("CARDINAL", None)]

class ResetSlotGPA(Action):

    def name(self):
        return "action_reset_gpe"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("GPE", None)]

class ResetSlotGenre(Action):

    def name(self):
        return "action_reset_genre"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("GENRE", None)]
    
class ActionSuggestMovie(Action):

    def name(self) -> Text:
        return "action_suggest_movie"
    
    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:
        
        selected_genre = tracker.get_slot("GENRE")
        print(selected_genre)

        if selected_genre in MOVIES:
            movies = MOVIES[selected_genre]
            random_movie = movies[randrange(len(movies))]

        else:
            random_movie = None

        print("random_movie")
        print(random_movie)
        if(random_movie == None):
            dispatcher.utter_message(response="utter_genre_not_found", GENRE=selected_genre)
        else:
            dispatcher.utter_message(response="utter_suggest_movie", WORK_OF_ART=random_movie)

        return []
