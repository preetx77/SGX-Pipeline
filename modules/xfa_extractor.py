#!/usr/bin/env python3
"""
XFA Form Extractor Module
Extracts director transaction data from Adobe-wrapped XFA Form 1/3 PDFs.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from typing import Dict, List, Optional

class XFAExtractor:
    """Extract structured data from XFA PDF forms"""
    
    @staticmethod
    def extract_from_pdf(pdf_path: str) -> Optional[Dict]:
        """Extract XFA datasets from a PDF file"""
        try:
            reader = PdfReader(pdf_path)
            
            if not (reader.xfa and 'datasets' in reader.xfa):
                return None
            
            datasets_bytes = reader.xfa['datasets']
            if isinstance(datasets_bytes, bytes):
                datasets_str = datasets_bytes.decode('utf-8', errors='ignore')
            else:
                datasets_str = str(datasets_bytes)
            
            root = ET.fromstring(datasets_str)
            
            result = {
                'filename': os.path.basename(pdf_path),
                'filepath': pdf_path,
                'has_xfa': True,
            }
            
            # Extract fields
            for elem in root.iter():
                tag = elem.tag.split('}')[-1]
                text = (elem.text or '').strip()
                
                if tag == 'name' and 'limited' in text.lower() and len(text) > 5 and 'company_name' not in result:
                    result['company_name'] = text
                
                if tag in ['nameDirector', 'nameShareholder'] and len(text) > 2 and 'director_name' not in result:
                    result['director_name'] = text
                    result['is_shareholder'] = (tag == 'nameShareholder')
                
                if tag in ['dateNotification', 'dateTransaction'] and len(text) == 10 and 'date' not in result:
                    result['date'] = text
            
            form_type = 'Form 3' if result.get('is_shareholder') else 'Form 1'
            result['form_type'] = form_type
            
            return result
            
        except Exception as e:
            return None
    
    @staticmethod
    def extract_batch(directory: str, pattern: str = '*Form*.pdf') -> List[Dict]:
        """Extract XFA data from all matching PDFs"""
        results = []
        pdf_files = list(Path(directory).rglob(pattern))
        
        print(f"[*] Extracting XFA from {len(pdf_files)} files")
        
        for i, pdf_file in enumerate(pdf_files, 1):
            result = XFAExtractor.extract_from_pdf(str(pdf_file))
            if result:
                results.append(result)
                if i % 10 == 0:
                    print(f"  Processed {i} files, extracted {len(results)} records")
        
        return results

