# 🏷️ Teccam SGT - Sistema de Generación e Impresión de Etiquetas

Sistema web modular para la gestión, parametrización e impresión de etiquetas de fibra óptica y trazabilidad industrial en planta. Diseñado bajo arquitectura de producción desacoplada (Flask + Gunicorn + Systemd), con soporte 100% autónomo (offline-first) y maquetación de alta fidelidad milimétrica para impresoras térmicas de etiquetas (Zebra / compatibles).

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Especificaciones de Etiquetas Soportadas](#-especificaciones-de-etiquetas-soportadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
  - [Entorno de Desarrollo](#entorno-de-desarrollo)
  - [Variables de Entorno](#variables-de-entorno)
- [Despliegue Operativo con Systemd](#-despliegue-operativo-con-systemd)
  - [Instalación del Servicio](#instalación-del-servicio)
  - [Comandos de Gestión Operativa](#comandos-de-gestión-operativa)
  - [Desinstalación Limpia](#desinstalación-limpia)
- [Ejecución de Pruebas](#-ejecución-de-pruebas)
- [Guía de Diagnóstico y Resolución Rápida (3 AM)](#-guía-de-diagnóstico-y-resolución-rápida-3-am)

---

## ✨ Características Principales

* **Renderizado Térmico Preciso:** Plantillas CSS maquetadas con unidades físicas exactas (`mm` para geometrías y márgenes de corte, `pt` para tipografía), eliminando descalces en cabezales térmicos.
* **Generación Vectorial de Código de Barras:** Motor nativo basado en ReportLab para códigos Code 39 en formato SVG puro, nítidos en cualquier resolución de impresión (203 dpi / 300 dpi) y sin llamadas a APIs externas.
* **Operatividad Offline (Air-Gapped):** Cero dependencias externas en tiempo de ejecución. Tailwind CSS y recursos estáticos alojados localmente en el servidor.
* **Validación Determinista:** Validación estricta en servidor de todos los campos de etiqueta previo a generar la orden de impresión (evita impresiones en blanco o defectuosas en línea de ensamblaje).
* **Servicio de Grado Productivo:** Entrypoint WSGI optimizado para Gunicorn con reinicio automático bajo fallas gestionado por systemd.

---

## 🏷️ Especificaciones de Etiquetas Soportadas

| Identificador (`type_id`) | Nombre Operativo | Dimensiones | Código de Barras | Campos Principales |
| :--- | :--- | :--- | :--- | :--- |
| `caja-individual-utm` | Caja Individual UTM | **102 mm × 30 mm** | Code 39 (Material) | Código material, descripción, UTM, cantidad, derivada, peso |
| `caja-intermedia-ut1` | Caja Intermedia UT1 | **102 mm × 60 mm** | Code 39 (Material) | Código material, descripción, UTM, cantidad (6), W/X/Y/Z, derivada, peso |
| `caja-intermedia-ut2` | Caja Intermedia UT2 | **102 mm × 60 mm** | Code 39 (Material) | Código material, descripción, UTM, cantidad (24), W/X/Y/Z, derivada, peso |
| `pallet-utw` | Pallet UTW (Movistar) | **102 mm × 153 mm** | Code 39 (Material) | Empresa, Centro Logístico Avellaneda, pedido/derivada, cantidad (96), peso |

---

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura MVC modular con separación estricta de responsabilidades:

```text
.
├── app/
│   ├── __init__.py           # Application Factory (create_app), blueprints y context processors
│   ├── config.py             # Configuración desacoplada leída desde variables de entorno
│   ├── controllers/          # Controladores HTTP (Blueprints)
│   │   ├── home_controller.py   # Vista principal y telemetría de planta
│   │   ├── label_controller.py  # Formularios, validación y endpoint de impresión
│   │   └── error_controller.py  # Manejador determinista de errores 404 / 500
│   ├── models/               # Modelos de dominio y registro de especificaciones
│   │   ├── label_model.py       # Registro canónico LABEL_REGISTRY y dimensiones
│   │   └── ot_model.py          # Métricas y KPIs de órdenes de trabajo (OTs)
│   ├── services/             # Servicios desacoplados de dominio
│   │   └── barcode_service.py   # Generador ReportLab Code 39 a SVG
│   ├── static/               # Assets locales (CSS, logos, iconos, favicons)
│   └── templates/            # Plantillas Jinja2
│       ├── base.html            # Layout maestro con navegación activa
│       ├── home/                # Panel de control e indicadores
│       ├── etiquetas/           # Formularios y modal de impresión térmica
│       └── errors/              # Vistas de error 404/500
├── scripts/
│   ├── install_service.sh    # Instalador systemd dinámico y portable (root)
│   ├── uninstall_service.sh  # Desinstalador limpio de servicios systemd (root)
│   ├── teccam-etiquetas.service.template # Plantilla parametrizable de systemd
│   └── generate_favicon.py   # Generador de favicon e iconos estáticos
├── tests/
│   └── test_app.py           # Suite exhaustiva de pruebas unitarias y de integración
├── requirements.txt          # Dependencias mínimas fijadas
├── run.py                    # Runner unificado (modo desarrollo o producción)
└── wsgi.py                   # Hook WSGI estándar para servidores de aplicaciones
```

---

## ⚙️ Requisitos del Sistema

* **Sistema Operativo:** Linux (Debian, Ubuntu o derivados con systemd).
* **Python:** Versión 3.10 o superior con módulo `venv`.
* **Impresora:** Impresora térmica para etiquetas continuas o troqueladas con soporte de 102 mm de ancho (Zebra ZD420/ZT230 o similares).

---

## 🚀 Instalación y Puesta en Marcha

### Entorno de Desarrollo

1. **Clonar el repositorio y situarse en el directorio raíz:**
   ```bash
   git clone <URL_REPOSITORIO> etiquetas-fibra
   cd etiquetas-fibra
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias requeridas:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor de desarrollo:**
   ```bash
   python3 run.py --dev
   ```
   El sistema quedará accesible en: `http://localhost:8600`

### Variables de Entorno

El sistema permite personalizar su comportamiento mediante variables de entorno estándar:

| Variable | Valor por Defecto | Descripción |
| :--- | :--- | :--- |
| `PORT` | `8600` | Puerto TCP de escucha del servidor web. |
| `HOST` | `0.0.0.0` | Dirección IP de escucha de red. |
| `WORKERS` | `2` | Cantidad de procesos worker para Gunicorn en producción. |
| `FLASK_DEBUG`| `0` | Modo depuración (`1` activa recarga en caliente y trazas). |
| `SECRET_KEY` | *(generada por defecto)* | Clave de firma para sesiones Flask. |

---

## 🛡️ Despliegue Operativo con Systemd

Para entornos de producción en planta, el sistema provee scripts portables que instalan el servicio como unidad de systemd sin rutas absolutas prefijadas.

### Instalación del Servicio

Ejecutar con permisos de superusuario:
```bash
sudo ./scripts/install_service.sh
```

El instalador:
1. Detecta automáticamente la ruta del proyecto y el usuario de ejecución real.
2. Comprueba la presencia del entorno virtual y del binario de Gunicorn.
3. Parametriza la plantilla `scripts/teccam-etiquetas.service.template`.
4. Copia el archivo a `/etc/systemd/system/teccam-etiquetas.service`.
5. Habilita (`systemctl enable`) e inicia (`systemctl start`) el daemon.

### Comandos de Gestión Operativa

| Acción | Comando |
| :--- | :--- |
| **Ver estado operativo** | `sudo systemctl status teccam-etiquetas.service` |
| **Inspeccionar logs en vivo** | `sudo journalctl -u teccam-etiquetas.service -f` |
| **Reiniciar servicio** | `sudo systemctl restart teccam-etiquetas.service` |
| **Detener servicio** | `sudo systemctl stop teccam-etiquetas.service` |

### Desinstalación Limpia

Para retirar completamente el servicio del sistema:
```bash
sudo ./scripts/uninstall_service.sh
```

---

## 🧪 Ejecución de Pruebas

El proyecto cuenta con una suite de pruebas automatizadas que valida:
- Disponibilidad offline de assets (Tailwind CSS).
- Integridad de formularios y placeholders dinámicos.
- Validación estricta de parámetros al solicitar impresión.
- Generación de etiquetas con medidas dimensionales en `mm` y códigos Code 39 en SVG.
- Control estricto de rutas y manejo de errores 404.

Para ejecutar la suite completa:
```bash
venv/bin/python3 -m unittest discover tests
```

---

## 🚨 Guía de Diagnóstico y Resolución Rápida (3 AM)

Procedimientos directos de contingencia bajo el estándar ASD-STE100:

| Síntoma / Error | Causa Determinista | Acción Inmediata de Mitigación |
| :--- | :--- | :--- |
| **El servicio no inicia:** `gunicorn: not found` | Entorno virtual ausente o dependencias no instaladas. | Ejecutar: `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt` |
| **Error HTTP 400 al solicitar impresión** | Parámetros obligatorios vacíos o no enviados en la petición. | Completar todos los campos del formulario antes de pulsar "Imprimir Etiqueta". |
| **Error HTTP 404 en rutas antiguas** (`/analisisOts.php`) | Ruta obsoleta retirada por estricta modularización. | Navegar a la raíz `/` para acceder a los formularios vigentes desde el menú principal. |
| **Etiqueta desfasada en la impresora** | Configuración de papel incorrecta en el driver o navegador. | En el diálogo de impresión: seleccionar tamaño personalizado correspondiente (102×30mm, 102×60mm o 102×153mm) y márgenes en "Ninguno". |
| **Fallo de enlace a puerto 8600** (`Address already in use`) | Proceso huérfano bloqueando el puerto. | Ejecutar: `sudo fuser -k 8600/tcp` y luego reiniciar el servicio con `sudo systemctl restart teccam-etiquetas.service`. |
