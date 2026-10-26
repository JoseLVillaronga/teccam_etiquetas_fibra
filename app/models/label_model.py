"""Domain models and specifications for printing labels."""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class LabelDefinition:
    type_id: str
    name: str
    short_name: str
    width_mm: int
    height_mm: int
    default_data: Dict[str, Any]

LABEL_REGISTRY: Dict[str, LabelDefinition] = {
    "caja-individual-utm": LabelDefinition(
        type_id="caja-individual-utm",
        name="Etiqueta para caja individual UTM",
        short_name="Caja Individual UTM",
        width_mm=102,
        height_mm=30,
        default_data={
            "codigo_material": "10202520294",
            "descripcion": "CBL Drop Precon OPTITAP 100m Low-friction",
            "utm": "1",
            "cantidad": "1",
            "derivada": "904xxxxxx",
            "peso": "1,10 kg",
        }
    ),
    "caja-intermedia-ut1": LabelDefinition(
        type_id="caja-intermedia-ut1",
        name="Etiqueta caja intermedia UT1",
        short_name="Caja Intermedia UT1",
        width_mm=102,
        height_mm=60,
        default_data={
            "codigo_material": "10202520294",
            "descripcion": "CBL Drop Precon OPTITAP 100m Low-friction",
            "utm": "1",
            "cantidad": "6",
            "pres_w": "000",
            "pres_x": "000",
            "pres_y": "006",
            "pres_z": "001",
            "derivada": "904xxxxxx",
            "peso": "6,60 kg",
        }
    ),
    "caja-intermedia-ut2": LabelDefinition(
        type_id="caja-intermedia-ut2",
        name="Etiqueta caja intermedia UT2",
        short_name="Caja Intermedia UT2",
        width_mm=102,
        height_mm=60,
        default_data={
            "codigo_material": "10202520294",
            "descripcion": "CBL Drop Precon OPTITAP 100m Low-friction",
            "utm": "1",
            "cantidad": "24",
            "pres_w": "000",
            "pres_x": "004",
            "pres_y": "006",
            "pres_z": "001",
            "derivada": "904xxxxxx",
            "peso": "26,40 kg",
        }
    ),
    "pallet-utw": LabelDefinition(
        type_id="pallet-utw",
        name="Etiqueta para pallet UTW",
        short_name="Pallet UTW",
        width_mm=102,
        height_mm=153,
        default_data={
            "empresa": "Tasa ó Movi",
            "pedido_derivada": "940XXXXXXX",
            "codigo_material": "10202520294",
            "descripcion_linea1": "CBL Drop Precon OPTITAP 100m",
            "descripcion_linea2": "Low-friction",
            "utm": "1",
            "cantidad": "96",
            "pres_w": "004",
            "pres_x": "004",
            "pres_y": "006",
            "pres_z": "001",
            "peso_pallet": "105,06 kg",
        }
    ),
}

def get_label_definition(label_type: str) -> LabelDefinition:
    """Retrieve label definition by slug or raise KeyError."""
    return LABEL_REGISTRY[label_type]
