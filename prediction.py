from fastapi import FastAPI
import uvicorn
import pickle
import numpy
from models import User
app=FastAPI()
model=pickle.load(open("modelupdated.pkl","rb"))

@app.post("/predict")
def predict(req:User):
    n_pregnant=req.n_pregnant
    glucose_conc=req.glucose_conc
    bp=req.bp
    skin_len=req.skin_len
    insulin=req.insulin
    bmi=req.bmi
    pedigree_fun=req.pedigree_fun
    age=req.age
    features=list([n_pregnant,glucose_conc,bp,skin_len,insulin,
    bmi,
    pedigree_fun,
    age])
    predict=model.predict([features])
    probab=model.predict_proba([features])
    # if(predict==1):
    #     return {"ans":"You have been tested positive with {} probability".format(probab[0][1])}
    # else:
    #     return {"ans":"You have been tested negative with {} probability".format(probab[0][0])}
    return {"Outcome": predict.tolist()}

if __name__=="__prediction__":
    uvicorn.run(app)