from flask import Blueprint, render_template, request, Response, abort
from app.models.label_model import LABEL_REGISTRY, get_label_definition
from app.services.barcode_service import generate_code39_svg

label_bp = Blueprint("labels", __name__, url_prefix="/etiquetas")

@label_bp.route("/<label_type>", methods=["GET"], strict_slashes=True)
def show_form(label_type: str):
    """
    Renders the visual interactive form for a specific label type.
    """
    if label_type not in LABEL_REGISTRY:
        abort(404)
        
    label_def = get_label_definition(label_type)
    return render_template(
        f"etiquetas/form_{label_type.replace('-', '_')}.html",
        label=label_def,
        active_nav=label_type,
        labels_list=LABEL_REGISTRY.values()
    )

@label_bp.route("/imprimir/<label_type>", methods=["GET", "POST"], strict_slashes=True)
def print_label(label_type: str):
    """
    Renders the popup print view formatted specifically for thermal/label printers.
    Uses 'mm' for dimensional layout and 'pt' for typography.
    """
    if label_type not in LABEL_REGISTRY:
        abort(404)
        
    label_def = get_label_definition(label_type)
    req_data = request.form if request.method == "POST" else request.args
    
    # Extract data from request; all fields are required
    data = {}
    missing_fields = []
    for key in label_def.default_data.keys():
        val = req_data.get(key, "").strip()
        if not val:
            missing_fields.append(key)
        data[key] = val
        
    if missing_fields:
        abort(400, description=f"Debe completar todos los campos antes de imprimir. Faltantes: {', '.join(missing_fields)}")
            
    # Generate Code 39 SVG for the material code
    barcode_val = data.get("codigo_material", "0")
    if label_type == "caja-individual-utm":
        barcode_svg = generate_code39_svg(barcode_val, bar_width=0.6, bar_height=22.0)
    else:
        barcode_svg = generate_code39_svg(barcode_val, bar_width=1.0, bar_height=30.0)

    # Cantidad de copias de la etiqueta física a imprimir (mínimo 1)
    try:
        cant_eti = max(1, int(req_data.get("cantEti", 1)))
    except (ValueError, TypeError):
        cant_eti = 1

    return render_template(
        "etiquetas/print_label.html",
        label_type=label_type,
        label=label_def,
        data=data,
        barcode_svg=barcode_svg,
        cantEti=cant_eti
    )

@label_bp.route("/barcode/<value>", methods=["GET"], strict_slashes=True)
def get_barcode(value: str):
    """
    Direct endpoint returning a pure Code 39 SVG barcode.
    """
    bar_width = request.args.get("width", default=1.1, type=float)
    bar_height = request.args.get("height", default=30.0, type=float)
    svg_content = generate_code39_svg(value, bar_width=bar_width, bar_height=bar_height)
    return Response(svg_content, mimetype="image/svg+xml")
