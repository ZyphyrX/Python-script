# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KI9g-VYeo1cyuX8Y30lkCPrT2oCOKVA9
"""

import requests
import pandas as pd
from google.colab import files  # Import the files module

def get_abuseipdb_info(api_key, ip_addresses):
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {
        'Key': api_key,
        'Accept': 'application/json'
    }

    results = []

    for ip_address in ip_addresses:
        params = {'ipAddress': ip_address.strip()}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            result = response.json()
            results.append(result)
        except requests.exceptions.RequestException as e:
            print(f"Error for IP {ip_address}: {e}")

    return results

def main():
    # Replace 'YOUR_API_KEY' with your actual AbuseIPDB API key
    api_key = '05f86961fa9e1a056f5d07adbfad5521d5ad4b552cd7ecfc9ea81f0149ac3f20154b196556949f77'

    # Prompt user to upload a CSV file
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]

    # Load IP addresses and domains from the uploaded CSV file
    df = pd.read_csv(file_name)
    target_ips = df['Source IP'].astype(str).tolist()

    # Get AbuseIPDB results
    results = get_abuseipdb_info(api_key, target_ips)

    # Create a list to store structured data
    structured_data = []

    for result in results:
        ip_address = result['data']['ipAddress']
        abuse_confidence_score = result['data']['abuseConfidenceScore']
        country_code = result['data']['countryCode']
        usage_type = result['data']['usageType']
        isp = result['data']['isp']

        # Check if 'domain' key is present in the result
        if 'domain' in result['data']:
            domain = result['data']['domain']
        else:
            domain = None

        # Append data to the list
        structured_data.append([ip_address, abuse_confidence_score, country_code, usage_type, isp, domain])

    # Create a DataFrame with proper columns
    columns = ['IP Address', 'Abuse Confidence Score', 'Country Code', 'Usage Type', 'ISP', 'Domain']
    result_df = pd.DataFrame(structured_data, columns=columns)

    # Save the DataFrame to an Excel file
    result_df.to_excel("abuseipdb_results.xlsx", index=False)

    # Download the Excel file using the files module
    files.download("abuseipdb_results.xlsx")

if __name__ == "__main__":
    main()

import requests
import pandas as pd
from google.colab import files  # Import the files module

def get_abuseipdb_info(api_key, ip_addresses):
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {
        'Key': api_key,
        'Accept': 'application/json'
    }

    results = []

    for ip_address in ip_addresses:
        params = {'ipAddress': ip_address.strip()}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            result = response.json()
            results.append(result)
        except requests.exceptions.RequestException as e:
            print(f"Error for IP {ip_address}: {e}")

    return results

def main():
    # Replace 'YOUR_API_KEY' with your actual AbuseIPDB API key
    api_key = '05f86961fa9e1a056f5d07adbfad5521d5ad4b552cd7ecfc9ea81f0149ac3f20154b196556949f77'

    # Prompt user to upload a CSV file
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]

    # Load IP addresses and domains from the uploaded CSV file
    df = pd.read_csv(file_name)
    target_ips = df['Source IP'].astype(str).tolist()

    # Get AbuseIPDB results
    results = get_abuseipdb_info(api_key, target_ips)

    # Create lists to store additional data
    domains = []
    country_codes = []
    abuse_confidence_scores = []

    for result in results:
        # Check if 'domain' key is present in the result
        if 'domain' in result['data']:
            domain = result['data']['domain']
        else:
            domain = None

        country_code = result['data']['countryCode']
        abuse_confidence_score = result['data']['abuseConfidenceScore']

        # Append data to the lists
        domains.append(domain)
        country_codes.append(country_code)
        abuse_confidence_scores.append(abuse_confidence_score)

    # Add new columns to the original DataFrame
    df['Domain'] = domains
    df['Country Code'] = country_codes
    df['Abuse Confidence Score'] = abuse_confidence_scores

    # Save the updated DataFrame to the original CSV file
    df.to_csv(file_name, index=False)

    # Download the modified CSV file using the files module
    files.download(file_name)

if __name__ == "__main__":
    main()