import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import joblib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from fastapi.responses import HTMLResponse


# creating a FastAPI server
strokepred_server = FastAPI(title='Stroke pred User API')


# creating a response class for predictions
class PredResponse(BaseModel):
    response: str = 'Intentionally empty'


def correct_user_and_pswd(username,password):
    if (username=="alice"      and password=="wonderland") or\
       (username=="bob"        and password=="builder") or\
       (username=="clementine" and password=="mandarine"):
        return True
    else:
        return False


@strokepred_server.get('/status')
async def get_status():
    """Returns 1
    """
    return 1


@strokepred_server.get('/lrpred')
async def get_lrpred(username,password,age,gluc,bmi,gendr,smoking):
    """Returns the prediction of stroke disease, according to a Linear Regression prediction model.<br>
       Parameters:<br>
       &nbsp;&nbsp;&nbsp;username: str    -Authorized user of this service<br>
       &nbsp;&nbsp;&nbsp;password: str    -Password of authorized user<br>
       &nbsp;&nbsp;&nbsp;age: float    -Age of the tested person<br>
       &nbsp;&nbsp;&nbsp;gluc: float   -Average glucose level of the tested person<br>
       &nbsp;&nbsp;&nbsp;bmi: float    -BMI of the tested person<br>
       &nbsp;&nbsp;&nbsp;gendr: str (male/female/other)   -Gender of the tested person<br>
       &nbsp;&nbsp;&nbsp;smoking (optional): str (formerlysmoked/neversmoked/smokes/unknown)   -Smoking status of the tested person<br>
    """
    lareponse = PredResponse()
    # Verif user authorization
    if not correct_user_and_pswd(username,password):
        raise HTTPException(
            status_code=401,
            detail='Unauthorized.')
    # Input verification and transformation
    if (age.isnumeric()):
        age = (float(age) - 0.08) / (82.0 - 0.08)
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'age' should be numeric.")
    if (gluc.isnumeric()):
        avg_glucose_level = (float(gluc) - 55.12) / (271.74 - 55.12)
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'gluc' should be numeric.")
    if (bmi.isnumeric()):
        bmi = (float(bmi) - 10.3) / (97.6 - 10.3)
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'bmi' should be numeric.")
    if (gendr == "male"):
        gender = 0
    elif (gendr == "female"):
        gender = 1
    elif (gendr == "other"):
        gender = 2
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'gendr' doesn't have a valid content ('male', 'female' or 'other').")
    if (smoking == "formerlysmoked"):
        smoking_num = 2
    elif (smoking == "neversmoked"):
        smoking_num = 1
    elif (smoking == "smokes"):
        smoking_num = 3
    elif (smoking == "unknown"):
        smoking_num = 0
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'smoking' doesn't have a valid content ('formerlysmoked', 'neversmoked', 'smokes' or 'unknown').")

    # Launch predictive algorithm
    #    LR - Régression logistique
    #    On charge le modèle ML sauvegardé
    LeModeleLR = joblib.load('/home/ModelStrokeMF_P2_LR2.sav')
    #     La prédiction (LR) sur le cas entré en input :
    X_test_API_LR = [[age,avg_glucose_level,bmi,gender,smoking_num]]
    y_pred_API_LR = LeModeleLR.predict(X_test_API_LR)
    if (y_pred_API_LR[0]==0):
        lareponse.response = "LR - Pour les valeurs entrées, la prédiction de stroke est : négative (risque de stroke non identifié)."
    elif (y_pred_API_LR[0]==1):
        lareponse.response = "LR - Pour les valeurs entrées, la prédiction de stroke est : positive (risque de stroke identifié)."
    else:
        lareponse.response = "LR - IMPOSSIBLE IMPOSSIBLE IMPOSSIBLE IMPOSSIBLE IMPOSSIBLE"
    return lareponse.response


@strokepred_server.get('/knnpred')
async def get_knnpred(username,password,age,gluc,bmi,gendr,smoking):
    """Returns the prediction of stroke disease, according to a KNN prediction model.<br>
       Parameters:<br>
       &nbsp;&nbsp;&nbsp;username: str    -Authorized user of this service<br>
       &nbsp;&nbsp;&nbsp;password: str    -Password of authorized user<br>
       &nbsp;&nbsp;&nbsp;age: float    -Age of the tested person<br>
       &nbsp;&nbsp;&nbsp;gluc: float   -Average glucose level of the tested person<br>
       &nbsp;&nbsp;&nbsp;bmi: float    -BMI of the tested person<br>
       &nbsp;&nbsp;&nbsp;gendr: str (male/female/other)   -Gender of the tested person<br>
       &nbsp;&nbsp;&nbsp;smoking (optional): str (formerlysmoked/neversmoked/smokes/unknown)   -Smoking status of the tested person<br>
    """
    lareponse = PredResponse()
    # Verif user authorization
    if not correct_user_and_pswd(username,password):
        raise HTTPException(
            status_code=401,
            detail='Unauthorized.')
    # Input verification and transformation
    if (age.isnumeric()):
        age = (float(age) - 0.08) / (82.0 - 0.08)
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'age' should be numeric.")
    if (gluc.isnumeric()):
        avg_glucose_level = (float(gluc) - 55.12) / (271.74 - 55.12)
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'gluc' should be numeric.")
    if (bmi.isnumeric()):
        bmi = (float(bmi) - 10.3) / (97.6 - 10.3)
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'bmi' should be numeric.")
    if (gendr == "male"):
        gender = 0
    elif (gendr == "female"):
        gender = 1
    elif (gendr == "other"):
        gender = 2
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'gendr' doesn't have a valid content ('male', 'female' or 'other').")
    if (smoking == "formerlysmoked"):
        smoking_num = 2
    elif (smoking == "neversmoked"):
        smoking_num = 1
    elif (smoking == "smokes"):
        smoking_num = 3
    elif (smoking == "unknown"):
        smoking_num = 0
    else:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'smoking' doesn't have a valid content ('formerlysmoked', 'neversmoked', 'smokes' or 'unknown').")

    # Launch predictive algorithm
    #    KNN
    #    On charge le modèle ML sauvegardé
    LeModeleKNN = joblib.load('/home/ModelStrokeMF_P2_KNN2.sav')
    #    La prédiction (KNN) sur le cas entré en input :
    X_test_API_KNN = [[age,avg_glucose_level,bmi,gender,smoking_num]]
    y_pred_API_KNN = LeModeleKNN.predict(X_test_API_KNN)
    if (y_pred_API_KNN[0]==0):
        lareponse.response = "KNN - Pour les valeurs entrées, la prédiction de stroke est : négative (risque de stroke non identifié)."
    elif (y_pred_API_KNN[0]==1):
        lareponse.response = "KNN - Pour les valeurs entrées, la prédiction de stroke est : positive (risque de stroke identifié)."
    else:
        lareponse.response = "KNN - IMPOSSIBLE IMPOSSIBLE IMPOSSIBLE IMPOSSIBLE IMPOSSIBLE"
    return lareponse.response


# Afficher les performances LR :
@strokepred_server.get('/lrperf',response_class=HTMLResponse)
async def get_LR_perf():
    """Returns the Linear Regression prediction model performance
    """
    return (
        "<p style='font-size:14;font-family:\"Courier\"'>"+
        "Confusion matrix sur le set de test :<br>"+
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Prédits nég.&nbsp;&nbsp;Prédits pos.<br>"+
        "&nbsp;&nbsp;&nbsp;Nég. réels&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;681&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;259<br>"+
        "&nbsp;&nbsp;&nbsp;Pos. réels&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;188&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;752<br>"+
        "Balanced accuracy score : 0.7622340425531915<br>"+
        "Accuracy score : 0.7622340425531915<br>"+
        "F1 score : 0.7708867247565352<br>"+
        "</p>"
        )
    # On a choisi de sortir un HTML pour le visuel, mais on pourrait sortir un json, on le garde ci-dessous au cas où :
    #x = {"PositifsReels_predits_Negatifs": 196,
    #     "PositifsReels_correctementpredits": 744,
    #     "NegatifsReels_predits_Positifs": 254,
    #     "NegatifsReels_correctementpredits": 686,
    #     "Balanced_accuracy_score": 0.7606382978723405,
    #     "Accuracy_score": 0.7606382978723404,
    #     "F1_score": 0.7678018575851393
    #    }
    #return json.dumps(x,indent=4)


# Afficher les performances KNN :
@strokepred_server.get('/knnperf',response_class=HTMLResponse)
async def get_KNN_perf():
    """Returns the KNN prediction model performance
    """
    return (
        "<p style='font-size:14;font-family:\"Courier\"'>"+
        "Confusion matrix sur le set de test :<br>"+
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Prédits nég.&nbsp;&nbsp;Prédits pos.<br>"+
        "&nbsp;&nbsp;&nbsp;Nég. réels&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;827&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;113<br>"+
        "&nbsp;&nbsp;&nbsp;Pos. réels&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;940<br>"+
        "Balanced accuracy score : 0.9398936170212766<br>"+
        "Accuracy score : 0.9398936170212766<br>"+
        "F1 score : 0.9433015554440543<br>"+
        "</p>"
        )
    # On a choisi de sortir un HTML pour le visuel, mais on pourrait sortir un json, on le garde ci-dessous au cas où :
    #x = {"PositifsReels_predits_Negatifs": 0,
    #     "PositifsReels_correctementpredits": 940,
    #     "NegatifsReels_predits_Positifs": 113,
    #     "NegatifsReels_correctementpredits": 827,
    #     "Balanced_accuracy_score": 0.9398936170212766,
    #     "Accuracy_score": 0.9398936170212766,
    #     "F1_score": 0.9433015554440543
    #    }
    #return json.dumps(x,indent=4,separators=(", ",": ")).encode("utf-8")


