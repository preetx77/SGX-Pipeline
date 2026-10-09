"""
Isolated diagnostic test for SGXClient.get_company_list()
No system modifications, no database changes, no watchlist updates.
Single request with comprehensive error handling.
"""

import sys
import logging
import json
from datetime import datetime
from pathlib import Path

# Configure logging to console only (diagnostic mode)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Import dependencies
try:
    from scraper.client import SGXClient
    from config.settings import ANNOUNCEMENT_API
except ImportError as e:
    logger.error(f"Import failed: {e}")
    sys.exit(1)

def sanitize_response(obj, max_depth=2, current_depth=0):
    """Recursively sanitize response to avoid exposing secrets"""
    if current_depth > max_depth:
        return "..."
    
    sensitive_keys = ['token', 'key', 'secret', 'auth', 'password', 'cookie', 'session']
    
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if any(s in k.lower() for s in sensitive_keys):
                result[k] = "[REDACTED]"
            else:
                result[k] = sanitize_response(v, max_depth, current_depth + 1)
        return result
    elif isinstance(obj, list):
        if len(obj) > 10:
            return f"[list with {len(obj)} items]"
        return [sanitize_response(item, max_depth, current_depth + 1) for item in obj]
    elif isinstance(obj, str) and len(obj) > 500:
        return f"{obj[:100]}...[truncated, {len(obj)} chars total]"
    else:
        return obj

def test_get_company_list():
    """Test SGXClient.get_company_list() in isolation"""
    
    logger.info("=" * 80)
    logger.info("SGXClient.get_company_list() Diagnostic Test")
    logger.info("=" * 80)
    
    # Configuration
    ENDPOINT = ANNOUNCEMENT_API
    endpoint_called = f"{ENDPOINT}/companylist"
    original_codes = ["HQU", "1J5", "L19", "5FO", "5TP", "G50", "42C", "1V3", "1LO", "VC2", "5AB", "41A"]
    test_timestamp = datetime.utcnow().isoformat()
    
    logger.info(f"\nConfiguration:")
    logger.info(f"  Base URL: {ENDPOINT}")
    logger.info(f"  Endpoint called: {endpoint_called}")
    logger.info(f"  Test timestamp: {test_timestamp}")
    logger.info(f"  Original 12 codes: {', '.join(original_codes)}")
    logger.info(f"  Timeout: 30 seconds")
    
    # Step 1: Instantiate client
    logger.info(f"\nStep 1: Instantiating SGXClient...")
    try:
        client = SGXClient(throttle_delay=0.5)  # Reduced throttle for test
        logger.info(f"  ✓ Client instantiated")
        logger.info(f"  ✓ Authentication initialized")
    except Exception as e:
        logger.error(f"  ✗ Failed to instantiate client: {e}")
        return None
    
    # Step 2: Call get_company_list()
    logger.info(f"\nStep 2: Calling get_company_list()...")
    response_data = None
    http_status = None
    error_type = None
    error_msg = None
    
    try:
        response_data = client.get_company_list()
        http_status = 200
        logger.info(f"  ✓ Request succeeded (HTTP 200)")
    except requests.exceptions.Timeout as e:
        error_type = "TIMEOUT"
        error_msg = str(e)
        logger.error(f"  ✗ Request timed out (>30s): {error_msg}")
    except requests.exceptions.ConnectionError as e:
        error_type = "CONNECTION_ERROR"
        error_msg = str(e)
        logger.error(f"  ✗ Connection error (DNS/network): {error_msg}")
    except requests.exceptions.HTTPError as e:
        error_type = "HTTP_ERROR"
        error_msg = str(e)
        try:
            http_status = e.response.status_code
        except:
            pass
        logger.error(f"  ✗ HTTP error: {error_msg}")
        if http_status:
            logger.error(f"      Status code: {http_status}")
    except ValueError as e:
        error_type = "PARSE_ERROR"
        error_msg = str(e)
        logger.error(f"  ✗ JSON parse error: {error_msg}")
    except Exception as e:
        error_type = "UNKNOWN_ERROR"
        error_msg = str(e)
        logger.error(f"  ✗ Unexpected error: {type(e).__name__}: {error_msg}")
    
    # Step 3: Analyze response if successful
    if response_data is not None:
        logger.info(f"\nStep 3: Analyzing response schema...")
        
        # Type check
        response_type = type(response_data).__name__
        logger.info(f"  Response type: {response_type}")
        
        # Top-level keys
        if isinstance(response_data, dict):
            top_keys = list(response_data.keys())
            logger.info(f"  Top-level keys: {top_keys}")
        
        # Record count
        record_count = 0
        if isinstance(response_data, dict):
            # Try common data container names
            for key in ['data', 'records', 'companies', 'results', 'items']:
                if key in response_data:
                    container = response_data[key]
                    if isinstance(container, list):
                        record_count = len(container)
                        logger.info(f"  Data container: '{key}'")
                        logger.info(f"  Record count: {record_count}")
                        break
        elif isinstance(response_data, list):
            record_count = len(response_data)
            logger.info(f"  Record count: {record_count} (top-level array)")
        
        # Sample records
        logger.info(f"\nStep 4: Sample records (max 5)...")
        sample_records = []
        
        if isinstance(response_data, dict):
            for key in ['data', 'records', 'companies', 'results', 'items']:
                if key in response_data and isinstance(response_data[key], list):
                    sample_records = response_data[key][:5]
                    break
        elif isinstance(response_data, list):
            sample_records = response_data[:5]
        
        for i, record in enumerate(sample_records, 1):
            sanitized = sanitize_response(record, max_depth=1)
            logger.info(f"  Record {i}: {json.dumps(sanitized, indent=2)}")
        
        # Step 5: Validate against original codes
        logger.info(f"\nStep 5: Validating against original 12 codes...")
        
        # Extract all codes from response
        returned_codes = set()
        
        def extract_codes(obj, codes_set):
            """Recursively extract potential stock codes from response"""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if any(code_key in k.lower() for code_key in ['code', 'stock', 'ticker']):
                        if isinstance(v, str) and v.strip():
                            codes_set.add(v.strip().upper())
                    extract_codes(v, codes_set)
            elif isinstance(obj, list):
                for item in obj:
                    extract_codes(item, codes_set)
        
        extract_codes(response_data, returned_codes)
        
        logger.info(f"  Codes found in response: {len(returned_codes)}")
        
        matched_codes = []
        missing_codes = []
        
        for code in original_codes:
            if code in returned_codes:
                matched_codes.append(code)
            else:
                missing_codes.append(code)
        
        logger.info(f"  ✓ Matched: {len(matched_codes)} - {', '.join(matched_codes)}")
        logger.info(f"  ✗ Missing: {len(missing_codes)} - {', '.join(missing_codes)}")
        
        if len(matched_codes) == 12:
            logger.info(f"  ✓ All original 12 codes found!")
        elif len(matched_codes) > 0:
            logger.info(f"  ⚠ Partial match: {len(matched_codes)}/12 codes found")
        else:
            logger.warning(f"  ⚠ No original codes found (response may use different structure)")
        
        # Step 6: Generate reference file if data looks valid
        logger.info(f"\nStep 6: Generating reference CSV...")
        
        if record_count > 0 and (len(matched_codes) > 0 or record_count > 50):
            # Create data/reference directory
            ref_dir = Path("data/reference")
            ref_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract companies from response
            companies = []
            
            if isinstance(response_data, dict):
                for key in ['data', 'records', 'companies', 'results', 'items']:
                    if key in response_data and isinstance(response_data[key], list):
                        companies = response_data[key]
                        break
            elif isinstance(response_data, list):
                companies = response_data
            
            # Build CSV
            csv_file = ref_dir / "sgx_company_universe.csv"
            
            with open(csv_file, 'w', encoding='utf-8') as f:
                # Header
                f.write("stock_code,company_name,instrument_type,source,verified_at,validation_status\n")
                
                # Rows
                written = 0
                for company in companies[:100]:  # First 100 for now
                    if isinstance(company, dict):
                        # Extract fields (adapt keys based on actual response)
                        code = company.get('stock_code') or company.get('code') or company.get('ticker') or ''
                        name = company.get('company_name') or company.get('name') or company.get('issuer_name') or ''
                        instrument = company.get('instrument_type') or company.get('type') or ''
                        
                        if code and name:
                            status = "matched" if code.upper() in matched_codes else "retrieved"
                            f.write(f'"{code}","{name}","{instrument}","sgx_api_companylist","{test_timestamp}","{status}"\n')
                            written += 1
                
                f.write(f"# Total records in response: {record_count}\n")
                f.write(f"# Records written to CSV: {written}\n")
                f.write(f"# Original codes matched: {len(matched_codes)}/12\n")
            
            logger.info(f"  ✓ CSV written to: {csv_file}")
            logger.info(f"    Records written: {written}")
        else:
            logger.info(f"  ⚠ Insufficient data for reference CSV (records: {record_count}, matches: {len(matched_codes)})")
    
    # Final Report
    logger.info(f"\n" + "=" * 80)
    logger.info("DIAGNOSTIC TEST COMPLETE")
    logger.info("=" * 80)
    
    logger.info(f"\nFinal Report:")
    logger.info(f"  Endpoint: {endpoint_called}")
    logger.info(f"  Status: {'SUCCESS' if response_data is not None else 'FAILED'}")
    
    if response_data is not None:
        logger.info(f"  Records returned: {record_count}")
        logger.info(f"  Original codes matched: {len(matched_codes)}/12")
        logger.info(f"  Reference CSV: {'Created' if record_count > 0 else 'Not created'}")
        logger.info(f"\nNext action: Review sgx_company_universe.csv and validate instrument types")
    else:
        logger.info(f"  Error type: {error_type}")
        logger.info(f"  Error: {error_msg}")
        logger.info(f"  HTTP status: {http_status if http_status else 'N/A'}")
        logger.info(f"\nNext action: Check endpoint configuration or authentication")
    
    logger.info(f"\n" + "=" * 80)
    
    return response_data

# Import requests here after logging setup to catch errors
try:
    import requests
except ImportError:
    logger.error("requests library not installed")
    sys.exit(1)

if __name__ == "__main__":
    try:
        test_get_company_list()
    except KeyboardInterrupt:
        logger.info("\nTest interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
