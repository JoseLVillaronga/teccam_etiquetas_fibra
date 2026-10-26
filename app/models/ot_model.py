from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class OtMetricModel:
    """Domain model providing telemetry and analysis metrics for Work Orders (OTs)."""

    @classmethod
    def get_dashboard_data(cls) -> Dict[str, Any]:
        """
        Returns structured chart and KPI data replicating the Teccam SGT dashboard.
        Strict typing and deterministic format for view presentation.
        """
        return {
            "title": "Cantidad de OTs (Acumulado cada 10 minutos)",
            "subtitle": "Análisis temporal de órdenes de trabajo en planta",
            "time_axis_label": "Tiempo",
            "y_axis_label": "Cantidad de OTs (Acumulado cada 10 minutos)",
            "y_ticks": [0, 5, 10, 15, 20, 25],
            "timestamps": [
                {"full": "13:10 Oct 26, 2026", "short": "13:10", "date": "Oct 26, 2026"},
                {"full": "13:20", "short": "13:20", "date": ""},
                {"full": "13:30", "short": "13:30", "date": ""},
                {"full": "13:40", "short": "13:40", "date": ""},
                {"full": "13:50", "short": "13:50", "date": ""},
                {"full": "14:00", "short": "14:00", "date": ""},
            ],
            "series": [
                {
                    "id": "acumulado_total",
                    "name": "Tendencia Total",
                    "color": "#111827",
                    "line_style": "dotted",
                    "values": [16.0, 25.0, 21.5, 21.0, 26.5, 12.0]
                },
                {
                    "id": "linea_azul",
                    "name": "Línea Principal (Azul)",
                    "color": "#4f46e5",
                    "line_style": "solid",
                    "values": [16.0, 23.5, 20.0, 6.0, 11.2, 18.0]
                },
                {
                    "id": "linea_amarilla",
                    "name": "Línea Intermedia (Amarilla)",
                    "color": "#eab308",
                    "line_style": "solid",
                    "values": [None, 4.2, 3.5, 14.8, 17.5, None]
                },
                {
                    "id": "linea_roja",
                    "name": "Línea Alerta (Roja)",
                    "color": "#ef4444",
                    "line_style": "solid",
                    "values": [None, None, None, None, 3.5, 2.8]
                }
            ],
            "kpis": [
                {
                    "label": "OTs Procesadas",
                    "value": "142",
                    "change": "+12%",
                    "positive": True,
                    "badge": "Turno Tarde"
                },
                {
                    "label": "En Ejecución",
                    "value": "18",
                    "change": "Normal",
                    "positive": True,
                    "badge": "Activas"
                },
                {
                    "label": "Tiempo Promedio",
                    "value": "24 min",
                    "change": "-8%",
                    "positive": True,
                    "badge": "Óptimo"
                },
                {
                    "label": "Eficiencia de Línea",
                    "value": "97.4%",
                    "change": "+1.8%",
                    "positive": True,
                    "badge": "Excelente"
                }
            ]
        }
