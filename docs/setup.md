
```markdown
# Currency Converter Application Setup Guide

This is a Python-based GUI application built using **Tkinter** for currency conversion. The application connects to a **SQL Server** database to fetch currency exchange rates and store conversion history. Here's how you can set up and run this project.

## Prerequisites

Before running the application, you need to install a few dependencies:

### 1. **Install Python:**
   Ensure that you have **Python 3.x** installed on your system. You can download it from the official Python website:  
   [Download Python](https://www.python.org/downloads/)

### 2. **Install Required Python Libraries:**
   You can install the necessary Python libraries by running the following command in your terminal:

   ```bash
   pip install tkinter pyodbc pillow
   ```

   - **Tkinter:** For the GUI interface.
   - **pyodbc:** To connect to the SQL Server database.
   - **Pillow:** To handle image files (e.g., logo or images displayed in the GUI).

### 3. **Install SQL Server (If not already installed):**
   You need to have a **SQL Server** instance running on your machine or a remote server. You can use **SQL Server Express Edition** if you're setting it up locally.  
   You can download SQL Server from the following link:  
   [Download SQL Server Express](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)

   If you're using a local instance, ensure that it's running on `.\SQLEXPRESS`.







### 4. **Create the Database and Tables:**

   After setting up SQL Server, you need to create the **CurrencyConverter** database and the required table(s). insert the SQL code in a SSMS -> New-Query SQL and make the database ready to run the Software.

   SQL code will:
   - Create a `CurrencyConverter` database.
   - Create an `ExchangeRates` table with sample currency rates for USD, EUR, GBP, JPY, and CAD.





### 5. **Configure Database Connection:**

   In the Python code, there is a section where the **database connection string** is defined:

   ```python
   self.db_conn_string = (
       r'DRIVER={ODBC Driver 18 for SQL Server};'
       r'SERVER=.\SQLEXPRESS;'
       r'DATABASE=CurrencyConverter;'
       r'TrustServerCertificate=yes;'
       r'Authentication=ActiveDirectoryIntegrated;'
   )
   ```

   - Make sure the `SERVER` is correct (e.g., `.\SQLEXPRESS` if you're using SQL Server Express locally).
   - If you're using a different SQL Server version or instance, modify the `SERVER` and `Authentication` accordingly.




### 6. **Run the Application:**

   To start the application, navigate to the directory where the Python script is located and run the following command:

   ```bash
   python your_script_name.py
   ```

   This will launch the **Currency Converter** application.

---



## Using the Application

1. **Main Screen (Currency Converter):**
   - **Amount:** Enter the amount you wish to convert.
   - **From Currency:** Select the currency you are converting from (e.g., USD).
   - **To Currency:** Select the currency you want to convert to (e.g., EUR).
   - **Convert Button:** Press this button to perform the conversion. The result will be displayed below the input fields.

2. **Manage Currencies (CRUD Operations):**
   - **Add:** To add a new exchange rate, fill in the `Currency Code` and `Exchange Rate` and click the "Add" button.
   - **Update:** To update an existing exchange rate, select a currency from the list, change the rate, and click "Update".
   - **Delete:** To delete an exchange rate, select the currency and click the "Delete" button.

3. **Reports:**
   - View conversion history by clicking the "Report" button. This will show a list of all past currency conversions, including the amount, the converted amount, and the date of conversion.

4. **Back to Main Screen:**
   - You can navigate back to the main currency converter screen at any time by clicking the "Back to Converter" button in the CRUD or Report screens.

---

## Troubleshooting

- **Error in Database Connection:**  
  If the application cannot connect to the database, double-check the connection string (`db_conn_string`) and ensure SQL Server is running.

- **Missing Python Libraries:**  
  If any Python libraries are missing, you can reinstall them using `pip install <library-name>`.

- **Database Errors:**  
  If you see errors related to database queries (e.g., `pyodbc.Error`), ensure that the database is correctly set up and that the `ExchangeRates` table contains valid data.
  
- **Image Errors:**  
  If you see errors related to image_path, you can delete the part that uploade the image or download the image on your computer and then, replace thet image address base on its location on your computer.
---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/YasinShamsedini/CurrencyConverter/blob/main/LICENSE) file for details.

