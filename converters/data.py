# converters/data.py
import json
import os
from pathlib import Path
from . import ConversionResult

def convert(input_path: str, output_format: str, output_dir: str) -> ConversionResult:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    fmt = output_format.lower().strip().lstrip(".")
    output_path = output_dir / f"{input_path.stem}.{fmt}"
    ext = input_path.suffix.lower()

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 1. Parse input file into Python structure
        data = None
        if ext == '.json':
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif ext in ('.yaml', '.yml'):
            import yaml
            with open(input_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif ext == '.toml':
            try:
                import tomllib
                with open(input_path, 'rb') as f:
                    data = tomllib.load(f)
            except ImportError:
                import toml
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = toml.load(f)
        else:
            return ConversionResult(status='error', error=f"Unsupported structured data input format: {ext}")

        # 2. Serialize to output format
        if fmt == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
        elif fmt in ('yaml', 'yml'):
            import yaml
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False)
        elif fmt == 'toml':
            if not isinstance(data, dict):
                return ConversionResult(status='error', error="TOML output requires root element to be a key-value mapping/table.")
            try:
                import tomli_w
                with open(output_path, 'wb') as f:
                    tomli_w.dump(data, f)
            except ImportError:
                import toml
                with open(output_path, 'w', encoding='utf-8') as f:
                    toml.dump(data, f)
        elif fmt == 'csv':
            import pandas as pd
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False)
            elif isinstance(data, dict):
                df = pd.json_normalize(data)
                df.to_csv(output_path, index=False)
            else:
                return ConversionResult(status='error', error="Data cannot be flattened to tabular CSV.")
        else:
            return ConversionResult(status='error', error=f"Unsupported structured data output format: {fmt}")

        size = output_path.stat().st_size if output_path.exists() else None
        return ConversionResult(status='success', output_path=str(output_path), output_size=size)

    except Exception as e:
        return ConversionResult(status='error', error=str(e))
