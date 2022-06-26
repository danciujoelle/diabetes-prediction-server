from pydantic import BaseModel

class User(BaseModel):
    n_pregnant: int
    glucose_conc: int
    bp: int
    skin_len: int
    insulin: int
    bmi: float
    pedigree_fun: float
    age: int