from typing import Any, Text, Dict, List

from recommendation.descriptionRecommender import *
from recommendation.keywordRecommender import *

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted
from rasa_sdk.executor import CollectingDispatcher

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        events.append(ActionExecuted("utter_greet"))

        return events
    
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
        file_path = os.path.join(cur_path, '..\\dataset\\modulesMovieStyle2.csv')
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
                     
                    msg =  msg +  f"The module is worth {row['Credits']} credits and is SCQF Level {row['SCQF Level']}."

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
        file_path = os.path.join(cur_path, '..\\dataset\\modulesMovieStyle2.csv')

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

class ActionsendStaffEmail(Action):

    def name(self) -> Text:
        return "action_send_staff_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        cur_path = os.path.dirname(__file__)
        file_path = os.path.join(cur_path, '..\\dataset\\staffEmails.csv')

        staffMemeber = tracker.get_slot("staffEmail")
        intent = tracker.get_intent_of_latest_message()
        flag = 1
        msg = f""        

        with open(file_path, newline='') as csvfile:
        
            reader = csv.DictReader(csvfile)
        
            for row in reader:
                if row['Name'].lower() == "visaemail" and intent == "visaQuestions":
                    msg = msg + f"I'm sorry, I am only a chatbot. For further assistance regarding Visa's please contact {row['Email']}.\n"
                elif intent =="staffemail" and staffMemeber is not None:
                    if staffMemeber.lower() in row['Name'].lower():
                        msg = msg + f"This is {row['Name']}'s email address: {row['Email']}."
                        flag = 0

        if intent == "staffEmail" and flag == 1:
            msg = msg + "I am sorry, the name you have given does not appear in our system. Please can you try again?"
        dispatcher.utter_message(text=msg)

        return [] 
    
class ActionrecommendSimilarDescription(Action):

    def name(self) -> Text:
        return "action_recommend_similar_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        moduleName = tracker.get_slot("module1")
        recommendedModule = recommend_module_based_on_description(moduleName)
        print(recommendedModule)

        msg = f"You made it to the recommender, This the module that is being recommended {recommendedModule}" 
        dispatcher.utter_message(text=msg)

        return [] 
    
    
class ActionrecommendSimilarKeywords(Action):

    def name(self) -> Text:
        return "action_recommend_similar_keywords"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        field = []
        keywords = []

        field.append(tracker.get_slot("studyField"))
        keywords.append(tracker.get_slot("language"))
        if (tracker.get_slot("keywords") is not None):
            keywords.append(tracker.get_slot("keywords"))

        recommendedModules = recommend_module_based_on_metadata('userModule', field, keywords)
        print(recommendedModules)

        msg = f"This module best suits your requirements {recommendedModules[0]}. " 
        
        # add code to check keywords are in he recommended module
        
        cur_path = os.path.dirname(__file__)
        file_path = os.path.join(cur_path, '..\\dataset\\modulesMovieStyle2.csv')

        with open(file_path, newline='') as csvfile:
        
            reader = csv.DictReader(csvfile)
        
            for row in reader:
                if (recommendedModules[0] == row['Module Name']):

                    for x in range(len(keywords)):
                        if (keywords[x].lower() in row['Keywords'].lower() or keywords[x].lower() in row['Fields'].lower()):
                            print(f"{keywords[x]} is present")
                        else:
                            print(f"{keywords[x]} is not present")
                            msg += f"Unfortunately the module does not cover {keywords[x]}. "
                    for x in range(len(field)):    
                        if (field[x].lower() in row['Fields'].lower() or field[x].lower() in row['Keywords'].lower()):
                            print(f"{field[x]} is present")
                        else:
                            print(f"{field[x]} is not present")
                            msg += f"Unfortunately the module does not cover {field[x]}. "


        msg += "\nRemember I am only a chatbot in early development. Please contact the module leader before signing up. "
        dispatcher.utter_message(text=msg)  

        return [SlotSet("module1", recommendedModules[0]), SlotSet("module2", recommendedModules[1]), SlotSet("module3", recommendedModules[2])] 
    
class ActionModuleLeaderQuery(Action):

    def name(self) -> Text:
        return "action_module_leader_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        cur_path = os.path.dirname(__file__)
        file_path = os.path.join(cur_path, '..\\dataset\\modulesMovieStyle2.csv')
        emails_file_path = os.path.join(cur_path, '..\\dataset\\staffEmails.csv')
        moduleName = tracker.get_slot("module1")

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
                    with open(emails_file_path, newline='') as csvfile2:        
                        reader2 = csv.DictReader(csvfile2)

                        for row2 in reader2:
                            if row2['Name'].lower() in row['Lecturer'].lower():
                                msg = msg + f"The {row['Module Name']} module is run by {row2['Name']}. You can contact them via email {row2['Email']}\n"

        dispatcher.utter_message(text=msg)

        return [] 
    

class ActionModuleDescription(Action):

    def name(self) -> Text:
        return "action_module_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        cur_path = os.path.dirname(__file__)
        file_path = os.path.join(cur_path, '..\\dataset\\modulesMovieStyle2.csv')
        moduleName = tracker.get_slot("module1")

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
                    
                    msg += f"This is the Description: \n{row['Description']}"

        dispatcher.utter_message(text=msg)

        return [] 


class ActionUpdateModule1(Action):

    def name(self) -> Text:
        return "update_module1_from_module2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        module1 = tracker.get_slot("module1")
        module2 = tracker.get_slot("module2")
        print(module1)
        print(module2)

        print('this is the module name: ' + module1)
        msg = f"Okay, does this module Sound more appealing? {module2}"


        dispatcher.utter_message(text=msg)

        return [SlotSet("module1", module2)] 
    

class ActionClearModuleSlots(Action):

    def name(self) -> Text:
        return "clear_module_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import os
        import csv

        msg = ""

        dispatcher.utter_message(text=msg)

        return [SlotSet("studyField", None), SlotSet("codingAbility", None), SlotSet("language", None)] 

class ActionHowCanIHelp(Action):

    def name(self) -> Text:
        return "action_how_can_i_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("userName")

        msg = f""        

        if (name == None):
            msg += "How can i help you?"
        else:
            msg += f"Feel free to ask me a question, {name}"

        dispatcher.utter_message(text=msg)

        return [] 