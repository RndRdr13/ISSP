
import re

def calculate_snap_score(result):
    score = 0

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
    result['Snap Plugin Compatibility'] = labelquests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import re

def calculate_snap_score(result):
    score = 0

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

# --- Core Analyzer Function ---
def analyze_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        result = {
            'URL': url,
            'CMS / Platform': 'Unknown',
            'E-commerce System': 'Unknown',
            'Snap Plugin Detected': 'No',
            'Payment Gateways': [],
            'Third-Party Integrations': [],
            'Detected Plugins / Apps': [],
        'Platform Version': 'Unknown',
        'Theme': 'Unknown',
        'Programming Language': 'Unknown',
        'PHP Version': 'Unknown',
        'Competitors': []
        }

        html = response.text.lower()

        # CMS Detection
        if 'shopify' in html or 'Shopify' in html:
            result['CMS / Platform'] = 'Shopify'
        elif 'prestashop' in html:
            result['CMS / Platform'] = 'PrestaShop'
        elif any(term in html for term in ['magento', 'mage-', 'Magento_Catalog', 'skin/frontend/', 'mage-data', 'mage/cookies']):
            result['CMS / Platform'] = 'Magento'
        elif 'bigcommerce' in html:
            result['CMS / Platform'] = 'BigCommerce'
        elif 'wix.com' in html or 'wixsite' in html:
            result['CMS / Platform'] = 'Wix'
        elif 'squarespace' in html:
            result['CMS / Platform'] = 'Squarespace'

        # E-commerce System
        if result['CMS / Platform'] == 'WordPress' and 'woocommerce' in html:
            result['E-commerce System'] = 'WooCommerce'
        elif result['CMS / Platform'] == 'Shopify' and 'shopify-buy' in html:
            result['E-commerce System'] = 'Shopify Cart'
        elif result['CMS / Platform'] == 'PrestaShop' and 'prestashop' in html:
            result['E-commerce System'] = 'PrestaShop'
        elif result['CMS / Platform'] == 'BigCommerce' and 'bigcommerce' in html:
            result['E-commerce System'] = 'BigCommerce'
        elif result['CMS / Platform'] == 'Magento' and 'magento' in html:
            result['E-commerce System'] = 'Magento'

        # Snap Finance Detection
        if 'cdn.snapfinance.com' in html or 'data-snapfinance-apply' in html:
            result['Snap Plugin Detected'] = 'Yes'

        # Payment Gateways
        if 'paypal' in html:
            result['Payment Gateways'].append('PayPal')
        if 'stripe' in html:
            result['Payment Gateways'].append('Stripe')
        if 'klarna' in html:
            result['Payment Gateways'].append('Klarna')
        if 'affirm' in html:
            result['Payment Gateways'].append('Affirm')
        if 'afterpay' in html:
            result['Payment Gateways'].append('Afterpay')
        if 'sezzle' in html:
            result['Payment Gateways'].append('Sezzle')
        if 'bread' in html:
            result['Payment Gateways'].append('Bread Finance')
        if 'zipmoney' in html or 'zip-pay' in html:
            result['Payment Gateways'].append('Zip Pay')
        if 'authorize.net' in html:
            result['Payment Gateways'].append('Authorize.Net')
        if 'squareup.com' in html:
            result['Payment Gateways'].append('Square')
        if any(term in html for term in ['snap finance', 'pay with snap', 'snap checkout', 'snap marketing']):
            result['Payment Gateways'].append('Snap Finance')

        # Third-Party Integrations
        if 'google-analytics' in html:
            result['Third-Party Integrations'].append('Google Analytics')
        if 'klaviyo' in html:
            result['Third-Party Integrations'].append('Klaviyo')
        if 'aftership' in html:
            result['Third-Party Integrations'].append('Aftership')

        # Extended Snap-Related Payment Detection
        if any(term in html for term in ['snap finance', 'pay with snap', 'snap checkout', 'snap marketing']):
            result['Payment Gateways'].append('Snap Finance')

        snap_terms = [
            'shopify checkout application',
            'shopify snap finance payment gateway',
            'woocommerce snap finance checkout plugin',
            'magento snap finance checkout plugin',
            'bigcommerce ecommerce platform',
            'snap marketing for woocommerce',
            'snap marketing for magento',
            'snap marketing for bigcommerce',
            'snap marketing for shopify'
        ]
        for term in snap_terms:
            if term in html:
                result['Payment Gateways'].append(term.title())

        # Plugin / App Detection
        plugin_keywords = ['shopify', 'woocommerce', 'wordpress']
        for plugin in plugin_keywords:
            if plugin in html:
                result['Detected Plugins / Apps'].append(plugin.title())

        if 'tidiochat' in html or 'code.tidio.co' in html:
            result['Detected Plugins / Apps'].append('Tidio Chatbot')
        if 'drift' in html or 'js.driftt.com' in html:
            result['Detected Plugins / Apps'].append('Drift Chat')
        if 'hotjar' in html:
            result['Detected Plugins / Apps'].append('Hotjar')
        if 'segment.com' in html:
            result['Detected Plugins / Apps'].append('Segment')
        if 'sezzle.js' in html:
            result['Detected Plugins / Apps'].append('Sezzle')
        if 'bread.js' in html:
            result['Detected Plugins / Apps'].append('Bread Finance')
        if 'zipmoney' in html or 'zip.js' in html:
            result['Detected Plugins / Apps'].append('Zip Pay')

        
        # Additional Metadata Extraction
        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        if meta_generator and meta_generator.get('content'):
            result['Platform Version'] = meta_generator['content']

        # Shopify theme detection (basic example)
        theme_match = re.search(r'theme_name\s*:\s*"([^"]+)"', html)
        if theme_match:
            result['Theme'] = theme_match.group(1)

        # Server headers: PHP Version
        x_powered = response.headers.get('X-Powered-By', '')
        if 'php' in x_powered.lower():
            result['PHP Version'] = x_powered

        # Programming Language
        if 'wp-content' in html:
            result['Programming Language'] = 'PHP'
        elif 'shopify' in html:
            result['Programming Language'] = 'Liquid'
        elif 'react' in html:
            result['Programming Language'] = 'JavaScript (React)'
        elif 'vue' in html:
            result['Programming Language'] = 'JavaScript (Vue)'

        # Competitor Detection
        competitors = []
        for comp in ['affirm', 'afterpay', 'sezzle', 'klarna']:
            if comp in html:
                competitors.append(comp.title())
        result['Competitors'] = competitors

        # Snap Compatibility Detection Logic
        snap_compatibility = []
        if 'shopify' in html and 'snap finance' in html:
            snap_compatibility.append('Shopify-Snap Compatible')
        if 'woocommerce' in html and 'snap finance' in html:
            snap_compatibility.append('WooCommerce-Snap Compatible')
        if 'magento' in html and 'snap finance' in html:
            snap_compatibility.append('Magento-Snap Compatible')
        if 'bigcommerce' in html and 'snap finance' in html:
            snap_compatibility.append('BigCommerce-Snap Compatible')
        if snap_compatibility:
            result['Detected Plugins / Apps'].extend(snap_compatibility)

        calculate_snap_score(result)

        
        if 'Tech Stack' not in result:
            result['Tech Stack'] = []

        
        # Ensure all joinable fields are safe lists
        for key in ["Payment Gateways", "Third-Party Integrations", "Detected Plugins / Apps", "Tech Stack"]:
            if not isinstance(result.get(key), list):
                result[key] = []

        
    # Normalizar campos tipo lista
    for key in ["Payment Gateways", "Third-Party Integrations", "Detected Plugins / Apps", "Tech Stack"]:
        if not isinstance(result.get(key), list):
            result[key] = []

    return result

    except Exception as e:
        return {'URL': url, 'Error': str(e)}

# --- Command-Line Interface ---
def main():
    if len(sys.argv) < 2:
        print("Usage: python snap_analyzer.py <url1,url2,...>")
        return

    urls = sys.argv[1].split(',')
    all_results = []

    for url in urls:
        url = url.strip()
        if not url.startswith("http"):
            url = "https://" + url

        result = analyze_website(url)
        all_results.append(result)

        print("\n--- Analysis Result ---")
        if 'Error' in result:
            print(f"Error analyzing {url}: {result['Error']}")
        else:
            for key, value in result.items():
                if isinstance(value, list):
                    print(f"{key}: {', '.join(value)}")
                else:
                    print(f"{key}: {value}")

    # Export to Excel
    df = pd.DataFrame(all_results)
    filepath = os.path.join(os.getcwd(), "snap_site_analysis.xlsx")
    df.to_excel(filepath, index=False)
    print(f"\nAnalysis complete. Results saved to: {filepath}")

if __name__ == '__main__':
    main()
