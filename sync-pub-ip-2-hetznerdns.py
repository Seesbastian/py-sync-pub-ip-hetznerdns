import requests
import json
from requests import get

def get_public_ip():
    try:
        ip = get('https://api.ipify.org').content.decode('utf8')
        return ip
    except requests.RequestException as e:
        print(f"Error while trying to get public IP: {e}")
        return None

def update_dns_record(record_id, api_token, new_ip, zone_id):
    #Function for updating Record in Hetzner Cloud:
    
    url = f"https://dns.hetzner.com/api/v1/records/{record_id}"
    headers = {
        "Content-Type": "application/json",
        "Auth-API-Token": api_token  # API-Token in den Header aufnehmen
    }
    data = {
        "value": new_ip,  # Die neue IP-Adresse, die gesetzt werden soll
        "ttl": 600,       # Time-to-Live für den DNS-Record
        "type": "A",      # Typ des DNS-Records (A für IPv4)
        "name": "nc",  # Name des DNS-Records (z.B. Subdomain)
        "zone_id": zone_id  # Zone-ID, die die Domain angibt
    }
    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        print(f"Updated DNS-Record successfully")
        print(f"Response HTTP Status Code: {response.status_code}")
        print(f"Response HTTP Response Body: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")

# Example
record_id = "<Record-ID>"  # Hier die tatsächliche Record ID einfügen
api_token = "<Hetzner-API-Token>"  # Dein API-Token
new_ip = get_public_ip()  # Neue IP-Adresse, die du setzen willst
zone_id = "<DNS-Zone>"  # Die Zone ID deiner Domain

update_dns_record(record_id, api_token, new_ip, zone_id)
