try :
    from tools.assistant import ask_question
    from tools.AI.data import data , youtube , wiki , google , youtube_play , goto_keys  
    from tools.AI.data import install_keys , calc_keys , should_not_learn
    from tools.wiki_search import wiki_search 
    from settings.logs import *
    from tools.browser.search import *
    from tools.browser.goto import find_goto_address
    from system.install import install , command 
    from system.screen_text import command_sep
    from tools.string_processing import is_matched
    from tools.json_manager import JsonManager
    from tools.calculation import google_calculation
    from tools.run_program import if_run_type
    from system.notifications import notify
    from settings.settings import bot , DEBUG
    from tools.shell import if_shell_type
    from tools.OJ.cp import if_cp_type
    from termcolor import cprint
    from tools.downloader import wget_downloader
    import os
except Exception as e:
    print(e)

def check(msg,mp,need = 90):
    logger.debug('check->' + msg)
    for word in mp :
        if is_matched(word,msg,need):
            return True
    return False


def rep(msg,mp):
    msg = msg.lower()
    # for key in mp :
    #     for word in key:
    #         for w in msg:
    #             if w == word:
    #                 w = word
    # return msg.strip().capitalize()
    for word in mp :
        if word in msg:
            return msg.replace(word,'',1).strip()
    return msg.strip()

def ai(msg,orginal_path) :
    """ Little ai for reacting to the msg.
        Written by Saurav-Paul"""
    logger.debug('Processing with ai')
    msg = msg.replace('  ',' ')
    msg = msg.replace(bot['name'],'')
    msg = msg.replace(bot['name'].lower(),'')
    msg = msg.replace(bot['name'].capitalize(),'')
    reply = "I don't know what to do, sir ."
    # print('you said ' , msg, bot['name'])
    if if_cp_type(msg):
        return 'Good luck sir.'
    if if_shell_type(msg):
        return 'Good luck sir.'
    if if_run_type(msg):
        return 'Good luck sir.'
    else :
        try :
            msg = msg.strip().lower()
            for line in data :
                if is_matched(msg,line,95):
                    reply = data[line]
                    return reply
            # logger.info('Not found in common data')
            # from history
            try :
                f = orginal_path+'/tools/AI/.learnt'
                history = JsonManager.json_read(f)
                for line in history:
                    if is_matched(msg,line,95):
                        logging.info('Learnt this before')
                        return history[line]

            except :
                logging.error("Can't read history file")
            if(check(msg,['change dir','change directory','chdir','-cd'],100)):
                # print(os.getcwd())
                cprint('Enter the path: ','cyan',end='')
                path = input()
                os.chdir(path)
                return 'Directory changed.'
            if check(msg,youtube_play):
                msg = rep(msg,youtube_play)
                logger.info(msg)
                find_goto_address(msg)
                reply = 'Enjoy sir. :D'
            elif check(msg,goto_keys):
                msg = rep(msg,goto_keys)
                find_goto_address(msg)
                reply = 'check browser'
                notify('Check Browser',':D',t=5)
            elif check(msg,youtube):
                msg = rep(msg,youtube)
                search_youtube(msg)
                reply = 'check browser.'
                notify('Check Browser',':D',t=5)
            elif check(msg,wiki):
                msg = rep(msg,wiki)
                # search_wiki(msg)
                msg = 'en.wikipedia.org '+msg
                find_goto_address(msg)
                reply = 'check browser.'
                notify('Check Browser',':D',t=5)
            elif msg == 'download':
                cprint('Enter the url : ','cyan',end='')
                url = input()
                wget_downloader(url)
                reply = 'Done.'
            elif check(msg,google):
                msg = rep(msg,google)
                # print('here = ',msg)
                search_google(msg)
                reply = 'check browser.'
                notify('Check Browser',':D',t=5)
            elif check(msg,install_keys):
                msg = rep(msg,install_keys)
                reply = install(msg)
            elif check(msg,calc_keys):
                msg = rep(msg,calc_keys)
                reply = google_calculation(msg)
                if reply == "sorry":
                    search_google(msg)
                    reply = "check browser"
                    notify('Check Browser',':D',t=5)
            else :
                if 0 and 'cmd:' in msg or '-s' in msg:
                    msg = rep(msg,{'cmd:'})
                    msg = rep(msg,{'-s'})
                    command_sep()
                    command(msg.lower())
                    command_sep()
                    reply = 'done sir'
                else :
                    reply = ask_question(msg)
                    ok = True
                    for word in should_not_learn:
                        if word in msg or word in reply:
                            ok = False
                            break
                    
                    if ok:
                        logger.info('reply -> ' + reply)
                        if DEBUG:
                            learn = input('.......Press y to learn it.....')
                        else :
                            learn = 'y'
                        if learn.lower() == 'y':
                            try :
                                history.update({msg:reply})
                                JsonManager.json_write(f,history)
                                logger.info('Learnt')
                            except Exception as e:
                                logger.info("Exception while writing learnt : "+e)
            return reply
        except Exception as e:
            logger.info('Getting some error in ai')
            logger.info(e)
            return reply

