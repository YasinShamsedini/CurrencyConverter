import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from PIL import Image, ImageTk
import datetime
import decimal  


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("830x500")
        self.conf_style()

        # Database connection string.  Maybe u need to change this section based on your DRIVER, Server,...
        self.db_conn_string = (
            r'DRIVER={ODBC Driver 18 for SQL Server};'
            r'SERVER=.\SQLEXPRESS;'
            r'DATABASE=CurrencyConverter;'
            r'TrustServerCertificate=yes;'
            r'Authentication=ActiveDirectoryIntegrated;'
        )

        # Frames for different sections of the UI
        self.main_frame = ttk.Frame(self.root)
        self.crud_frame = ttk.Frame(self.root)
        self.report_frame = ttk.Frame(self.root)

        self.main_ui()
        self.crud_ui()
        self.report_ui()
        self.show_main()

        self.root.configure(bg='#020f29')

    def conf_style(self):
        """Configures the visual style for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        bg_color = '#020f29'
        fg_color = '#ffffff'
        entry_bg = '#3d3d3d'
        button_bg = '#4d4d4d'
        highlight = '#5d5d5d'

        # Base style
        style.configure('.',
                        background=bg_color,
                        foreground=fg_color,
                        font=('Arial', 10))

        # Widget styles
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TEntry',
                        fieldbackground=entry_bg,
                        foreground=fg_color,
                        insertcolor=fg_color)
        style.configure('TCombobox',
                        fieldbackground=entry_bg,
                        foreground='black',
                        background=entry_bg)
        style.configure('TButton',
                        background=button_bg,
                        relief='flat',
                        padding=6)
        style.map('TButton',
                  background=[('active', highlight)],
                  foreground=[('active', fg_color)])

        # Treeview styles
        style.configure('Treeview',
                        background=entry_bg,
                        fieldbackground=entry_bg,
                        foreground=fg_color,
                        rowheight=25)
        style.configure('Treeview.Heading',
                        background=button_bg,
                        foreground=fg_color,
                        relief='flat')
        style.map('Treeview',
                  background=[('selected', highlight)])

        style.configure('TitleBar.TFrame', background='#20355c')
        style.configure('TitleBar.TLabel', foreground=fg_color, background='#20355c', font=('Arial', 12, 'bold'))

    def main_ui(self):
        """Creates the main UI elements for currency conversion."""
        frame = self.main_frame
        frame.grid(row=0, column=0, sticky='nsew')

        frm1 = ttk.Frame(frame)
        frm1.grid(row=2, column=1, columnspan=3, rowspan=3, sticky='nsew', padx=50, pady=50)

        # Configure grid columns
        frm1.grid_columnconfigure(0, weight=1)
        frm1.grid_columnconfigure(1, weight=2)

        # Widgets for input
        ttk.Label(frm1, text="Amount:", font=("Arial", 15)).grid(row=0, column=0, sticky='e', pady=10)
        self.amount_entry = ttk.Entry(frm1, width=30)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        ttk.Label(frm1, text="From Currency:", font=("Arial", 12)).grid(row=1, column=0, sticky='e', pady=10)
        self.from_currency = ttk.Combobox(frm1, width=28, state='readonly')
        self.from_currency.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        ttk.Label(frm1, text="To Currency:", font=("Arial", 12)).grid(row=2, column=0, sticky='e', pady=10)
        self.to_currency = ttk.Combobox(frm1, width=28, state='readonly')
        self.to_currency.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        # Buttons frame
        btns = ttk.Frame(frm1)
        btns.grid(row=3, column=0, columnspan=2, pady=20, sticky='ew')
        btns.grid_columnconfigure(0, weight=1)
        btns.grid_columnconfigure(1, weight=1)

        ttk.Button(btns, text="Convert", command=self.convert).grid(row=0, column=0, padx=5, sticky='ew')
        ttk.Button(btns, text="Manage Currencies & CRUD", command=self.show_crud).grid(row=0, column=1, padx=5,
                                                                                          sticky='ew')
        ttk.Button(btns, text="Report", command=self.show_report).grid(row=0, column=2, padx=5,
                                                                        sticky='ew')  # Add a button to open report

        # Result label
        self.result_label = ttk.Label(frm1, text="", font=('Arial', 14, 'bold'), anchor='center')
        self.result_label.grid(row=0, column=2, sticky='e', pady=10)

        # Image loading
        image_path = r"D:\Users\BLACK-RAYANE\Downloads\pngimg.com - money_PNG3520.png"
        try:
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(image)
            ttk.Label(frm1, image=self.image_tk).grid(row=3, column=2, columnspan=2, pady=1, padx=50, sticky='ew')
        except:
            print('Error loading image!')

        self.populate_currencies()

    def crud_ui(self):
        """Creates the UI for managing currency exchange rates (CRUD operations)."""
        frame = self.crud_frame
        frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Treeview for displaying currency rates
        self.tree = ttk.Treeview(frame, columns=('ID', 'Currency', 'Rate', 'Updated'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Currency', text='Currency')
        self.tree.heading('Rate', text='Rate')
        self.tree.heading('Updated', text='Last Updated')

        # Configure column alignment
        self.tree.column("ID", anchor='center')
        self.tree.column("Currency", anchor='center')
        self.tree.column("Rate", anchor='center')
        self.tree.column("Updated", anchor='center')

        self.tree.grid(row=0, column=0, columnspan=4, sticky='nsew', pady=10)
        self.tree.bind("<ButtonRelease-1>", self.select_item)

        # Labels and entry fields for editing currency rates
        ttk.Label(frame, text="Currency Code:").grid(row=1, column=0, padx=5, pady=10, sticky='e')
        self.crud_code = ttk.Entry(frame, width=10)
        self.crud_code.grid(row=1, column=1, padx=5, pady=10, sticky='w')

        ttk.Label(frame, text="Exchange Rate:").grid(row=1, column=1, padx=5, pady=10, sticky='e')
        self.crud_rate = ttk.Entry(frame, width=15)
        self.crud_rate.grid(row=1, column=2, padx=5, pady=10, sticky='w')

        # Buttons for CRUD operations
        ttk.Button(frame, text="Add", command=self.add_rate).grid(row=3, column=0, padx=10, pady=5, sticky='ew', columnspan=1)
        ttk.Button(frame, text="Update", command=self.update_rate).grid(row=3, column=1, padx=10, pady=5, sticky='ew', columnspan=1)
        ttk.Button(frame, text="Delete", command=self.delete_rate).grid(row=3, column=2, padx=10, pady=5, sticky='ew', columnspan=2)
        ttk.Button(frame, text="Back to Converter", command=self.show_main).grid(row=4, column=0, columnspan=4,
                                                                                 pady=10, padx=10, sticky='ew')

    def report_ui(self):
        """Creates the UI for displaying conversion history."""
        frame = self.report_frame
        frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Treeview for displaying conversion history
        self.report_tree = ttk.Treeview(frame,
                                         columns=('ID', 'From', 'To', 'Amount', 'Converted Amount', 'Date'),
                                         show='headings')
        self.report_tree.heading('ID', text='ID')
        self.report_tree.heading('From', text='From Currency')
        self.report_tree.heading('To', text='To Currency')
        self.report_tree.heading('Amount', text='Amount')
        self.report_tree.heading('Converted Amount', text='Converted Amount')
        self.report_tree.heading('Date', text='Date')
        self.report_tree.grid(row=0, column=0, sticky='nsew', pady=10)

        ttk.Button(frame, text="Back to main", command=self.show_main).grid(row=1, column=0, pady=10, padx=2,
                                                                             sticky='w')

    def show_main(self):
        """Displays the main currency converter UI."""
        self.crud_frame.grid_remove()
        self.report_frame.grid_remove()
        self.main_frame.grid()
        self.populate_currencies()

    def show_crud(self):
        """Displays the currency management UI."""
        self.main_frame.grid_remove()
        self.report_frame.grid_remove()
        self.crud_frame.grid()
        self.load_rates()

    def show_report(self):
        """Displays the conversion report UI."""
        self.main_frame.grid_remove()
        self.crud_frame.grid_remove()
        self.report_frame.grid()
        self.load_report()

    def load_report(self):
        """Loads conversion history data from the database into the report treeview."""
        # Clear existing data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        try:
            with pyodbc.connect(self.db_conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT ID, FromCurrency, ToCurrency, Amount, ConvertedAmount, ConversionDate FROM ConversionHistory")
                    for row in cursor.fetchall():
                        # Format date and insert into treeview
                        formatted_date = row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else ""
                        self.report_tree.insert('', 'end',
                                                values=(row[0], row[1], row[2], row[3], row[4],
                                                        formatted_date))

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Error", "Error loading report data.")

    def populate_currencies(self):
        """Populates the currency comboboxes with available currencies from the database."""
        try:
            with pyodbc.connect(self.db_conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT CurrencyCode FROM ExchangeRates")
                    currencies = [row[0] for row in cursor.fetchall()]
                    self.from_currency['values'] = currencies
                    self.to_currency['values'] = currencies
                    if currencies:
                        self.from_currency.current(0)
                        self.to_currency.current(0)
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Error", f"Error populating currencies: {e}")

    def load_rates(self):
        """Loads exchange rates from the database into the rate management treeview."""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with pyodbc.connect(self.db_conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ID, CurrencyCode, Rate, LastUpdated FROM ExchangeRates")
                    for row in cursor.fetchall():
                        # Extract values
                        id_val = row[0]
                        currency_code = row[1]
                        rate_val = row[2]
                        updated_val = row[3]

                        # Convert Rate to string
                        if isinstance(rate_val, (int, float, decimal.Decimal)):
                            rate_val = str(rate_val)
                        else:
                            rate_val = str(rate_val)

                        # Convert LastUpdated to string
                        if isinstance(updated_val, datetime.datetime):
                            updated_val = updated_val.strftime("%Y-%m-%d %H:%M:%S")
                        elif updated_val is None:
                            updated_val = ""
                        else:
                            updated_val = str(updated_val)

                        self.tree.insert('', 'end', values=(id_val, currency_code, rate_val, updated_val))

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Error", f"Database error loading exchange rates: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            messagebox.showerror("Error", f"Unexpected error loading exchange rates: {e}")

    def select_item(self, event):
        """Populates the entry fields with the selected item's data from the rate management treeview."""
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            item_values = self.tree.item(item_id)['values']

            # Populate entry fields
            self.crud_code.delete(0, tk.END)
            self.crud_code.insert(0, str(item_values[1]))  # Currency Code

            self.crud_rate.delete(0, tk.END)
            try:
                rate = float(item_values[2])  # Convert Rate to float
                self.crud_rate.insert(0, str(rate))
            except ValueError:
                self.crud_rate.insert(0, item_values[2])  # if it is not a number, insert it as is.

    def get_rate(self, currency_code):
        """Retrieves the exchange rate for a given currency code from the database."""
        try:
            with pyodbc.connect(self.db_conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT Rate FROM ExchangeRates WHERE CurrencyCode = ?", (currency_code,))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except pyodbc.Error as e:
            print(f"Database error: {e}")  # Log the error
            messagebox.showerror("Error", "A database error occurred.")
            return None

    def convert(self):
        """Converts the amount from one currency to another and saves the conversion to the database."""
        try:
            # Get input values
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            # Get exchange rates
            from_rate = self.get_rate(from_curr)
            to_rate = self.get_rate(to_curr)

            if from_rate is None or to_rate is None:
                messagebox.showerror("Error", "Could not retrieve exchange rates.")
                return

            # Perform conversion
            converted_amount = (amount / float(from_rate)) * float(to_rate)
            result_text = f"{amount:.2f} {from_curr} = {converted_amount:.2f} {to_curr}"
            self.result_label.config(text=result_text)

            # Save conversion to database
            with pyodbc.connect(self.db_conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO ConversionHistory (FromCurrency, ToCurrency, Amount, ConvertedAmount) VALUES (?, ?, ?, ?)",
                        (from_curr, to_curr, amount, converted_amount))
                    conn.commit()

        except ValueError:
            messagebox.showerror("Error", "Enter valid input")

    def add_rate(self):
        """Adds a new currency exchange rate to the database."""
        code = self.crud_code.get().strip().upper()
        rate_str = self.crud_rate.get().strip()

        if not code or not rate_str:  # Check if either are empty
            messagebox.showerror("Error", "Fill both fields")
            return

        if not all(c.isalpha() for c in code):  # Check if the code is alphabetic
            messagebox.showerror("Error", "Currency code should contain alphabet characters only")
            return

        try:
            rate = float(rate_str)  # Convert to float
            with pyodbc.connect(self.db_conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO ExchangeRates (CurrencyCode, Rate) VALUES (?, ?)", (code, rate))
                    conn.commit()
            self.load_rates()
            messagebox.showinfo("Success", "Rate added")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Invalid rate. Please enter a valid number.")
        except pyodbc.IntegrityError:
            messagebox.showerror("Error", "Currency code already exists.")
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def update_rate(self):
        """Updates an existing currency exchange rate in the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a currency to update.")
            return

        code = self.crud_code.get().strip().upper()
        rate_str = self.crud_rate.get().strip()

        if not code or not rate_str:
            messagebox.showerror("Error", "Fill both fields")
            return

        try:
            rate = float(rate_str)
            item_id = selected_item[0]  # Get the selected item's ID
            with pyodbc.connect(self.db_conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE ExchangeRates SET Rate = ?, LastUpdated = GETDATE() WHERE CurrencyCode = ?",
                                   (rate, code))
                    conn.commit()

            self.load_rates()
            messagebox.showinfo("Success", "Rate updated")
            self.clear_entries()
            self.tree.selection_remove(item_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid rate. Please enter a valid number.")
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def delete_rate(self):
        """Deletes a currency exchange rate from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a currency to delete.")
            return

        code = self.crud_code.get().strip().upper()
        if not code:
            messagebox.showerror("Error", "Currency Code field is required for deletion.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {code}?"):
            try:
                item_id = selected_item[0]  # Get the selected item's ID
                with pyodbc.connect(self.db_conn_string) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("DELETE FROM ExchangeRates WHERE CurrencyCode = ?", (code,))
                        conn.commit()
                self.load_rates()
                messagebox.showinfo("Success", f"{code} deleted successfully.")
                self.clear_entries()
                self.tree.selection_remove(item_id)
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

    def clear_entries(self):
        """Clear the Currency Code and Exchange Rate entry fields."""
        self.crud_code.delete(0, tk.END)
        self.crud_rate.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
