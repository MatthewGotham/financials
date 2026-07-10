"""
@author: Matthew Gotham

Opens a widget for pricing options and calculating implied volatility,
using the code in binomial_option_pricer.py.
"""

#%% Preliminaries


import tkinter as tk
from tkinter import ttk, messagebox
from binomial_option_pricer import get_premium_greeks, get_iv


# Main window
root = tk.Tk()
root.title("Binomial Option Price Calculator")
root.geometry("500x300")

# Create the notebook.
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create a frame for each tab.
tab1 = ttk.Frame(notebook, padding=15)
notebook.add(tab1, text="Calculate Premium")
tab2 = ttk.Frame(notebook, padding=15)
notebook.add(tab2, text="Calculate Implied Volatility")


#%% Calculate premium tab

# Workhorse function
def calculate_premium():
    try:
        price = float(entries["Current price"].get())
        strike = float(entries["Strike price"].get())
        dte = int(entries["Days to expiry"].get())
        rfr = float(entries["Risk-free rate"].get())/100
        vol = float(entries["Volatility"].get())/100
        call = is_call.get()
        american = is_american.get()
        div_yield = float(entries["Dividend yield"].get())/100
        days_in_year = int(entries["Based on"].get())

        results = get_premium_greeks(price, strike, dte, rfr, vol, call,
                                     american, div_yield, days_in_year)

        for output,result in [(premium,results['Premium']),
                              (delta,results['Delta']),
                              (gamma,results['Gamma']),
                              (theta,results['Theta'])]:
            output.delete("1.0", tk.END)
            output.insert(tk.END, str(round(result,4)))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Input fields
parameters = [
    "Current price",
    "Strike price",
    "Days to expiry",
    "Based on",
    "Risk-free rate",
    "Volatility",
    "Dividend yield"]

entries = {}

ttk.Label(tab1, text='INPUTS').grid(row=0, column=0, columnspan=4,
                                     pady=(0,15))
for row, name in enumerate(parameters):
    ttk.Label(tab1, text=name).grid(row=row+1, column=0, sticky="w", padx=5,
                                     pady=2)
    entry = ttk.Entry(tab1, width=8)
    entry.grid(row=row+1, column=2)
    entries[name] = entry
entries['Based on'].insert(tk.END, '252')

# Boolean inputs
is_call = tk.BooleanVar(value=True)
is_american = tk.BooleanVar(value=False)
latest_row=len(parameters)+1
ttk.Label(tab1, text='Option type').grid(row=latest_row, column=0,
                                          sticky='w', padx=5, pady=2)
ttk.Radiobutton(tab1, text='Call', variable=is_call,
                value=True).grid(row=latest_row, column=2, sticky='w')
ttk.Radiobutton(tab1, text='Put', variable=is_call,
                value=False).grid(row=latest_row, column=3, sticky='w')
ttk.Label(tab1, text='Exercise type').grid(row=latest_row+1, column=0,
                                            sticky='w', padx=5, pady=2)
ttk.Radiobutton(tab1, text='European', variable=is_american,
                value=False).grid(row=latest_row+1, column=2, sticky='w')
ttk.Radiobutton(tab1, text='American', variable=is_american,
                value=True).grid(row=latest_row+1, column=3, sticky='w')

# Units
dollar_rows = [1,2]
pct_rows = [5,6,7]
for dollar_row in dollar_rows:
    ttk.Label(tab1, text='$').grid(row=dollar_row, column=1)
for pct_row in pct_rows:
    ttk.Label(tab1, text='%').grid(row=pct_row, column=3, stick='w')
ttk.Label(tab1, text='days in a year').grid(row=4, column=3)

# Run button
ttk.Button(tab1, text="Calculate", command=calculate_premium).grid(
    row=0, column=5, columnspan=3, pady=(0,15))

# Outputs
ttk.Label(tab1, text="Premium").grid(row=1, column=5, sticky="w",
                                         padx=15, pady=2)
ttk.Label(tab1, text='$').grid(row=1, column=6)
ttk.Label(tab1, text='Delta').grid(row=2, column=5, sticky="w", padx=15,
                                    pady=2)
ttk.Label(tab1, text='Gamma').grid(row=3, column=5, sticky="w", padx=15,
                                    pady=2)
ttk.Label(tab1, text='Theta').grid(row=4, column=5, sticky="w", padx=15,
                                    pady=2)
#
premium = tk.Text(tab1, height=1, width=8)
premium.grid(row=1, column=7)
delta = tk.Text(tab1, height=1, width=8)
delta.grid(row=2, column=7)
gamma = tk.Text(tab1, height=1, width=8)
gamma.grid(row=3, column=7)
theta = tk.Text(tab1, height=1, width=8)
theta.grid(row=4, column=7)


#%% Caculated implied volatility tab

# Workhorse function
def calculate_iv():
    try:
        price = float(entries2["Current price"].get())
        strike = float(entries2["Strike price"].get())
        premium = float(entries2['Premium'].get())
        dte = int(entries2["Days to expiry"].get())
        rfr = float(entries2["Risk-free rate"].get())/100
        call = is_call2.get()
        american = is_american2.get()
        div_yield = float(entries2["Dividend yield"].get())/100
        days_in_year = int(entries2["Based on"].get())

        implied_vol = get_iv(price, strike, premium, dte, rfr, call, american,
                             div_yield, days_in_year)
        results2 = get_premium_greeks(price, strike, dte, rfr, implied_vol,
                                      call, american, div_yield, days_in_year)
        iv.delete("1.0", tk.END)
        iv.insert(tk.END, implied_vol*100)
        for output,result in [(delta2,results2['Delta']),
                              (gamma2,results2['Gamma']),
                              (theta2,results2['Theta'])]:
            output.delete("1.0", tk.END)
            output.insert(tk.END, str(round(result,4)))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Input fields
parameters2 = [
    "Current price",
    "Strike price",
    "Premium",
    "Days to expiry",
    "Based on",
    "Risk-free rate",
    "Dividend yield"]

entries2 = {}

ttk.Label(tab2, text='INPUTS').grid(row=0, column=0, columnspan=4, pady=(0,15))
for row, name in enumerate(parameters2):
    ttk.Label(tab2, text=name).grid(row=row+1, column=0, sticky="w", padx=5,
                                    pady=2)
    entry = ttk.Entry(tab2, width=8)
    entry.grid(row=row+1, column=2)
    entries2[name] = entry
entries2['Based on'].insert(tk.END, '252')

# Boolean inputs
is_call2 = tk.BooleanVar(value=True)
is_american2 = tk.BooleanVar(value=False)
latest_row2 = len(parameters2)+1
ttk.Label(tab2, text='Option type').grid(row=latest_row2, column=0,
                                         sticky='w', padx=5, pady=2)
ttk.Radiobutton(tab2, text='Call', variable=is_call2,
                value=True).grid(row=latest_row2, column=2, sticky='w')
ttk.Radiobutton(tab2, text='Put', variable=is_call2,
                value=False).grid(row=latest_row2, column=3, sticky='w')
ttk.Label(tab2, text='Exercise type').grid(row=latest_row2+1, column=0,
                                           sticky='w', padx=5, pady=2)
ttk.Radiobutton(tab2, text='European', variable=is_american2,
                value=False).grid(row=latest_row2+1, column=2, sticky='w')
ttk.Radiobutton(tab2, text='American', variable=is_american2,
                value=True).grid(row=latest_row2+1, column=3, sticky='w')

# Units
dollar_rows2 = [1,2,3]
pct_rows2 = [6,7]
for dollar_row in dollar_rows2:
    ttk.Label(tab2, text='$').grid(row=dollar_row, column=1)
for pct_row in pct_rows2:
    ttk.Label(tab2, text='%').grid(row=pct_row, column=3, stick='w')
ttk.Label(tab2, text='days in a year').grid(row=4, column=3)

# Run button
ttk.Button(tab2, text="Calculate", command=calculate_iv).grid(
    row=0, column=5, columnspan=3, pady=(0,15))

# Outputs
ttk.Label(tab2, text="Implied volatility").grid(row=1, column=5, sticky="w",
                                                padx=15, pady=2)
ttk.Label(tab2, text='%').grid(row=1, column=7)
ttk.Label(tab2, text='Delta').grid(row=2, column=5, sticky="w", padx=15,
                                    pady=2)
ttk.Label(tab2, text='Gamma').grid(row=3, column=5, sticky="w", padx=15,
                                    pady=2)
ttk.Label(tab2, text='Theta').grid(row=4, column=5, sticky="w", padx=15,
                                    pady=2)
#
iv = tk.Text(tab2, height=1, width=8)
iv.grid(row=1, column=6)
delta2 = tk.Text(tab2, height=1, width=8)
delta2.grid(row=2, column=6)
gamma2 = tk.Text(tab2, height=1, width=8)
gamma2.grid(row=3, column=6)
theta2 = tk.Text(tab2, height=1, width=8)
theta2.grid(row=4, column=6)


#%% Finish

root.mainloop()