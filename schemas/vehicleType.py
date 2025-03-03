from models.vehicleType import vehicleBase, VehiclePublic


def vehicle_entity(entity: dict) -> vehicleBase:
    return {
        "num_acidente": entity['num_acidente'],
        "tipo_veiculo": entity['tipo_veiculo'],
        "ind_veic_estrangeiro": entity['ind_veic_estrangeiro'],
        "qtde_veiculos": entity['qtde_veiculos'],
        "frota_total": entity['frota_total'],
        "frota_circulante": entity['frota_circulante'],
        "lim_velocidade": entity['lim_velocidade'],
        "tp_pista": entity['tp_pista']
    }


def vehicle_entity_from_db(entity: dict) -> VehiclePublic:
    vehicle = {
        'id': str(entity['_id']),
        **vehicle_entity(entity)
    }
    
    return VehiclePublic(**vehicle)

def vehicle_entities_from_db(entities: list) -> list[VehiclePublic]:
    return [vehicle_entity_from_db(entity) for entity in entities]

