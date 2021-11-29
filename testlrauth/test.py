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
username1 = 'alice'
password1 = 'wonderland'
username2 = 'bob'
password2 = 'builder'
username3 = 'clementine'
password3 = 'mandarine'
username4 = 'stan'
password4 = 'getz'   # A bad one
age_test = 50
gluc_test = 100
bmi_test = 50
gendr_test = "male"
smoking_test = "unknown"

time.sleep(8)

# Requêtes
now = datetime.now()
r1 = requests.get(
        url='http://{address}:{port}/lrpred?username={username}&password={password}&age={age}&gluc={gluc}&bmi={bmi}&gendr={gendr}&smoking={smoking}'.format
            (address=api_address, port=api_port, username=username1, password=password1, age=age_test, gluc=gluc_test, bmi=bmi_test, gendr=gendr_test, smoking=smoking_test)
     )
r2 = requests.get(
        url='http://{address}:{port}/lrpred?username={username}&password={password}&age={age}&gluc={gluc}&bmi={bmi}&gendr={gendr}&smoking={smoking}'.format
            (address=api_address, port=api_port, username=username2, password=password2, age=age_test, gluc=gluc_test, bmi=bmi_test, gendr=gendr_test, smoking=smoking_test)
     )
r3 = requests.get(
        url='http://{address}:{port}/lrpred?username={username}&password={password}&age={age}&gluc={gluc}&bmi={bmi}&gendr={gendr}&smoking={smoking}'.format
            (address=api_address, port=api_port, username=username3, password=password3, age=age_test, gluc=gluc_test, bmi=bmi_test, gendr=gendr_test, smoking=smoking_test)
     )
r4 = requests.get(
        url='http://{address}:{port}/lrpred?username={username}&password={password}&age={age}&gluc={gluc}&bmi={bmi}&gendr={gendr}&smoking={smoking}'.format
            (address=api_address, port=api_port, username=username4, password=password4, age=age_test, gluc=gluc_test, bmi=bmi_test, gendr=gendr_test, smoking=smoking_test)
     )

# Affichage du résultat
output = '''=========================================================
    LRPRED - Authentication test at {now}
=========================================================
   Request done at "/lrpred" with username={username1} and password={password1} :
      expected result = 200
      actual result = {status_code1}
      ==>  {test_status1}
      {la_reponse1}
   Request done at "/lrpred" with username={username2} and password={password2} :
      expected result = 200
      actual result = {status_code2}
      ==>  {test_status2}
      {la_reponse2}
   Request done at "/lrpred" with username={username3} and password={password3} :
      expected result = 200
      actual result = {status_code3}
      ==>  {test_status3}
      {la_reponse3}
   Request done at "/lrpred" with username={username4} and password={password4} :
      expected result = 401
      actual result = {status_code4}
      ==>  {test_status4}
'''

status_code1 = r1.status_code
status_code2 = r2.status_code
status_code3 = r3.status_code
status_code4 = r4.status_code

if status_code1 == 200:
    test_status1 = 'SUCCESS'
    lareponse1 = "(And the answer is " + r1.text + ")"
else:
    test_status1 = 'FAILURE'
    lareponse1 = ""
if status_code2 == 200:
    test_status2 = 'SUCCESS'
    lareponse2 = "(And the answer is " + r2.text + ")"
else:
    test_status2 = 'FAILURE'
    lareponse2 = ""
if status_code3 == 200:
    test_status3 = 'SUCCESS'
    lareponse3 = "(And the answer is " + r3.text + ")"
else:
    test_status3 = 'FAILURE'
    lareponse3 = ""
if status_code4 == 401:
    test_status4 = 'SUCCESS'
else:
    test_status4 = 'FAILURE'

print(output.format(now=now,
                    username1=username1, password1=password1, status_code1=status_code1, test_status1=test_status1, la_reponse1=lareponse1,
                    username2=username2, password2=password2, status_code2=status_code2, test_status2=test_status2, la_reponse2=lareponse2,
                    username3=username3, password3=password3, status_code3=status_code3, test_status3=test_status3, la_reponse3=lareponse3,
                    username4=username4, password4=password4, status_code4=status_code4, test_status4=test_status4 ))

# impression dans un fichier
with open('/home/strokepred_test.log', 'a') as file:      # 'a' for appending
    file.write(output.format
               (now=now,
                username1=username1, password1=password1, status_code1=status_code1, test_status1=test_status1, la_reponse1=lareponse1,
                username2=username2, password2=password2, status_code2=status_code2, test_status2=test_status2, la_reponse2=lareponse2,
                username3=username3, password3=password3, status_code3=status_code3, test_status3=test_status3, la_reponse3=lareponse3,
                username4=username4, password4=password4, status_code4=status_code4, test_status4=test_status4 ))

