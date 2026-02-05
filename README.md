# Northwind Traders Dashboard

An interactive dashboard developed with **Streamlit** and **Python** for analyzing data from the Northwind database.

## 📋 Description

This project provides a modern web application that connects to a **SQL Server** database (Northwind) and presents visual analyses and statistics about:

- **Products**: Number of products, categories, suppliers, and units in stock
- **Orders**: Number of orders, customers, employees, cities, and countries
- **Revenue**: Revenue analysis and sales details
- **Trends**: Charts and data visualizations over time

## 🛠️ Technologies Used

- **Streamlit** - Framework for creating interactive web applications
- **Python 3.x** - Programming language
- **Pandas** - Data manipulation and analysis
- **SQLAlchemy** - ORM and SQL toolkit
- **Plotly Express** - Interactive visualizations
- **PyODBC** - SQL Server connectivity
- **NumPy** - Numerical computing
- **Matplotlib** - Complementary visualizations

## 📦 Installation

### Prerequisites

- Python 3.7+
- SQL Server with Northwind database configured
- Pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/python-streamlit.git
   cd python-streamlit
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   
   On Windows (PowerShell):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   On Windows (CMD):
   ```cmd
   .venv\Scripts\activate.bat
   ```
   
   On Linux/macOS:
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

5. **Configure the database connection**
   
   Edit the `app.py` file and update the SQL Server credentials:
   ```python
   connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=your-server;DATABASE=Northwind;UID=your-user;PWD=your-password"
   ```

## 🚀 Running the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
python-streamlit/
├── app.py                 # Main application with the dashboard
├── northwind.ipynb       # Jupyter Notebook with exploratory analyses
├── requirement.txt       # Project dependencies
└── README.md            # This file
```

## 📊 Features

### Main Dashboard (`app.py`)

- **Key Indicators**: Cards showing key statistics from the database
- **Dynamic Charts**: Interactive visualizations with Plotly
- **Period Analysis**: Monthly and annual revenue analysis
- **Top Categories**: Ranking of categories by product quantity
- **Geographic Distribution**: Analysis of orders by country and city

### Exploratory Notebook (`northwind.ipynb`)

Contains additional analyses and data exploration with Jupyter Notebook, including:
- Data loading and cleaning
- Statistical analyses
- Exploratory visualizations

## 🔧 Database Configuration

This project uses the **Northwind** database from SQL Server. Make sure you have:

1. SQL Server installed and running
2. Northwind database restored
3. User and password configured correctly

## 📝 Environment Variables (Optional)

For better security, you can use environment variables instead of hardcoding credentials:

```python
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("DATABASE_URL")
```

## 🐛 Troubleshooting

### Error: "ODBC Driver 17 for SQL Server not found"
- Install the Microsoft ODBC Driver 17 for SQL Server

### Database connection error
- Verify that SQL Server is running
- Confirm access credentials
- Test the connection with SQL Server Management Studio

### Streamlit won't start
- Verify that all dependencies are installed
- Try reinstalling: `pip install --upgrade streamlit`

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Plotly Documentation](https://plotly.com/python/)
- [Northwind Database](https://github.com/Microsoft/sql-server-samples)

## 📄 License

This project is provided as is for educational and demonstration purposes.

## ✉️ Contact

For questions or suggestions, open an issue in the repository.

---

**Developed with ❤️ using Streamlit**
