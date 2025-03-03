from models.vehicleType import vehicleBase


def vehicle_entity(entity: dict) -> dict:
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