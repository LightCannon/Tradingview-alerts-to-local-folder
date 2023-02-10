  # Tradingview alerts to local folder

## Perquisites
 Ngrok account authentication token. Refer to next section for how to get the token
 ## Ngrok 
 

 1. Create Ngrok account from [here](https://dashboard.ngrok.com/signup)
 2. An email will be sent to you with verification link to verify your account
 3. Navigate to your dashboard to get auth token (https://dashboard.ngrok.com/get-started/your-authtoken
 4. Copy your authentication token as we will need it later![enter image description here](https://i.imgur.com/3gT6ooJ.png)


## Running the app

1. Double click main.exe
2. Click on "Token" button, a pop up will request your auth token
3. Paste the token from your ngrok dashboard![enter image description here](https://i.imgur.com/51gTiJS.png)![enter image description here](https://i.imgur.com/7vcVqri.png)
5. Press Ok, now ngrok will automatically use this account to make the required tunnel.
6. Click on Browse  button, and select the folder you would like to forward the notifications to as .csv

## Important note
Do **not** delete the .env file near the exe. it holds the settings for the app. Also, don't delete ngrok.exe 
