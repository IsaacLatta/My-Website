#!/usr/bin/python3

import os
import sys
import json
import requests
from datetime import datetime

bot_key = os.getenv("TELEGRAM_BOT_KEY")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

def log(level, message):
    return
    with open("./contact_debug.txt", "a") as file:
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{time_stamp} [{level}] {message}\n")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{bot_key}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses
        log("INFO", "Message successfully sent to Telegram.")
        return True
    except requests.exceptions.RequestException as e:
        log("ERROR", f"Failed to send to Telegram: {e}")
        return False

def main():
    if not bot_key or not chat_id:
        log("ERROR", "Environment variables TELEGRAM_BOT_KEY or TELEGRAM_CHAT_ID are not set.")
        sys.stdout.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
        sys.stdout.flush()
        sys.exit(1)

    try:
        input_args = sys.stdin.read()
        log("INFO", f"Input received: {input_args}")

        args = json.loads(input_args)
        if not isinstance(args, dict):
            raise ValueError("Input is not a valid JSON object.")

        name = args.get("name", "Unknown")
        email = args.get("email", "Unknown")
        message = args.get("message", "No message provided")
        telegram_message = (
            f"New Contact Request\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Message: {message}"
        )

        if send_to_telegram(telegram_message):
            sys.stdout.write("HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n")
        else:
            sys.stdout.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
    except json.JSONDecodeError as e:
        log("ERROR", f"Invalid JSON input: {e}")
        sys.stdout.write("HTTP/1.1 400 Bad Request\r\n\r\n")
    except ValueError as e:
        log("ERROR", f"Validation error: {e}")
        sys.stdout.write("HTTP/1.1 400 Bad Request\r\n\r\n")
    except Exception as e:
        log("ERROR", f"Unexpected error: {e}")
        sys.stdout.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
    finally:
        sys.stdout.flush()

if __name__ == "__main__":
    main()
