from pydantic import BaseModel
from datetime import date


class vehicleBase(BaseModel):
    num_acidente: int
    tipo_veiculo: str
    ind_veic_estrangeiro: str
    qtde_veiculos: int
    frota_total: int
    frota_circulante: int
    lim_velocidade: str
    tp_pista: str

