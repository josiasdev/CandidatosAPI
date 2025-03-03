from pydantic import BaseModel

class LocalityBase(BaseModel):
    chv_localidade: str
    ano_referencia: str
    mes_referencia: str
    mes_ano_referencia: str
    regiao: str
    uf: str
    codigo_ibge: str
    municipio: str
    regiao_metropolitana: str
    qtde_habitantes: str