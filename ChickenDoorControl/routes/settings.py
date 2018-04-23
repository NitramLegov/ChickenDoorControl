import web
import controller.settings as settings
import json

class Settings(object):
    """description of class"""

    def GET(self):
        return json.dumps(settings.configuration)

    def GET(self,section=None,setting=None):
        if section != '':
            if setting == None:
                return json.dumps(settings.configuration.items(section))
            else:
                return json.dumps(settings.configuration.get(section,setting))
        else:
            returnDict = {}
            for section in  settings.configuration.sections():
                returnDict[section] = settings.configuration.items(section)
            return json.dumps(returnDict)
        
