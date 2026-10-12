# converters/__init__.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ConversionResult:
    status: str  # 'success' or 'error'
    output_path: Optional[str] = None
    error: Optional[str] = None
    output_size: Optional[int] = None
    message: Optional[str] = None