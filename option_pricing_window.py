"""
@author: Matthew Gotham

Opens a widget for pricing options, using the code in
binomial_option_pricer.py.
"""


import tkinter as tk
from tkinter import ttk, messagebox
from binomial_option_pricer import get_premium_greeks

# Workhorse function
def run_function():
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

# Main window
root = tk.Tk()
root.title("Binomial Option Price Calculator")
root.geometry("500x300")

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

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

ttk.Label(frame, text='INPUTS').grid(row=0, column=0, columnspan=4,
                                     pady=(0,15))
for row, name in enumerate(parameters):
    ttk.Label(frame, text=name).grid(row=row+1, column=0, sticky="w", padx=5,
                                     pady=2)
    entry = ttk.Entry(frame, width=8)
    entry.grid(row=row+1, column=2)
    entries[name] = entry
entries['Based on'].insert(tk.END, '252')

# Boolean inputs
is_call = tk.BooleanVar(value=True)
is_american = tk.BooleanVar(value=False)
latest_row=len(parameters)+1
ttk.Label(frame, text='Option type').grid(row=latest_row, column=0,
                                          sticky='w', padx=5, pady=2)
ttk.Radiobutton(frame, text='Call', variable=is_call,
                value=True).grid(row=latest_row, column=2, sticky='w')
ttk.Radiobutton(frame, text='Put', variable=is_call,
                value=False).grid(row=latest_row, column=3, sticky='w')
ttk.Label(frame, text='Exercise type').grid(row=latest_row+1, column=0,
                                            sticky='w', padx=5, pady=2)
ttk.Radiobutton(frame, text='European', variable=is_american,
                value=False).grid(row=latest_row+1, column=2, sticky='w')
ttk.Radiobutton(frame, text='American', variable=is_american,
                value=True).grid(row=latest_row+1, column=3, sticky='w')

# Units
dollar_rows = [1,2]
pct_rows = [5,6,7]
for dollar_row in dollar_rows:
    ttk.Label(frame, text='$').grid(row=dollar_row, column=1)
for pct_row in pct_rows:
    ttk.Label(frame, text='%').grid(row=pct_row, column=3, stick='w')
ttk.Label(frame, text='days in a year').grid(row=4, column=3)

# Run button
ttk.Button(frame, text="Calculate", command=run_function).grid(
    row=0, column=5, columnspan=3, pady=(0,15))

# Outputs
ttk.Label(frame, text="Premium").grid(row=1, column=5, sticky="w",
                                         padx=15, pady=2)
ttk.Label(frame, text='$').grid(row=1, column=6)
ttk.Label(frame, text='Delta').grid(row=2, column=5, sticky="w", padx=15,
                                    pady=2)
ttk.Label(frame, text='Gamma').grid(row=3, column=5, sticky="w", padx=15,
                                    pady=2)
ttk.Label(frame, text='Theta').grid(row=4, column=5, sticky="w", padx=15,
                                    pady=2)
#
premium = tk.Text(frame, height=1, width=8)
premium.grid(row=1, column=7)
delta = tk.Text(frame, height=1, width=8)
delta.grid(row=2, column=7)
gamma = tk.Text(frame, height=1, width=8)
gamma.grid(row=3, column=7)
theta = tk.Text(frame, height=1, width=8)
theta.grid(row=4, column=7)

root.mainloop()