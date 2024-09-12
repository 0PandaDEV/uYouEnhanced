import json
import requests
import sys


def get_latest_youtube_version():
    url = 'https://itunes.apple.com/search'
    params = {
        'limit': '5',
        'entity': 'software,iPadSoftware',
        'country': 'us',
        'term': 'youtube',
        'callback': 'fetch_with_cb_cb'
    }
    headers = {
        'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
        'Referer': 'https://armconverter.com/',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        # Extract JSON from JSONP response
        json_str = response.text[response.text.index('(') + 1 : response.text.rindex(')')]
        data = json.loads(json_str)
        
        # Find YouTube app in results
        for app in data['results']:
            if app['bundleId'] == 'com.google.ios.youtube':
                return app['version']
        
        print("YouTube app not found in search results")
        return None
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None


def get_decrypted_youtube_url(version):
    base_url = f'https://armconverter.com/decryptedappstore/download/544007664/com.google.ios.youtube/{version}'
    info_url = f'{base_url}/info'
    prepare_url = f'{base_url}/prepare'

    headers = {
        'accept': '*/*',
        'accept-language': 'en,de;q=0.9,de-CH;q=0.8',
        'cookie': 'session=.eJxFkc1qHTEMhd_F60sj2_KP5lVCGSRbboaGzOCZCwkh714loe1CCx0h8Z2jd7eOqeeTW65515tbt-4WB6piVbG3DlCwYBWtjVvjUQOE0esITAx-CDF7LjF6rD30ItJ64DwUetKogyGUGpJkZkUPIpl8rGmQYg9apMUcarStBkXsSAOQ7Azkfur8pvEecq0UTd3289fez3Xn-_W0XvtvfXHLuzMwPc-_vfMJvKYsvTWsMFQbohJqqsNzo7KWiORDkEGYUgFGYqKi6rNmKQxYBKm3TJlM7CGbZSJWzxZDIjESfT02C27lyy2-hBRzSiH8oIrx_3AzmgzGADc39Svof5DmKEBGC28YWJJokJlDrK0SZyQhewEmZeieI6FXc9l6rJFDFenGcLb9ULc8umPuY3tW9_Pmvs6v19vnwIny1Ok-bu5FX6_1Pp9NfOja5ttxaefjOK996oP7-AMU_J0c.Zs3Ckg.uGf_7HZAqZBagipeBQIzbEVwymE',
        'dnt': '1',
        'priority': 'u=1, i',
        'referer': 'https://armconverter.com/decryptedappstore/us/youtube',
        'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    try:
        # First request
        response = requests.get(info_url, headers=headers)
        response.raise_for_status()
        info_data = response.json()

        # Second request
        prepare_headers = headers.copy()
        prepare_headers.update({
            'content-length': '0',
            'origin': 'https://armconverter.com',
        })
        prepare_response = requests.post(prepare_url, headers=prepare_headers)
        prepare_response.raise_for_status()
        prepare_data = prepare_response.json()

        if prepare_data.get('success') and prepare_data.get('token'):
            token = prepare_data['token']
            final_url = f"{base_url}?token={token}"
            return final_url
        else:
            print("Failed to get token from prepare request")
            return None
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None


if __name__ == "__main__":
    latest_version = get_latest_youtube_version()
    if latest_version:
        decrypted_url = get_decrypted_youtube_url(latest_version)
        if decrypted_url:
            print(decrypted_url)
            sys.exit(0)
    sys.exit(1)
