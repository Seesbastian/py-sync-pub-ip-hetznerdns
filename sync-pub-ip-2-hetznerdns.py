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
        "Auth-API-Token": api_token  
    }
    data = {
        "value": new_ip,  
        "ttl": 600,       
        "type": "A",      
        "name": sub_domain,
        "zone_id": zone_id 
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
record_id = "<Record-ID>" # string of letters and numbers
api_token = "<Hetzner-API-Token>"  # can be found in your hetzner account
new_ip = get_public_ip()  # Your Public IP
zone_id = "<DNS-Zone>"  # Zone of your domain
sub_domain = "<your-subdomain>"

update_dns_record(record_id, api_token, new_ip, zone_id)
