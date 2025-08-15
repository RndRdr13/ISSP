
import requests
import re

def analyze_website(url):
    result = {
        'URL': url,
        'CMS / Platform': 'Unknown',
        'Snap Plugin Detected': 'No',
        'Payment Gateways': [],
        'Third-Party Integrations': [],
        'Detected Plugins / Apps': [],
        'Tech Stack': [],
        'Programming Language': 'Unknown',
        'Snap Compatibility Score (%)': 0,
        'Snap Plugin Compatibility': 'Unlikely Compatible',
        'Detected HTML': ''
    }

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        result['Detected HTML'] = html

        # CMS detection (simplified)
        if "shopify" in html.lower():
            result["CMS / Platform"] = "Shopify"
            result["Programming Language"] = "Liquid"
        elif "woocommerce" in html.lower() or "wp-content" in html.lower():
            result["CMS / Platform"] = "WooCommerce"
            result["Programming Language"] = "PHP"
        elif "magento" in html.lower():
            result["CMS / Platform"] = "Magento"
            result["Programming Language"] = "PHP"
        elif "bigcommerce" in html.lower():
            result["CMS / Platform"] = "BigCommerce"
            result["Programming Language"] = "JavaScript"

        # Snap plugin detection (keywords)
        snap_keywords = ['snap finance', 'snap checking', 'as low as']
        if any(kw in html.lower() for kw in snap_keywords):
            result['Snap Plugin Detected'] = 'Yes'

        # Payment gateway detection
        if "stripe" in html.lower(): result['Payment Gateways'].append("Stripe")
        if "paypal" in html.lower(): result['Payment Gateways'].append("PayPal")
        if "afterpay" in html.lower(): result['Payment Gateways'].append("Afterpay")
        if "klarna" in html.lower(): result['Payment Gateways'].append("Klarna")
        if "affirm" in html.lower(): result['Payment Gateways'].append("Affirm")
        if "authorizenet" in html.lower() or "authorize.net" in html.lower():
            result['Payment Gateways'].append("Authorize.Net")

        # Plugins / Apps detection
        if "klaviyo" in html.lower(): result["Detected Plugins / Apps"].append("Klaviyo")
        if "yotpo" in html.lower(): result["Detected Plugins / Apps"].append("Yotpo")
        if "gorgias" in html.lower(): result["Detected Plugins / Apps"].append("Gorgias")

    except Exception as e:
        result['error'] = f"Error fetching URL: {str(e)}"
        return result

    calculate_snap_score(result)

    # Normalize array fields
    for key in [
        "Payment Gateways",
        "Third-Party Integrations",
        "Detected Plugins / Apps",
        "Tech Stack"
    ]:
        if not isinstance(result.get(key), list):
            result[key] = []

    return result

def calculate_snap_score(result):
    score = 0

    # Regla 1: CMS compatible → 80%
    if result['CMS / Platform'] in ['Shopify', 'WooCommerce', 'Magento', 'BigCommerce', 'WordPress']:
        score = 80

    # Regla 4: Si no es CMS compatible pero el lenguaje lo es → 80%
    elif result['Programming Language'] in ['PHP', 'JavaScript', 'Java', 'Liquid']:
        score = 80

    # Clasificación
    if score >= 80:
        label = "Likely Compatible"
    elif score >= 50:
        label = "Possibly Compatible"
    else:
        label = "Unlikely Compatible"

    result['Snap Compatibility Score (%)'] = score
    result['Snap Plugin Compatibility'] = label

    if result['CMS / Platform'] in ['Shopify', 'WooCommerce', 'Magento', 'BigCommerce', 'WordPress']:
        score += 40

    if result['Snap Plugin Detected'] == 'Yes':
        score += 30

    if any(keyword in result.get('Detected HTML', '').lower() for keyword in ['snap finance', 'snap', 'as low as', 'snap marketing', 'snap checking']):
        score += 10

    if result['Programming Language'] in ['PHP', 'JavaScript', 'Java', 'Liquid']:
        score += 10

    if any(g in ['Stripe', 'Authorize.Net', 'PayPal'] for g in result.get('Payment Gateways', [])):
        score += 10

    final_score = min(score, 100)

    if final_score >= 80:
        label = "Likely Compatible"
    elif final_score >= 50:
        label = "Possibly Compatible"
    else:
        label = "Unlikely Compatible"

    result['Snap Compatibility Score (%)'] = final_score
    result['Snap Plugin Compatibility'] = label
