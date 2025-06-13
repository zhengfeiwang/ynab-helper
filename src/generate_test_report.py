from ynab_client import YNABClient
from report_generator import ReportGenerator
from datetime import datetime, timedelta

def generate_test_report():
    print("Generating test report...")
    
    try:
        # Initialize client
        client = YNABClient()
        
        # Get transactions from the last 30 days
        transactions = client.get_red_flag_transactions(
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        
        if not transactions:
            print("No red-flagged transactions found in the last 30 days.")
            return
        
        # Generate reports in all formats
        report = ReportGenerator(transactions)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate PDF
        pdf_path = f"reports/red_flag_report_{timestamp}.pdf"
        report.generate_pdf(pdf_path)
        print(f"✓ Generated PDF report: {pdf_path}")
        
        # Generate CSV
        csv_path = f"reports/red_flag_report_{timestamp}.csv"
        report.generate_csv(csv_path)
        print(f"✓ Generated CSV report: {csv_path}")
        
        # Generate Excel
        excel_path = f"reports/red_flag_report_{timestamp}.xlsx"
        report.generate_excel(excel_path)
        print(f"✓ Generated Excel report: {excel_path}")
        
        # Print summary
        print(f"\nTotal amount: ${report.calculate_total():,.2f}")
        print(f"Number of transactions: {len(transactions)}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if your YNAB API token is correct in the .env file")
        print("2. Make sure the 'reports' directory exists")
        print("3. Verify you have write permissions in the current directory")

if __name__ == "__main__":
    generate_test_report() 