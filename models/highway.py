from pydantic import BaseModel

class HighwayBase(BaseModel):
    num_acidente: str # link para Entidade Acidentes
    tp_rodovia: str
    cond_pista: str # SECA
    tp_cruzamento: str  # 'NAO INFORMADO' 
    tp_pavimento: str
    tp_curva: str
    lim_velocidade: str
    ind_guardrail: str