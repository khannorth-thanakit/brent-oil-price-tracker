import yfinance as yf
import pandas as pd
import gspread
import datetime
import os # Import the os module

def update_brent_price(request):
  # Get credentials from environment variables
  # These environment variables would hold the content of your service account JSON file
  # Set these in the Cloud Function configuration
  google_credentials = {
      "type": os.environ.get("GOOGLE_TYPE"),
      "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
      "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
      "private_key": os.environ.get("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"), # Important: Replace \\n with actual newlines
      "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
      "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
      "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
      "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
      "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
      "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL")
  }

  # Authenticate using the dictionary
  client = gspread.service_account_from_dict(google_credentials)

  # Open Google sheet
  sheet = client.open("Brent Oil Prices").sheet1

  # ... (rest of your code remains the same)
  #Get data of Brent oil from yfinance
  data = yf.download("BZ=F", period="5d", interval="1d")
  data.reset_index(inplace=True)
  lasted_row = data.iloc[-1]

  #Prepare data (clean data)
  row_data = [
      lasted_row['Date'].strftime("%Y-%m-%d"), # Corrected variable name here
      lasted_row['Open'],
      lasted_row['High'],
      lasted_row['Low'],
      lasted_row['Close'],
      lasted_row['Adj Close'],
      lasted_row['Volume']
      ]
  # Append the data to the sheet (you're missing this line in your original code)
  sheet.append_row(row_data)

  return "Brent price updated successfully!" # Cloud Functions expect a response
