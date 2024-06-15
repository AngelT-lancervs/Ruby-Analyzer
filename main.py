import datetime
import lexical_analyzer as lexical

github_user = input("Escriba su usuario de Github: \n")
date_hour = datetime.datetime.now()

lexical.save_tokens_to_log(github_user, date_hour)