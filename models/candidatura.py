
from pydantic import BaseModel

# consulta_cand_2024.csv
class Candidatura(BaseModel):
    # Candidatura   
    sq_candidato: str # ID - id candidatura
    cd_eleicao: str # id eleicao. from eleicao como chave estrangeira
    sg_uf: str
    ds_cargo: str # Descricao CARGO
    nr_candidato: int # numero pra votar
    nr_partido: int # numero
    sg_partido: str # sigla
    nm_partido: str # nome do partido
    nr_turno: str # INDICA SE FOI OU NAO PARA SEGUNDO TURNO - QUANTOS ELEITOS FORAM PARA SEGUNDO TURNO
    tp_agremiacao: str
    ds_sit_tot_turno: str # NÃO ELEITO | ELEITO
    ds_motivo:str # from motivo_cassacao. descreve o motivo