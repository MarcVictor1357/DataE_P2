import os
import requests
from datetime import datetime
import time

# Définition de l'adresse de l'API
# (Il est important d'utiliser le nom du container et non une IP chiffrée, car on ne connaît pas l'IP qui sera celle de ce container dans le network.)
api_address = 'api_a_tester'
# port de l'API
api_port = 8000

# Les valeurs de test
username = 'alice'
password = 'wonderland'
# Valeurs qui doivent donner 0
age_test1 = 30
gluc_test1 = 70
bmi_test1 = 30
gendr_test1 = "female"
smoking_test1 = "neversmoked"
# Valeurs qui doivent donner 1
age_test2 = 110
gluc_test2 = 150
bmi_test2 = 95
gendr_test2 = "male"
smoking_test2 = "smokes"
# Réponses attendues
reponseattendue1 = "LR - Pour les valeurs entrées, la prédiction de stroke est : négative (risque de stroke non identifié)."
reponseattendue2 = "LR - Pour les valeurs entrées, la prédiction de stroke est : positive (risque de stroke identifié)."


time.sleep(24)


# Requêtes
now = datetime.now()
r1 = requests.get(
        url='http://{address}:{port}/lrpred?username={username}&password={password}&age={age}&gluc={gluc}&bmi={bmi}&gendr={gendr}&smoking={smoking}'.format
            (address=api_address, port=api_port, username=username, password=password, age=age_test1, gluc=gluc_test1, bmi=bmi_test1, gendr=gendr_test1, smoking=smoking_test1)
     )
r2 = requests.get(
        url='http://{address}:{port}/lrpred?username={username}&password={password}&age={age}&gluc={gluc}&bmi={bmi}&gendr={gendr}&smoking={smoking}'.format
            (address=api_address, port=api_port, username=username, password=password, age=age_test2, gluc=gluc_test2, bmi=bmi_test2, gendr=gendr_test2, smoking=smoking_test2)
     )


# Affichage du résultat
output = '''=========================================================
    LRPRED - Relevance test at {now}
=========================================================
   Request done at "/lrpred" with age={age1}, gluc={gluc1}, bmi={bmi1}, gendr={gendr1}, smoking={smoking1} :
      expected result = {reponseattendue1}
      actual result   = {text1}
      ==>  {test_status1}
   Request done at "/lrpred" with age={age2}, gluc={gluc2}, bmi={bmi2}, gendr={gendr2}, smoking={smoking2} :
      expected result = {reponseattendue2}
      actual result   = {text2}
      ==>  {test_status2}
'''

text1 = (r1.text).strip('"')
text2 = (r2.text).strip('"')

if text1 == reponseattendue1:
    test_status1 = 'SUCCESS'
else:
    test_status1 = 'FAILURE'
if text2 == reponseattendue2:
    test_status2 = 'SUCCESS'
else:
    test_status2 = 'FAILURE'

print(output.format(now=now,
                    age1=age_test1, gluc1=gluc_test1, bmi1=bmi_test1, gendr1=gendr_test1, smoking1=smoking_test1, reponseattendue1=reponseattendue1, text1=text1, test_status1=test_status1,
                    age2=age_test2, gluc2=gluc_test2, bmi2=bmi_test2, gendr2=gendr_test2, smoking2=smoking_test2, reponseattendue2=reponseattendue2, text2=text2, test_status2=test_status2
     ))

# impression dans un fichier
with open('/home/strokepred_test.log', 'a') as file:      # 'a' for appending
    file.write(output.format
               (now=now,
                age1=age_test1, gluc1=gluc_test1, bmi1=bmi_test1, gendr1=gendr_test1, smoking1=smoking_test1, reponseattendue1=reponseattendue1, text1=text1, test_status1=test_status1,
                age2=age_test2, gluc2=gluc_test2, bmi2=bmi_test2, gendr2=gendr_test2, smoking2=smoking_test2, reponseattendue2=reponseattendue2, text2=text2, test_status2=test_status2
               ))

