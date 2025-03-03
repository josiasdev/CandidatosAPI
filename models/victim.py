from pydantic import BaseModel
from datetime import date

class VictimBase(BaseModel):
    #Dados tratados
    num_acidente: str  
    chv_localidade: str 
    data_acidente: date 
    uf_acidente: str
    ano_acidente: str
    mes_acidente: str 
    faixa_idade: str
    genero: str
    gravidade_lesao: str
    equip_seguranca: str
    ind_motorista: bool
    tp_envolvido: str
    susp_alcool: str