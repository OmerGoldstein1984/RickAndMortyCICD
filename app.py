import requests
import csv
import os

# Configuration from Environment Variables
STATUS = os.getenv("TARGET_STATUS", "alive")
ORIGIN = os.getenv("TARGET_ORIGIN", "Earth")
# This path matches the VolumeMount in Kubernetes
OUTPUT_DIR = "/app/data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.csv")

def main():
    # Ensure the directory exists within the volume
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Fetching {STATUS} humans from {ORIGIN}...")
    url = f"https://rickandmortyapi.com/api/character/?status={STATUS}&species=human"
    results = []

    try:
        while url:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            for char in data.get("results", []):
                # Filter by Origin
                if ORIGIN.lower() in char["origin"]["name"].lower():
                    results.append({
                        "Name": char["name"],
                        "Location": char["location"]["name"],
                        "Image": char["image"]
                    })
            url = data.get("info", {}).get("next")

        # Write to the Volume path
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Name", "Location", "Image"])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"SUCCESS: Saved {len(results)} rows to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()