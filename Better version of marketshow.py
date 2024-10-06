import tkinter as tk
import requests
from tkinter import messagebox

def fetch_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin%2Cethereum&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en"
        response = requests.get(url)
        data = response.json()
        prices = {
            'bitcoin': {'usd': data[0]['current_price']},
            'ethereum': {'usd': data[1]['current_price']}
        }

        # Fetch gas fees using Etherscan API
        etherscan_api_key = 'DASKT89QYS2K511S23J82B3GF73FQSVKKH'
        url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={etherscan_api_key}"
        response = requests.get(url)    
        gas_fees = response.json()

        if gas_fees['status'] == "0":
            raise ValueError(gas_fees['message'])

        return prices, gas_fees

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching data: {e}")
        return None, None

def update_data():
    prices, gas_fees = fetch_data()
    if prices and gas_fees:
        btc_price.set(f"Bitcoin: ${prices['bitcoin']['usd']}")
        eth_price.set(f"Ethereum: ${prices['ethereum']['usd']}")
        if gas_fees['status'] == "1" and 'result' in gas_fees:
            eth_gas.set(f"Gas fees (Gwei): {gas_fees['result']['FastGasPrice']}")
        else:
            eth_gas.set("Gas fees (Gwei): Error fetching data")

# Dummy functions for the buttons
def connect_wallet():
    messagebox.showinfo("Connect Wallet", "Connecting wallet not implemented.")

def launch_bot():
    messagebox.showinfo("Launch Bot", "Launching bot not implemented.")
    
def stop_bot():
    messagebox.showinfo("Stop Bot", "Stopping bot not implemented.")

app = tk.Tk()
app.title("Crypto Tracker")
app.configure(bg='#000000')  # Set background color to black
app.geometry("500x300")  # Set window size to 500 pixels wide and 300 pixels tall

btc_price = tk.StringVar()
eth_price = tk.StringVar()
eth_gas = tk.StringVar()

update_data()  # Initial data fetch

label_opts = {'padx': 10, 'pady': 5, 'bg': '#000000', 'fg': '#ffffff', 'font': ('Arial', 14)}
tk.Label(app, textvariable=btc_price, **label_opts).grid(row=0, column=0, columnspan=2)
tk.Label(app, textvariable=eth_price, **label_opts).grid(row=1, column=0, columnspan=2)
tk.Label(app, textvariable=eth_gas, **label_opts).grid(row=2, column=0, columnspan=2)

button_opts = {'padx': 20, 'pady': 10, 'bg': '#4CAF50', 'fg': 'white', 'font': ('Arial', 12)}

# Button placement using grid() method
connect_wallet_btn = tk.Button(app, text="Connect Wallet", command=connect_wallet, **button_opts)
connect_wallet_btn.grid(row=3, column=0, padx=(50, 0), pady=(20, 0))

launch_bot_btn = tk.Button(app, text="Launch Bot", command=launch_bot, **button_opts)
launch_bot_btn.grid(row=4, column=0, padx=(50, 0), pady=(10, 0))

stop_bot_btn = tk.Button(app, text="Stop Bot", command=stop_bot, **button_opts)
stop_bot_btn.grid(row=3, column=1, padx=(50, 50), pady=(20, 0))

refresh_btn = tk.Button(app, text="Refresh", command=update_data, **button_opts)
refresh_btn.grid(row=4, column=1, padx=(50, 50), pady=(10, 0))

app.mainloop()  # Keep the application window open and responsive
