from pydantic import BaseModel
from datetime import date

class VictimBase(BaseModel):
    num_acidente: str  
    chv_localidade: str 
    data_acidente: date 
    uf_acidente: str
    ano_acidente: str
    mes_acidente: str 
    mes_ano_acidente: str 
    faixa_idade: str
    genero: str
    tp_envolvido: str
    gravidade_lesao: str
    equip_seguranca: str
    ind_motorista: bool # Era o motorista? SIM OU NAO
    susp_alcool: bool # SIM OU NAO
    qtde_envolvidos: int 
    qtde_feridosilesos: int
    qtde_obitos: int