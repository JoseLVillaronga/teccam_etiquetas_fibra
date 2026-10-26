"""Barcode generation service utilizing ReportLab.
Produces crisp, resolution-independent Code 39 SVG drawings.
"""
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics import renderSVG

def generate_code39_svg(
    value: str,
    bar_width: float = 1.1,
    bar_height: float = 32.0,
    checksum: bool = False
) -> str:
    """
    Generates a Code 39 barcode SVG string.

    Args:
        value: Alphanumeric string to encode.
        bar_width: Width of the narrowest bar (in points).
        bar_height: Height of the barcode bars (in points).
        checksum: Whether to include Mod 43 checksum (default False for standard Code 39).

    Returns:
        Clean SVG XML string.
    """
    # Clean value for Code 39 (uppercase alphanumeric + - . $ / + % and space)
    sanitized_value = "".join(c for c in str(value).upper() if c.isalnum() or c in "-.$/+% ")
    if not sanitized_value:
        sanitized_value = "0"

    drawing = createBarcodeDrawing(
        "Standard39",
        value=sanitized_value,
        barWidth=bar_width,
        barHeight=bar_height,
        checksum=checksum,
        humanReadable=False
    )
    
    return renderSVG.drawToString(drawing)
