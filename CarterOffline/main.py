from JanexPT import *
from Janex import *
from carterpy import Carter

class CarterOffline:
    def __init__(self, intents_file_path, thesaurus_file_path, UIName, CarterAPI):
        self.intents_file_path = intents_file_path
        self.thesaurus_file_path = thesaurus_file_path
        self.UIName = UIName
        self.CarterAPI = CarterAPI
        self.matcher = JanexPT(intents_file_path, thesaurus_file_path, UIName)
        self.intentm = IntentMatcher(intents_file_path, thesaurus_file_path)

    def SendToCarter(self, input_string, User):
        carter = Carter(self.CarterAPI)
        response = carter.say(input_string, User)
        intent_class = self.matcher.pattern_compare(input_string, User)
        intents = self.intentm.train()

        for intent in intents['intents']:
            if intent.get("tag") == intent_class.get("tag"):
                intent_class.setdefault("patterns", []).append(input_string)
                intent_class.setdefault("responses", []).append(response.output_text)

        with open(self.intents_file_path, 'w') as json_file:
            json.dump(intents, json_file, indent=4, separators=(',', ': '))

        return response.output_text
