import tkinter as tk
from tkinter import ttk
from num2words import num2words

# Function to convert the number to Indian currency words
def convert_to_indian_currency_words(amount):
    try:
        words = num2words(amount, lang='en_IN')
        return words
    except ValueError:
        return "Invalid Amount"

# Function to calculate the amount for a row
def calculate_row(row_frame):
    try:
        qty = int(row_frame.qty_entry.get())
        rate = float(row_frame.rate_entry.get())
        row_frame.amount_label.config(text=f"{qty * rate:.2f}")
    except ValueError:
        row_frame.amount_label.config(text="0.00")
    calculate_total()  # Dynamically update the total whenever a row changes

# Function to calculate the total amount
def calculate_total():
    total_before_tax = 0
    for row in rows:
        try:
            total_before_tax += float(row.amount_label.cget("text"))
        except ValueError:
            pass

    # Update total amount before tax
    total_label.config(text=f"Total Amount (Before Tax) : {total_before_tax:.2f}")

    # Calculate taxes
    cgst = total_before_tax * 0.025
    sgst = total_before_tax * 0.025
    igst = total_before_tax * 0.00

    # Update taxes dynamically
    cgst_label.config(text=f"CGST @ 2.5%                 : {cgst:.2f}")
    sgst_label.config(text=f"SGST @ 2.5%                 : {sgst:.2f}")
    igst_label.config(text=f"IGST @ 0%                     : {igst:.2f}")

    # Calculate grand total
    grand_total = total_before_tax + cgst + sgst + igst
    grand_total_label.config(text=f"Grand Total  : {grand_total:.2f}")
    
    # Convert grand total to integer (rounded) before converting to words
    grand_total_int = int(round(grand_total))  # Convert to integer
    grand_total_in_words = convert_to_indian_currency_words(grand_total_int)
    
    # Update the invoice amount in words
    invoice_amount_in_words_label.config(text=f"Invoice Amount in Words: {grand_total_in_words}")

# Function to delete a row
def delete_row(row_frame):
    row_frame.destroy()
    rows.remove(row_frame)
    reindex_rows()  # Re-index rows after deletion
    calculate_total()  # Recalculate total after row deletion

# Function to add a new row
def add_row():
    row_frame = tk.Frame(rows_frame)
    row_frame.grid(row=len(rows) + 1, column=0, sticky='ew', pady=5)

    # Configure uniform column widths
    row_frame.grid_columnconfigure(0, weight=1, minsize=50)  # S. No
    row_frame.grid_columnconfigure(1, weight=2, minsize=150)  # Description of Goods
    row_frame.grid_columnconfigure(2, weight=1, minsize=75)  # Quantity
    row_frame.grid_columnconfigure(3, weight=1, minsize=75)  # Rate
    row_frame.grid_columnconfigure(4, weight=1, minsize=100)  # Amount
    row_frame.grid_columnconfigure(5, weight=1, minsize=75)  # Delete button

    # S. No
    s_no_label = tk.Label(row_frame, text=str(len(rows) + 1), width=5, anchor="center")
    s_no_label.grid(row=0, column=0, padx=5, sticky='w')
    row_frame.s_no_label = s_no_label

    # Dropdown for product selection
    product_var = tk.StringVar()
    product_dropdown = ttk.Combobox(row_frame, textvariable=product_var, width=20)
    product_dropdown['values'] = ['T-shirt', 'Tracksuit', 'Sweater']
    product_dropdown.grid(row=0, column=1, padx=5, sticky='ew')
    row_frame.product_var = product_var

    # Spinbox for quantity with up and down arrows
    qty_var = tk.IntVar(value=1)  # Default value of quantity is 1
    qty_spinbox = ttk.Spinbox(row_frame, from_=0, to=10000000, textvariable=qty_var, width=10, command=lambda: calculate_row(row_frame))
    qty_spinbox.grid(row=0, column=2, padx=5, sticky='ew')
    row_frame.qty_entry = qty_spinbox

    # Bind the manual typing to trigger calculation
    qty_spinbox.bind("<KeyRelease>", lambda event: calculate_row(row_frame))

    # Entry for rate
    rate_entry = tk.Entry(row_frame, width=10)
    rate_entry.grid(row=0, column=3, padx=5, sticky='ew')
    rate_entry.bind("<KeyRelease>", lambda event: calculate_row(row_frame))  # Update on rate change
    row_frame.rate_entry = rate_entry

    # Label for amount
    amount_label = tk.Label(row_frame, text="0.00", width=10, anchor="e")
    amount_label.grid(row=0, column=4, padx=5, sticky='e')
    row_frame.amount_label = amount_label

    # Delete button
    delete_button = tk.Button(row_frame, text="Delete", command=lambda: delete_row(row_frame))
    delete_button.grid(row=0, column=5, padx=5)

    rows.append(row_frame)
    reindex_rows()  # Re-index rows after adding a new row

# Function to re-index rows after adding or deleting a row
def reindex_rows():
    for i, row in enumerate(rows):
        row.s_no_label.config(text=str(i + 1))  # Set the S. No for each row

# Function to reset all fields
def reset():
    for row in rows:
        row.destroy()
    rows.clear()
    for _ in range(5):
        add_row()
    calculate_total()

# Function to save filled rows to a text file
def save_to_file():
    with open("invoice.txt", "w") as file:
        file.write(f"{'S.No':<5} {'Description of Goods':<25} {'Quantity':<10} {'Rate':<10} {'Amount':<10}\n")
        file.write("-" * 60 + "\n")

        s_no = 1  # To re-index rows in the file
        for row in rows:
            description = row.product_var.get()
            quantity = row.qty_entry.get()
            rate = row.rate_entry.get()
            amount = row.amount_label.cget("text")
            
            if description and quantity and rate:
                file.write(f"{s_no:<5} {description:<25} {quantity:<10} {rate:<10} {amount:<10}\n")
                s_no += 1
        
        file.write("\n")
        file.write(total_label.cget("text") + "\n")
        file.write(cgst_label.cget("text") + "\n")
        file.write(sgst_label.cget("text") + "\n")
        file.write(igst_label.cget("text") + "\n")
        file.write(grand_total_label.cget("text") + "\n")
        file.write(invoice_amount_in_words_label.cget("text") + "\n")
    print("Invoice saved to 'invoice.txt'")

# Main GUI
root = tk.Tk()
root.title("Billing Application")

header_frame = tk.Frame(root)
header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

tk.Label(header_frame, text="S. No", width=5, anchor="center").grid(row=0, column=0, padx=5)
tk.Label(header_frame, text="Description of Goods", width=20, anchor="center").grid(row=0, column=1, padx=5)
tk.Label(header_frame, text="Quantity", width=10, anchor="center").grid(row=0, column=2, padx=5)
tk.Label(header_frame, text="Rate of One", width=10, anchor="center").grid(row=0, column=3, padx=5)
tk.Label(header_frame, text="Amount", width=10, anchor="center").grid(row=0, column=4, padx=5)
tk.Label(header_frame, text="Actions", width=10, anchor="center").grid(row=0, column=5, padx=5)

rows_frame = tk.Frame(root)
rows_frame.grid(row=1, column=0, sticky='ew', padx=10)

rows = []
for _ in range(5):
    add_row()

add_row_btn = tk.Button(root, text="Add Row", command=add_row)
add_row_btn.grid(row=2, column=0, sticky='w', padx=10, pady=10)

reset_btn = tk.Button(root, text="Reset", command=reset)
reset_btn.grid(row=2, column=1, sticky='w', padx=10, pady=10)

save_btn = tk.Button(root, text="Save Invoice", command=save_to_file)
save_btn.grid(row=2, column=2, sticky='w', padx=10, pady=10)

total_label = tk.Label(root, text="Total Amount (Before Tax) : 0.00", font=("Arial", 10))
total_label.grid(row=3, column=0, sticky='w', padx=10, pady=5)

cgst_label = tk.Label(root, text="CGST @ 2.5%                 : 0.00", font=("Arial", 10))
cgst_label.grid(row=4, column=0, sticky='w', padx=10, pady=5)

sgst_label = tk.Label(root, text="SGST @ 2.5%                 : 0.00", font=("Arial", 10))
sgst_label.grid(row=5, column=0, sticky='w', padx=10, pady=5)

igst_label = tk.Label(root, text="IGST @ 0%                     : 0.00", font=("Arial", 10))
igst_label.grid(row=6, column=0, sticky='w', padx=10, pady=5)

grand_total_label = tk.Label(root, text="Grand Total  : 0.00", font=("Arial", 12, 'bold'))
grand_total_label.grid(row=7, column=0, sticky='w', padx=10, pady=10)

invoice_amount_in_words_label = tk.Label(root, text="Invoice Amount in Words: Zero Only", font=("Arial", 10))
invoice_amount_in_words_label.grid(row=8, column=0, sticky='w', padx=10, pady=5)

root.mainloop()
