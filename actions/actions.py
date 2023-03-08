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


        msg = f"Okay, so you would like to study {studyField} and you are {codingAbilityEnglish[int(codingAbility)-1]} at coding. You also have said you are interested in learning the {language} language. I will now search for some possible modules that fit this criteria."

        dispatcher.utter_message(text=msg)

        return [] 


class ActionModuleSpecifications(Action):

    def name(self) -> Text:
        return "action_module_specifications"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        cur_path = os.path.dirname(__file__)
        file_path = os.path.join(cur_path, '..\\dataset\\moduleInfoTest.csv')
        moduleName = tracker.get_slot("module")

        if moduleName is None:
            msg = "There was a non Type sent"

            dispatcher.utter_message(text=msg)
            return[]

        print('this is the module name: ' + moduleName)
        msg = ""

        with open(file_path, newline='') as csvfile:
        
            reader = csv.DictReader(csvfile)
        
            for row in reader:
                if (moduleName.lower() in row['Module Name'].lower()):
                    print(row['Module Code'], row['Module Name'])
                    
                    msg = f"The {row['Module Name']} module is run by {row['Lecturer']}. Here is some more information regarding the module.\n"

                    if (row['Coursework'] == "0"):
                        msg = msg + "This module does not contain a coursework element. "
                    else:
                        msg = msg + f"The module is {row['Coursework']}% coursework. "
                    
                    if (row['Exam'] == "0"):
                        msg = msg + "There is no exam element to this Module. "
                    else:
                        msg =msg + f"The exam portion of this module acounts for {row['Exam']}% of the final grade. "

                    if row['Class Test'] == "0":
                        msg = msg + "There will not be a class test for this module. "
                    else: 
                        msg = msg + f"The class test portion is {row['Class Test']}%. "
                    
                    if "n/a" in row['Prerequisites']:
                        msg = msg + "There are no prerequisites to study this module. "
                    else:
                        msg = msg + f"You must have passed {row['Prerequisites']} in order to take this module. "
                     
                    msg =  msg +  f"The module is worth {row['Credits']} credits and is SCQF Level {row['SCQF Level']}.\nModule Description:\n{row['Description']}"

        dispatcher.utter_message(text=msg)

        return [] 


class ActionListModules(Action):

    def name(self) -> Text:
        return "action_list_modules"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        cur_path = os.path.dirname(__file__)
        file_path = os.path.join(cur_path, '..\\dataset\\moduleInfoTest.csv')

        msg = f"This is a list of the modules available to you:\n"        

        with open(file_path, newline='') as csvfile:
        
            reader = csv.DictReader(csvfile)
        
            for row in reader:
                print(row['Module Code'], row['Module Name'])

                msg = msg + f"  {row['Module Name']}\n"

        dispatcher.utter_message(text=msg)

        return [] 



class ActionListStudyFields(Action):

    def name(self) -> Text:
        return "action_list_study_fields"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        cur_path = os.path.dirname(__file__)
        file_path = os.path.join(cur_path, '..\\dataset\\studyFields.csv')

        msg = f"This is a list of the possible fields you can Study Fields:\n"        

        with open(file_path, newline='') as csvfile:
        
            reader = csv.DictReader(csvfile)
        
            for row in reader:
                msg = msg + f"  {row['Study Fields']}\n"

        dispatcher.utter_message(text=msg)

        return [] 
