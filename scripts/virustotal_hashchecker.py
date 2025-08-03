import requests
import json

# My VirusTotal API key (i will replace the real one when handing in)
API_KEY = "a24bde446d6eb80080b8aefee75bea"

# hardcoded list of hashes to check
hashes = [
	
	"a0aa4a74b70cbca5a03960df1a3dc878",
	"08071481e8f076cf0e68d58e0b3b8362",
	"485887d8cafee405e0a630e76124112f",
	"0e690d5adb6b4046bbbd33840d470fe5",
	"ce9acb4f873e20297df2193f8b507b5f",
	"c7f855f8e2d7a3dda14112bd00b0ceda",
	"7c6fac02352dc182ecc46fb0ae15ae27",
	"782b234d4a9bcafdfc79ac3d6901cfd6",
	"46a89134262813e36d0ed97bf5904201",
	"38ef174fe25e861710d5f68d371f686d",
	"15f2c0638f1deb20c26c2ccbe875c228",
	"e238a28f468ea0d51c33d50a96f46838",
	"02c0a31551cc2aebf747612b8038a080",
	"3376781b3505bbf5b61ac7bd8efdc541"



]

headers = {
    "x-apikey": API_KEY
}

def pretty_print_response(hash_value, response_json):
    #  if the file exists 
    if "data" in response_json:
        attributes = response_json["data"]["attributes"]
        # file name
        file_name = attributes.get("meaningful_name")
        if not file_name:
            names = attributes.get("names", [])
            file_name = names[0] if names else "N/A"
        reputation = attributes.get("reputation", "N/A")
        size = attributes.get("size", "N/A")  # File size in bytes
        stats = attributes.get("last_analysis_stats", {})
        malicious = stats.get("malicious", "N/A")
        suspicious = stats.get("suspicious", "N/A")
        undetected = stats.get("undetected", "N/A")
        harmless = stats.get("harmless", "N/A")
        
        print(f"Hash: {hash_value}")
        print(f"Name: {file_name}")
        print(f"File Size: {size} bytes")
        print(f"Reputation: {reputation}")
        print("Analysis Stats:")
        print(f"  Malicious: {malicious}")
        print(f"  Suspicious: {suspicious}")
        print(f"  Undetected: {undetected}")
        print(f"  Harmless: {harmless}")
    else:
        # if there's an error, print the error message.
        error = response_json.get("error", {})
        message = error.get("message", "Unknown error")
        print(f"Hash: {hash_value}")
        print("Error:", message)

for h in hashes:
    print("=" * 50)
    print(f"Checking hash: {h}")
    url = f"https://www.virustotal.com/api/v3/files/{h}"
    response = requests.get(url, headers=headers)
    if response.ok:
        try:
            response_json = response.json()
            pretty_print_response(h, response_json)
        except Exception as e:
            print(f"Error processing hash {h}: {e}")
    else:
        print(f"Error retrieving data for hash {h}: HTTP {response.status_code}")
    print("\n")
