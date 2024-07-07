import datetime
import analyzers.lexical_analyzer as lexical
import analyzers.syntax_analyzer as syntax

github_user = input("Ingrese su usuario de GitHub: \n")
date_hour = datetime.datetime.now()

#lexical.save_tokens_to_log(github_user, date_hour)