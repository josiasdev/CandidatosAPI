from pydantic import BaseModel
from datetime import date

class AccidentBase(BaseModel):
    num_acidente: str 
    chv_localidade: str # link para Eentidade Localidades
    data_acidente: date 
    uf_acidente: str
    dia_semana: str 
    fase_dia: str 
    tp_acidente: str
    cond_meteorologica: str
    hora_acidente: str # '073000' 
    cond_pista: str # 'SECA' 
    tp_cruzamento: str # 'NAO INFORMADO' 
    tp_pavimento: str 
    tp_curva: str  
    qtde_envolvidos: int 
    qtde_feridosilesos: int
    qtde_obitos: int