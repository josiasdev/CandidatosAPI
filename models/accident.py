from pydantic import BaseModel
from datetime import datetime

class AccidentBase(BaseModel):
    chv_localidade: str # link para Eentidade Localidades
    data_acidente: datetime 
    uf_acidente: str
    dia_semana: str 
    fase_dia: str 
    tp_acidente: str
    cond_meteorologica: str
    hora_acidente: int # 073000
    cond_pista: str # 'SECA' 
    tp_cruzamento: str # 'NAO INFORMADO' 
    tp_pavimento: str 
    tp_curva: str  
    qtde_acid_com_obitos: int
    qtde_envolvidos: int 
    qtde_feridosilesos: int
    qtde_obitos: int

class AccidentCreateMixin(BaseModel):
    num_acidente: str

class AccidentPublicMixin(BaseModel):
    id: str
    num_acidente: str

class AccidentCreate(AccidentBase, AccidentCreateMixin):
    pass

class AccidentPublic(AccidentBase, AccidentPublicMixin):
    pass

class AccidentUpdate(BaseModel): 
    chv_localidade: str | None = None
    data_acidente: datetime | None = None
    uf_acidente: str | None = None
    dia_semana: str | None = None
    fase_dia: str | None = None
    tp_acidente: str | None = None
    cond_meteorologica: str | None = None
    hora_acidente: int | None = None
    cond_pista: str | None = None
    tp_cruzamento: str | None = None
    tp_pavimento: str | None = None
    tp_curva: str | None = None
    qtde_acid_com_obitos: int | None = None
    qtde_envolvidos: int | None = None
    qtde_feridosilesos: int | None = None
    qtde_obitos: int | None = None