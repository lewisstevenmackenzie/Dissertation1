from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionRepeatValues(Action):

    def name(self) -> Text:
        return "action_repeat_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        studyField = tracker.get_slot("studyField")
        
        language = tracker.get_slot("language")

        codingAbility = tracker.get_slot("codingAbility")
        codingAbilityEnglish = ["minimal", "not good", "okay", "very good", "great"]


        msg = f"Okay, so you would like to study {studyField} and you are {codingAbilityEnglish[int(codingAbility)-1]} at coding. You also have said you are inerested in learning the {language} language. I will now search for some possible modules that fit this criteria."

        #msg2 = f"This is the Study field: {studyField} \nThis is the value for the coding ability: {codingAbility} \nThis is the language: {language}"

        dispatcher.utter_message(text=msg)

        return [] 