import requests
import os

STATUS_URL = "https://4277980205320394.hostedstatus.com/1.0/status/59db90dbcdeb2f04dadcf16d"
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
STATE_FILE = "last_status.txt"


def get_last_status():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return None


def save_last_status(status_code):
    with open(STATE_FILE, "w") as f:
        f.write(str(status_code))


def send_discord_alert(status_desc, status_code):
    emoji = "🟠" if status_code != "100" else "✅"
    payload = {
        "content": f"{emoji} **Roblox Status**: {status_desc}"
    }
    requests.post(WEBHOOK_URL, json=payload, timeout=10)


def main():
    r = requests.get(STATUS_URL, timeout=10)
    data = r.json()
    status_code = str(data["result"]["status_overall"]["status_code"])
    status_desc = data["result"]["status_overall"]["status"]

    last_status = get_last_status()

    if status_code != last_status:
        send_discord_alert(status_desc, status_code)
        save_last_status(status_code)


if __name__ == "__main__":
    main()
