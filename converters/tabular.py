# converters/tabular.py
import os
import pandas as pd
from pathlib import Path
from . import ConversionResult

def convert(input_path: str, output_format: str, output_dir: str) -> ConversionResult:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    fmt = output_format.lower().strip().lstrip(".")
    output_path = output_dir / f"{input_path.stem}.{fmt}"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 1. Read the input into DataFrame
        ext = input_path.suffix.lower()
        if ext == '.csv':
            df = pd.read_csv(input_path)
        elif ext == '.tsv':
            df = pd.read_csv(input_path, sep='\t')
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(input_path)
        elif ext == '.json':
            try:
                df = pd.read_json(input_path)
            except ValueError:
                # Handle line-delimited or record json
                df = pd.read_json(input_path, lines=True)
        elif ext == '.parquet':
            df = pd.read_parquet(input_path)
        else:
            return ConversionResult(status='error', error=f"Unsupported tabular input format: {ext}")

        # 2. Export to requested format
        if fmt == 'csv':
            df.to_csv(output_path, index=False)
        elif fmt == 'tsv':
            df.to_csv(output_path, sep='\t', index=False)
        elif fmt == 'xlsx':
            df.to_excel(output_path, index=False)
        elif fmt == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif fmt == 'parquet':
            df.to_parquet(output_path, index=False)
        elif fmt == 'html':
            df.to_html(output_path, index=False)
        else:
            return ConversionResult(status='error', error=f"Unsupported tabular output format: {fmt}")

        size = output_path.stat().st_size if output_path.exists() else None
        return ConversionResult(status='success', output_path=str(output_path), output_size=size)

    except Exception as e:
        return ConversionResult(status='error', error=str(e))