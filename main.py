import os
import sys
import pandas as pd
from data_analyzer import analyze_data
from report_generator import generate_text_report, generate_visual_report
from whatsapp_sender import send_whatsapp_message
from twilio.rest import Client

ACCOUNT_SID = 'AC0b09562bba910c76e315aa6d90a1f097'
AUTH_TOKEN = '89d0cb2c9d6662d54059a51aaa86a270'
TWILIO_PHONE_NUMBER = 'whatsapp:+14155238886'
YOUR_PHONE_NUMBER = 'whatsapp:+584241420016'

EXCEL_FILE_NAME = 'Ventas-Fundamentos.xlsx'
REPORTS_FOLDER = 'Reports'
REPORT_TEXT_FILE_NAME = 'Business_Report.pdf'
REPORT_IMAGE_BASE_NAME = 'report_chart'
REPORT_IMAGE_EXTENSION = '.png'

def read_excel_data(file_name):
    if not os.path.exists(file_name):
        print(f"Error: The Excel file '{file_name}' was not found in the current directory.")
        print("Please ensure the Excel file is in the same directory as the script.")
        sys.exit(1)
    try:
        all_sheets_df = pd.read_excel(file_name, sheet_name=None)
        print(f"Data successfully loaded from all sheets in '{file_name}'.")
        return all_sheets_df
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        sys.exit(1)

def main():
    print("Starting the RPA process...")
    all_dfs = read_excel_data(EXCEL_FILE_NAME)

    analysis_results = analyze_data(all_dfs)
    if not analysis_results:
        print("No analysis results were generated. Exiting RPA.")
        sys.exit(1)

    text_report_path = generate_text_report(analysis_results, REPORTS_FOLDER, REPORT_TEXT_FILE_NAME)
    image_paths = generate_visual_report(analysis_results, REPORTS_FOLDER, REPORT_IMAGE_BASE_NAME, REPORT_IMAGE_EXTENSION)

    print("\nAttempting to send reports to WhatsApp...")
    twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)
    ngrok_public_url = 'https://3c0fc4c26d76.ngrok-free.app'

    media_urls_for_whatsapp = []
    text_report_url_to_send = None

    if not ngrok_public_url.endswith('/'): ngrok_public_url += '/'
    if text_report_path and os.path.exists(text_report_path):
        text_filename = os.path.basename(text_report_path)
        text_report_url_to_send = f"{ngrok_public_url}{text_filename}"
        print(f"Text report URL: {text_report_url_to_send}")
    else: print("Warning: Text report file not found, skipping URL generation for it.")

    for local_image_path in image_paths:
        image_filename = os.path.basename(local_image_path)
        constructed_url = f"{ngrok_public_url}{image_filename}"
        media_urls_for_whatsapp.append(constructed_url)
        print(f"Local image path: {local_image_path} -> Constructed URL: {constructed_url}")
    print(f"Final list of image URLs to send: {media_urls_for_whatsapp}")

    if text_report_url_to_send:
        print(f"\nSending text report as a file: {text_report_url_to_send}")
        send_whatsapp_message(twilio_client, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER,
                              "Here is your business report:",
                              media_urls=[text_report_url_to_send])
    else:
        send_whatsapp_message(twilio_client, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER,
            "Business report could not be generated or sent.")

    if media_urls_for_whatsapp:
        print("\nSending visual reports (graphs) as separate messages...")
        caption_map = {
            f"{REPORT_IMAGE_BASE_NAME}_sales_by_vehicle{REPORT_IMAGE_EXTENSION}": "Sales by Vehicle ID Chart",
            f"{REPORT_IMAGE_BASE_NAME}_sales_by_channel{REPORT_IMAGE_EXTENSION}": "Sales by Channel Chart",
            f"{REPORT_IMAGE_BASE_NAME}_sales_over_time{REPORT_IMAGE_EXTENSION}": "Monthly Sales Trend Chart",
            f"{REPORT_IMAGE_BASE_NAME}_vehicles_by_brand{REPORT_IMAGE_EXTENSION}": "Vehicles by Brand Chart",
            f"{REPORT_IMAGE_BASE_NAME}_vehicles_by_type{REPORT_IMAGE_EXTENSION}": "Vehicles by Type Chart",
            f"{REPORT_IMAGE_BASE_NAME}_registrations_over_time{REPORT_IMAGE_EXTENSION}": "New Registrations Over Time Chart"
        }

        for url in media_urls_for_whatsapp:
            filename = os.path.basename(url)
            caption = caption_map.get(filename, f"Business Report Chart: {filename}")
            print(f"Sending chart: {caption} from {url}")
            send_whatsapp_message(twilio_client, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER, caption, media_urls=[url])
    else: print("No public URLs provided for images or images not generated. Skipping visual report sending.")

    print("\nRPA process completed.")

if __name__ == "__main__": main()