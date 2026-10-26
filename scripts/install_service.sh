#!/usr/bin/env bash
# ==============================================================================
# Teccam SGT - Instalador de Servicio Systemd
# Cumple con el estándar ASD-STE100 y principio de portabilidad anti-hardcode.
# ==============================================================================
set -euo pipefail

# 1. Comprobación de privilegios de superusuario
if [[ "${EUID}" -ne 0 ]]; then
  echo "[ERROR] Este script requiere privilegios de superusuario para instalar servicios systemd." >&2
  echo "[ACCION] Ejecute nuevamente con sudo: sudo $0" >&2
  exit 1
fi

# 2. Resolución dinámica de rutas y usuario (100% portable)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

SERVICE_USER="${SUDO_USER:-$(id -un)}"
SERVICE_GROUP="$(id -gn "${SERVICE_USER}")"

SERVICE_NAME="teccam-etiquetas.service"
TARGET_SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
TEMPLATE_FILE="${SCRIPT_DIR}/teccam-etiquetas.service.template"

PORT="${PORT:-8600}"
HOST="${HOST:-0.0.0.0}"
WORKERS="${WORKERS:-2}"

# 3. Comprobación determinista de precondiciones
echo "==> Verificando componentes requeridos en: ${PROJECT_DIR}"

if [[ ! -f "${PROJECT_DIR}/wsgi.py" ]]; then
  echo "[ERROR] No se encontró wsgi.py en ${PROJECT_DIR}." >&2
  exit 1
fi

if [[ ! -x "${PROJECT_DIR}/venv/bin/gunicorn" ]]; then
  echo "[ERROR] No se encontró el binario ejecutable gunicorn en ${PROJECT_DIR}/venv/bin/gunicorn." >&2
  echo "[ACCION] Asegúrese de crear el entorno e instalar dependencias:" >&2
  echo "        python3 -m venv ${PROJECT_DIR}/venv" >&2
  echo "        ${PROJECT_DIR}/venv/bin/pip install -r ${PROJECT_DIR}/requirements.txt" >&2
  exit 1
fi

if [[ ! -f "${TEMPLATE_FILE}" ]]; then
  echo "[ERROR] No se encontró la plantilla de servicio en ${TEMPLATE_FILE}." >&2
  exit 1
fi

# 4. Generación de la unidad systemd desde plantilla
echo "==> Configurando unidad systemd: ${SERVICE_NAME}"
echo "    - Usuario de ejecución : ${SERVICE_USER}"
echo "    - Grupo de ejecución   : ${SERVICE_GROUP}"
echo "    - Directorio de trabajo: ${PROJECT_DIR}"
echo "    - Escucha de red       : http://${HOST}:${PORT}"
echo "    - Workers WSGI         : ${WORKERS}"

sed \
  -e "s|{{PROJECT_DIR}}|${PROJECT_DIR}|g" \
  -e "s|{{SERVICE_USER}}|${SERVICE_USER}|g" \
  -e "s|{{SERVICE_GROUP}}|${SERVICE_GROUP}|g" \
  -e "s|{{PORT}}|${PORT}|g" \
  -e "s|{{HOST}}|${HOST}|g" \
  -e "s|{{WORKERS}}|${WORKERS}|g" \
  "${TEMPLATE_FILE}" > "${TARGET_SERVICE_FILE}"

chmod 644 "${TARGET_SERVICE_FILE}"

# 5. Activación e inicio en systemd
echo "==> Recargando daemon de systemd..."
systemctl daemon-reload

echo "==> Habilitando e iniciando servicio..."
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

# 6. Comprobación y reporte de estado
sleep 1
if systemctl is-active --quiet "${SERVICE_NAME}"; then
  echo "=============================================================================="
  echo "[OK] Servicio ${SERVICE_NAME} instalado y ejecutándose correctamente."
  echo "     Acceso Web: http://${HOST}:${PORT}/"
  echo "=============================================================================="
  echo "Comandos operativos útiles:"
  echo "  - Estado del servicio : sudo systemctl status ${SERVICE_NAME}"
  echo "  - Logs en tiempo real : sudo journalctl -u ${SERVICE_NAME} -f"
  echo "  - Reiniciar servicio  : sudo systemctl restart ${SERVICE_NAME}"
  echo "  - Detener servicio    : sudo systemctl stop ${SERVICE_NAME}"
  echo "  - Desinstalar servicio: sudo ${SCRIPT_DIR}/uninstall_service.sh"
  echo "=============================================================================="
else
  echo "[ADVERTENCIA] El servicio no se encuentra en estado 'active'." >&2
  echo "Ejecute para diagnosticar:" >&2
  echo "  sudo journalctl -u ${SERVICE_NAME} -n 30 --no-pager" >&2
  exit 1
fi
