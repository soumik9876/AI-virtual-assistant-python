
from settings.settings import interaction_setting as it 
from settings.logs import *

def speak_voice(sentence):
    """" This function takes a text sentence and in return it will speak that sentence """
    try :
        from gtts import gTTS
        import os , playsound
        Gtts = gTTS(text=sentence,lang='en')
        logger.debug('Gtts setted')
        filename = 'voice.mp3'
        Gtts.save(filename)
        logger.debug('Gtts saved now will play the sound')
        playsound.playsound(filename)
        logger.debug('removeing file')
        os.remove(filename)
    except :
        logger.critical('Dependency error - (speak_voice): need gTTs ,playsound .')
        speak_text('You have some depenency missing sir unless i can not speak sir :( ')

def speak_text(sentence):
    """ It will takes a text sentence and reply as bot"""
    bot = '\n(^-^)-> '
    print(bot,sentence)

def speak(sentence):
    """This functin will determine if bot will speak or only reply"""
    if it['voice_reply'] or it['voice_read+voice_reply']:
        speak_voice(sentence)
    if it['text_reply']:
        speak_text(sentence)
    else :
        print('Sir your speaking and writing cabapity is disibled. Please enbale it from settings.')