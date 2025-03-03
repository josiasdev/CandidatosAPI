from pydantic import BaseModel



class vehicleBase(BaseModel):
    num_acidente: int
    tipo_veiculo: str
    ind_veic_estrangeiro: str
    qtde_veiculos: int
    frota_total: int
    frota_circulante: int
    lim_velocidade: str
    tp_pista: str

class VehicleCreateMixin(BaseModel):
    num_acidente: int

class VehiclePublicMixin(BaseModel):
    id: str
    num_acidente: int

class VehicleCreate(vehicleBase, VehicleCreateMixin):
    pass

class VehiclePublic(vehicleBase, VehiclePublicMixin):
    pass

class VehicleUpdate(BaseModel): 
    tipo_veiculo: str | None = None
    ind_veic_estrangeiro: str | None = None
    qtde_veiculos: int | None = None
    frota_total: int | None = None
    frota_circulante: int | None = None
    lim_velocidade: str | None = None
    tp_pista: str | None = None