from pydantic import BaseModel


class RequeteConnexion(BaseModel):
    username : str
    password : str

class TokenReponse(BaseModel): 
    access_token : str
    token_type : str


    