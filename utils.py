import re
import csv
from PySide6.QtWidgets import QMessageBox, QTableWidget

def validate_email(email):
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number: digits only, 10-15 characters."""
    return phone.isdigit() and 10 <= len(phone) <= 15

def show_message(title, text, icon=QMessageBox.Information):
    """Display a message box with given title and text."""
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec()

def export_table_to_csv(table: QTableWidget, filepath: str):
    """Export QTableWidget content to CSV file."""
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
        writer.writerow(headers)
        # Write data rows
        for row in range(table.rowCount()):
            row_data = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                row_data.append(item.text() if item else '')
            writer.writerow(row_data)