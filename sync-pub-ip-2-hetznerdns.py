import requests
import json
from requests import get
import os

# --- Konfiguration ---
HETZNER_DNS_API_TOKEN = "x"
DOMAIN_NAME = "x"

if not HETZNER_DNS_API_TOKEN:
    print("Fehler: HETZNER_DNS_API_TOKEN Umgebungsvariable ist nicht gesetzt.")
    print("Bitte setze sie z.B. mit: export HETZNER_DNS_API_TOKEN='DEIN_TOKEN'")
    exit(1)

# Liste der zu aktualisierenden DNS-Records
# Hinweis: Du benötigst hier nur noch den Namen und die Zone ID.
# Die Record-ID wird jetzt dynamisch ermittelt.
DNS_RECORDS_TO_UPDATE = [
    {
        "name": "bla",
        "zone_id": "x"
    },
    {
        "name": "bla2",
        "zone_id": "x"
    },
    {
        "name": "bla3",
        "zone_id": "x"
    },
    {
        "name": "bla4",
        "zone_id": "x"
    },
    {
        "name": "bla5",
        "zone_id": "x"
    },
    {
        "name": "bla6",
        "zone_id": "x"
    },
    {
        "name": "bla7",
        "zone_id": "x"
    },
    {
        "name": "bla8",
        "zone_id": "x"
    },
]

# --- Funktionen ---

def get_public_ip():
    """Ruft die aktuelle öffentliche IPv4-Adresse ab."""
    try:
        ip = get('https://api.ipify.org').content.decode('utf8')
        return ip
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der öffentlichen IP-Adresse: {e}")
        return None

def get_dns_record_details(record_data, api_token):
    """
    Ruft die Details (inkl. Record-ID und Wert) eines DNS-Records von Hetzner ab.
    Gibt ein Dictionary mit 'id' und 'value' zurück.
    """
    zone_id = record_data["zone_id"]
    record_name = record_data["name"]

    url = f"https://dns.hetzner.com/api/v1/records?zone_id={zone_id}"
    headers = {
        "Auth-API-Token": api_token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        records = response.json()["records"]

        for record in records:
            if record["name"] == record_name and record["type"] == "A":
                return {"id": record["id"], "value": record["value"]}

        return None # Record wurde nicht gefunden

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen des Records für '{record_name}.{DOMAIN_NAME}': {e}")
        return None

def update_dns_record(record_id, record_name, zone_id, api_token, new_ip):
    """Aktualisiert einen DNS-Record in Hetzner DNS."""
    url = f"https://dns.hetzner.com/api/v1/records/{record_id}"
    headers = {
        "Content-Type": "application/json",
        "Auth-API-Token": api_token
    }
    data = {
        "value": new_ip,
        "ttl": 600,
        "type": "A",
        "name": record_name,
        "zone_id": zone_id
    }
    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        print(f"DNS-Record für '{record_name}.{DOMAIN_NAME}' erfolgreich aktualisiert!")
        print(f"  Response HTTP Status Code: {response.status_code}")
        print(f"  Response HTTP Response Body: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim HTTP Request für '{record_name}.{DOMAIN_NAME}': {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Fehlerdetails: {e.response.text}")

# --- Hauptlogik ---
if __name__ == "__main__":
    current_public_ip = get_public_ip()

    if not current_public_ip:
        print("Konnte die öffentliche IP-Adresse nicht ermitteln. DNS-Updates werden übersprungen.")
        exit(1)

    print(f"Aktuelle öffentliche IP-Adresse: {current_public_ip}")

    for record_info in DNS_RECORDS_TO_UPDATE:
        record_name = record_info['name']
        zone_id = record_info['zone_id']

        print(f"\nÜberprüfe Record für '{record_name}.{DOMAIN_NAME}'...")

        # 1. Aktuellen DNS-Eintrag abrufen
        dns_record_details = get_dns_record_details(record_info, HETZNER_DNS_API_TOKEN)

        if not dns_record_details:
            print(f"  [WARNUNG] Record '{record_name}.{DOMAIN_NAME}' wurde nicht in Hetzner DNS gefunden. Überspringe.")
            continue

        current_dns_ip = dns_record_details['value']
        record_id = dns_record_details['id']

        print(f"  Aktueller DNS-Eintrag: {current_dns_ip}")

        # 2. IP-Adressen vergleichen
        if current_dns_ip == current_public_ip:
            print("  DNS-Record ist bereits aktuell. Keine Änderung erforderlich.")
        else:
            # 3. Aktualisierung bei Abweichung
            print(f"  IP-Adressen stimmen nicht überein! Aktualisiere von {current_dns_ip} auf {current_public_ip}...")
            update_dns_record(record_id, record_name, zone_id, HETZNER_DNS_API_TOKEN, current_public_ip)
