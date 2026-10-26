#!/usr/bin/env bash
# ==============================================================================
# Teccam SGT - Desinstalador de Servicio Systemd
# ==============================================================================
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "[ERROR] Este script requiere privilegios de superusuario para desinstalar el servicio." >&2
  echo "[ACCION] Ejecute nuevamente con sudo: sudo $0" >&2
  exit 1
fi

SERVICE_NAME="teccam-etiquetas.service"
TARGET_SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"

echo "==> Deteniendo servicio ${SERVICE_NAME}..."
systemctl stop "${SERVICE_NAME}" 2>/dev/null || true

echo "==> Deshabilitando servicio ${SERVICE_NAME}..."
systemctl disable "${SERVICE_NAME}" 2>/dev/null || true

if [[ -f "${TARGET_SERVICE_FILE}" ]]; then
  echo "==> Eliminando archivo de servicio ${TARGET_SERVICE_FILE}..."
  rm -f "${TARGET_SERVICE_FILE}"
fi

echo "==> Recargando daemon de systemd..."
systemctl daemon-reload
systemctl reset-failed 2>/dev/null || true

echo "=============================================================================="
echo "[OK] Servicio ${SERVICE_NAME} desinstalado completamente del sistema."
echo "=============================================================================="
