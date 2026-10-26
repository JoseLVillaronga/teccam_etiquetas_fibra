import unittest
from pathlib import Path
from urllib.parse import urlencode
from app import create_app
from app.models.label_model import LABEL_REGISTRY

class TestTeccamApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_tailwind_asset_exists_locally(self):
        """Verifies that the Tailwind CDN file is downloaded and present locally for 100% offline usage."""
        tailwind_path = Path(__file__).resolve().parent.parent / "app" / "static" / "vendor" / "tailwind" / "tailwind.js"
        self.assertTrue(tailwind_path.exists(), "Local tailwind.js should exist")
        self.assertGreater(tailwind_path.stat().st_size, 100000, "Tailwind file should be non-trivial size")

    def test_home_page_status_and_content(self):
        """Tests that GET / returns 200 and includes Teccam SGT branding and navigation."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Sistema de gestión Teccam", html)
        self.assertIn('SGT, desarrollo de "Teccam S.R.L."', html)
        self.assertIn("info@teccamsrl.com.ar", html)
        self.assertIn("Inicio", html)
        self.assertIn("Etiquetas", html)
        self.assertIn("Caja individual UTM", html)
        self.assertIn("Pallet UTW", html)

    def test_all_label_forms_render_with_placeholders_and_empty_values(self):
        """Tests that all 4 label form views render with placeholders instead of pre-filled values."""
        routes = [
            "/etiquetas/caja-individual-utm",
            "/etiquetas/caja-intermedia-ut1",
            "/etiquetas/caja-intermedia-ut2",
            "/etiquetas/pallet-utw",
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed")
            html = response.get_data(as_text=True)
            self.assertIn('value=""', html)
            self.assertIn("placeholder=", html)
            self.assertIn("Imprimir Etiqueta", html)
            self.assertIn("errorBanner", html)

    def test_pallet_utw_form_has_movistar_branding(self):
        """Tests that Pallet UTW form includes Centro Logístico Avellaneda and Movistar styling."""
        response = self.client.get("/etiquetas/pallet-utw")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Centro Logístico", html)
        self.assertIn("Avellaneda", html)
        self.assertIn("Para Empresa", html)
        self.assertIn("movistar_logo.png", html)

    def test_print_popup_validation_rejects_empty_fields(self):
        """Tests that attempting to print without required fields returns 400 Bad Request."""
        # Missing all parameters
        response = self.client.get("/etiquetas/imprimir/caja-individual-utm")
        self.assertEqual(response.status_code, 400)
        
        # Partially filled parameters
        response = self.client.get("/etiquetas/imprimir/caja-individual-utm?codigo_material=10202520294")
        self.assertEqual(response.status_code, 400)

    def test_print_popup_utm(self):
        """Tests the UTM print popup view with mm/pt units, auto-print, and Code 39 barcode."""
        data = LABEL_REGISTRY["caja-individual-utm"].default_data
        url = f"/etiquetas/imprimir/caja-individual-utm?{urlencode(data)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("102mm", html)
        self.assertIn("30mm", html)
        self.assertIn("pt", html)
        self.assertIn("window.print()", html)
        self.assertIn("window.close()", html)
        self.assertIn("<svg", html)  # Code 39 SVG barcode embedded

    def test_print_popup_pallet_utw(self):
        """Tests the Pallet UTW print popup view."""
        data = LABEL_REGISTRY["pallet-utw"].default_data
        url = f"/etiquetas/imprimir/pallet-utw?{urlencode(data)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("102mm", html)
        self.assertIn("153mm", html)
        self.assertIn("Centro Logístico", html)
        self.assertIn("Avellaneda", html)
        self.assertIn("movistar_logo.png", html)

    def test_barcode_endpoint(self):
        """Tests the Code 39 barcode SVG endpoint."""
        response = self.client.get("/etiquetas/barcode/10202520294")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/svg+xml")
        self.assertIn(b"<svg", response.data)

    def test_custom_404_page(self):
        """Tests strict routing: unmapped route returns 404 status and custom error template."""
        response = self.client.get("/ruta-totalmente-inexistente-1234")
        self.assertEqual(response.status_code, 404)
        html = response.get_data(as_text=True)
        self.assertIn("Ruta No Encontrada", html)
        self.assertIn("Error HTTP 404", html)

    def test_invalid_label_returns_404(self):
        """Tests that invalid label type returns 404."""
        response = self.client.get("/etiquetas/etiqueta-inexistente-xyz")
        self.assertEqual(response.status_code, 404)

    def test_analisis_ots_php_route_returns_404(self):
        """Tests that legacy route /analisisOts.php has been removed and returns 404."""
        response = self.client.get("/analisisOts.php")
        self.assertEqual(response.status_code, 404)
        response_extless = self.client.get("/analisisOts")
        self.assertEqual(response_extless.status_code, 404)

if __name__ == "__main__":
    unittest.main()
