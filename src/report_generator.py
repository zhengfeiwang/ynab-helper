import pandas as pd
from datetime import datetime
from typing import List, Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class ReportGenerator:
    def __init__(self, transactions: List[Dict]):
        self.transactions = transactions
        self.df = pd.DataFrame(transactions)
    
    def calculate_total(self) -> float:
        """Calculate the total amount of red-flagged transactions."""
        return self.df["amount"].sum() / 1000  # YNAB amounts are in milliunits
    
    def generate_csv(self, output_path: str) -> None:
        """Generate a CSV report."""
        self.df.to_csv(output_path, index=False)
    
    def generate_excel(self, output_path: str) -> None:
        """Generate an Excel report."""
        self.df.to_excel(output_path, index=False)
    
    def generate_pdf(self, output_path: str) -> None:
        """Generate a PDF report."""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        title = Paragraph("Red Flag Transaction Report", styles["Title"])
        elements.append(title)
        
        # Add date range
        date_range = Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
        elements.append(date_range)
        
        # Add total
        total = Paragraph(
            f"Total Amount: ${self.calculate_total():,.2f}",
            styles["Normal"]
        )
        elements.append(total)
        
        # Prepare data for table
        data = [["Date", "Payee", "Category", "Amount", "Notes"]]
        for _, row in self.df.iterrows():
            data.append([
                row["date"],
                row["payee_name"],
                row["category_name"],
                f"${row['amount']/1000:,.2f}",
                row.get("memo", "")
            ])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements) 