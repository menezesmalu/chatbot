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
        final_answer = response['hits']['hits'][0]['_source']['answer']
        

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

 
       