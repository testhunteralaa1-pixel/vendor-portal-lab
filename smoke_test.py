import json
import urllib.request
import urllib.error

def run_smoke_test():
    with open('config/renewal.json', 'r') as f:
        config = json.load(f)

    marker = config.get('renewal_marker', '')
    badge_url = f"https://cdn.rtecra.com/portal/badge.svg?ref={marker}"
    theme_url = "https://cdn.rtecra.com/portal/theme.css"

    urls = [("Badge URL", badge_url), ("Theme CSS URL", theme_url)]

    class NoRedirection(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirection)

    for name, url in urls:
        req = urllib.request.Request(url, method='HEAD')
        try:
            response = opener.open(req)
            print(f"{name} ({url}): HTTP {response.getcode()}")
        except urllib.error.HTTPError as e:
            print(f"{name} ({url}): HTTP {e.code}")
        except Exception as e:
            print(f"{name} ({url}): Error {e}")

if __name__ == '__main__':
    run_smoke_test()
