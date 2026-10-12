# converters/images.py
import os
from pathlib import Path
from PIL import Image
from . import ConversionResult

def convert(input_path: str, output_format: str, output_dir: str) -> ConversionResult:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    fmt = output_format.lower().strip().lstrip(".")
    output_path = output_dir / f"{input_path.stem}.{fmt}"
    
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(input_path) as img:
            # Handle PDF export
            if fmt == 'pdf':
                # Remove alpha channel if present because PDF doesn't support RGBA cleanly
                if img.mode in ("RGBA", "LA", "P"):
                    rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                    alpha = img.split()[-1] if img.mode in ("RGBA", "LA") else None
                    if img.mode == "P":
                        img = img.convert("RGBA")
                        alpha = img.split()[-1]
                    rgb_img.paste(img, mask=alpha)
                    rgb_img.save(output_path, "PDF", resolution=100.0)
                else:
                    img.convert("RGB").save(output_path, "PDF", resolution=100.0)
                
                size = output_path.stat().st_size if output_path.exists() else None
                return ConversionResult(status='success', output_path=str(output_path), output_size=size)

            # Handle ICO export
            if fmt == 'ico':
                icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                # Filter sizes that don't exceed original dimensions
                valid_sizes = [s for s in icon_sizes if s[0] <= max(img.width, 16)] or [(32, 32)]
                img.save(output_path, format='ICO', sizes=valid_sizes)
                size = output_path.stat().st_size if output_path.exists() else None
                return ConversionResult(status='success', output_path=str(output_path), output_size=size)

            # Handle JPG / JPEG / BMP export (require RGB, no alpha)
            if fmt in ("jpg", "jpeg", "bmp"):
                if img.mode in ("RGBA", "LA", "P"):
                    rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                    alpha = img.split()[-1] if img.mode in ("RGBA", "LA") else None
                    if img.mode == "P":
                        img = img.convert("RGBA")
                        alpha = img.split()[-1]
                    rgb_img.paste(img, mask=alpha)
                    save_fmt = 'JPEG' if fmt in ('jpg', 'jpeg') else 'BMP'
                    rgb_img.save(output_path, format=save_fmt, quality=95)
                else:
                    save_fmt = 'JPEG' if fmt in ('jpg', 'jpeg') else 'BMP'
                    img.convert("RGB").save(output_path, format=save_fmt, quality=95)
                
                size = output_path.stat().st_size if output_path.exists() else None
                return ConversionResult(status='success', output_path=str(output_path), output_size=size)

            # Handle PNG / WEBP / TIFF / GIF
            save_format_map = {
                'png': 'PNG',
                'webp': 'WEBP',
                'tiff': 'TIFF',
                'tif': 'TIFF',
                'gif': 'GIF',
            }
            save_format = save_format_map.get(fmt, fmt.upper())
            img.save(output_path, format=save_format)
            
            size = output_path.stat().st_size if output_path.exists() else None
            return ConversionResult(status='success', output_path=str(output_path), output_size=size)

    except Exception as e:
        return ConversionResult(status='error', error=str(e))