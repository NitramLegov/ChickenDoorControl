import ConfigParser

config_filename = 'ChickenDoorControl.conf'

def defaultValues():
    configuration.add_section('Server')
    configuration.set('Server','PORT','8080')
    configuration.add_section('Doorcontrol')
    configuration.set('Doorcontrol','UP_PIN','21')
    configuration.set('Doorcontrol','DOWN_PIN','17')
    configuration.set('Doorcontrol','TIME','30')
    with open(config_filename, 'wb') as config_file:
        configuration.write(config_file)

configuration = ConfigParser.SafeConfigParser()

try:
    #with open('Asmo.conf','r') as config_file:
    configuration.read(config_filename)
    print(configuration.get('Server','port'))
except:
    defaultValues()




