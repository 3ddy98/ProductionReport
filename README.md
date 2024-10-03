---
# Production Report Generator

This Python project is designed to generate daily and monthly production reports for different production lines in a factory setting. It processes production data such as products worked, time spent, and quantities produced, and outputs insightful visual and textual reports, including production rate per hour, total output, and other performance metrics. The results can be saved in various formats, such as images and text files.

## Features

- **Daily Reports**: Generate detailed reports on the performance of each production line on a daily basis.
- **Monthly Reports**: Aggregate and summarize the performance of multiple production lines over a month.
- **Data Visualization**: Plots showing production trends (e.g., wetpacks produced per hour, total output) and other statistics.
- **CSV/Excel Input**: Processes production data from CSV or Excel files for flexible and reusable data.
- **Performance Metrics**: Calculates metrics like wetpacks per hour (WPH), workers per hour, and average production rates.
- **Data Logging**: Saves output reports as text files and charts as PNG images for record-keeping.

## How it Works

### Classes:

1. **Item Class**:
   - Represents an individual production item with attributes like SKU, Work Order, Duration, Quantity, and Time Start/End.
   - Each item can be displayed with `print_product_data()`.

2. **Production_Line Class**:
   - Represents a production line with attributes like the number of wetpacks produced, employees, and the products worked on.
   - Each line can display its products and workers with `print_line_data()`.

### Report Generation Functions:

- **generate_line_report**:
   - Generates detailed daily reports for a specific production line, including metrics like total boxes produced, WPH (Wetpacks Per Hour), and cumulative production.
   - Produces a graphical output with production trends and detailed statistics.

- **generate_line_report_monthly**:
   - Aggregates and summarizes the performance of multiple production lines over the course of a month.
   - Plots average WPH for different products worked on each line.

- **calculate_line_stats**:
   - Computes various statistics (average WPH, maximum WPH, etc.) for individual products within a production line.
   - Returns summarized data for easy comparison across products.

### Input and Output:

- **Input**:
   - Data can be loaded from Excel files located in the `reports/` directory. The user is prompted to select daily or monthly reporting and to provide file names.
   - The data is parsed and processed into a pandas DataFrame for analysis.
   - The data must have the following columns:
![image](https://github.com/user-attachments/assets/f1782e37-0c8d-448e-a4fb-5ec0425225b9)


- **Output**:
   - The results are output as:
     - Plots saved as PNG images, displaying production rates and cumulative production over time.
     - Text reports that summarize daily/monthly statistics for later reference.

## Usage

1. Clone the repository.
2. Install the required libraries:
   ```bash
   pip install pandas matplotlib numpy openpyxl
   ```
3. Prepare your production data in CSV/Excel format.
4. Run the script:
   ```bash
   python production_report.py
   ```
5. Choose whether you want to generate a daily or monthly report:
   - **Option 1**: Monthly report
   - **Option 2**: Daily report (you will be asked to provide the working hours for accuracy).
6. The report will be generated and saved as images and text files.

## Example

### Daily Report

A typical daily report will include:
- The total number of wetpacks produced over time.
- Wetpacks per hour (WPH) for each product.
- Production targets and comparison to actual production.

### Monthly Report

The monthly report will compare average WPH across all products and production lines.

## Directory Structure

```
├── DailyReport/          # Contains saved daily report images
├── Report.txt            # Contains text summary of the reports
├── production_report.py   # Main Python script for generating reports
├── reports/              # Directory where your input Excel files are located
└── README.md             # This readme file
```

## Requirements

- Python 3.x
- pandas
- matplotlib
- numpy
- openpyxl

---

This explanation provides a comprehensive overview of the project for a potential user or collaborator on GitHub.
