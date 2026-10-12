# tests/test_converters.py
import os
import tempfile
import unittest
from pathlib import Path

from converters import tabular, images, documents, data
from converters.registry import (
    get_category_key_for_extension,
    get_supported_outputs,
    get_recommendations,
    convert_file
)

class TestFileConverters(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_registry_recommendations(self):
        recs_png = get_recommendations(".png")
        self.assertTrue(len(recs_png) > 0)
        formats = [r["format"] for r in recs_png]
        self.assertIn("WEBP", formats)

        recs_csv = get_recommendations(".csv")
        self.assertTrue(len(recs_csv) > 0)
        csv_formats = [r["format"] for r in recs_csv]
        self.assertIn("XLSX", csv_formats)

    def test_tabular_csv_to_json_and_parquet(self):
        sample_csv = Path(self.temp_dir) / "test.csv"
        sample_csv.write_text("id,name,score\n1,Alice,95\n2,Bob,88\n", encoding="utf-8")

        res_json = tabular.convert(str(sample_csv), "JSON", self.temp_dir)
        self.assertEqual(res_json.status, "success")
        self.assertTrue(Path(res_json.output_path).exists())

        res_parquet = tabular.convert(str(sample_csv), "PARQUET", self.temp_dir)
        self.assertEqual(res_parquet.status, "success")
        self.assertTrue(Path(res_parquet.output_path).exists())

    def test_image_png_to_jpg_webp_pdf(self):
        from PIL import Image
        sample_png = Path(self.temp_dir) / "test.png"
        img = Image.new("RGBA", (100, 100), color=(255, 0, 0, 128))
        img.save(sample_png)

        # PNG -> JPG (RGBA must flatten without crash)
        res_jpg = images.convert(str(sample_png), "JPG", self.temp_dir)
        self.assertEqual(res_jpg.status, "success")
        self.assertTrue(Path(res_jpg.output_path).exists())

        # PNG -> WEBP
        res_webp = images.convert(str(sample_png), "WEBP", self.temp_dir)
        self.assertEqual(res_webp.status, "success")
        self.assertTrue(Path(res_webp.output_path).exists())

        # PNG -> PDF (must not fail on alpha)
        res_pdf = images.convert(str(sample_png), "PDF", self.temp_dir)
        self.assertEqual(res_pdf.status, "success")
        self.assertTrue(Path(res_pdf.output_path).exists())

    def test_structured_data_json_yaml_toml(self):
        sample_json = Path(self.temp_dir) / "config.json"
        sample_json.write_text('{"app": "OmniConverter", "version": "1.0", "active": true}', encoding="utf-8")

        # JSON -> YAML
        res_yaml = data.convert(str(sample_json), "YAML", self.temp_dir)
        self.assertEqual(res_yaml.status, "success")
        self.assertTrue(Path(res_yaml.output_path).exists())

        # JSON -> TOML
        res_toml = data.convert(str(sample_json), "TOML", self.temp_dir)
        self.assertEqual(res_toml.status, "success")
        self.assertTrue(Path(res_toml.output_path).exists())

    def test_documents_txt_to_docx_and_html(self):
        sample_txt = Path(self.temp_dir) / "notes.txt"
        sample_txt.write_text("Hello World!\nThis is a test note.", encoding="utf-8")

        res_docx = documents.convert(str(sample_txt), "DOCX", self.temp_dir)
        self.assertEqual(res_docx.status, "success")
        self.assertTrue(Path(res_docx.output_path).exists())

        res_html = documents.convert(str(sample_txt), "HTML", self.temp_dir)
        self.assertEqual(res_html.status, "success")
        self.assertTrue(Path(res_html.output_path).exists())

if __name__ == "__main__":
    unittest.main()
