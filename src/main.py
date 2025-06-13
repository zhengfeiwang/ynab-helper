import os
import schedule
import time
from datetime import datetime, timedelta
from typing import Optional
from ynab_client import YNABClient
from report_generator import ReportGenerator

class YNABRedFlagTracker:
    def __init__(self):
        self.ynab_client = YNABClient()
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category_id: Optional[str] = None,
        account_id: Optional[str] = None,
        output_format: str = "pdf"
    ) -> None:
        """
        Generate a report of red-flagged transactions.
        
        Args:
            start_date: Start date for filtering transactions
            end_date: End date for filtering transactions
            category_id: Optional category ID to filter by
            account_id: Optional account ID to filter by
            output_format: Output format (pdf, csv, or excel)
        """
        # Get transactions
        transactions = self.ynab_client.get_red_flag_transactions(
            start_date=start_date,
            end_date=end_date,
            category_id=category_id,
            account_id=account_id
        )
        
        if not transactions:
            print("No red-flagged transactions found for the specified criteria.")
            return
        
        # Generate report
        report = ReportGenerator(transactions)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format.lower() == "pdf":
            output_path = os.path.join(self.reports_dir, f"red_flag_report_{timestamp}.pdf")
            report.generate_pdf(output_path)
        elif output_format.lower() == "csv":
            output_path = os.path.join(self.reports_dir, f"red_flag_report_{timestamp}.csv")
            report.generate_csv(output_path)
        elif output_format.lower() == "excel":
            output_path = os.path.join(self.reports_dir, f"red_flag_report_{timestamp}.xlsx")
            report.generate_excel(output_path)
        else:
            raise ValueError("Unsupported output format")
        
        print(f"Report generated successfully: {output_path}")
        print(f"Total amount: ${report.calculate_total():,.2f}")
    
    def schedule_daily_report(self, time_str: str = "18:00") -> None:
        """Schedule a daily report generation."""
        schedule.every().day.at(time_str).do(
            self.generate_report,
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now()
        )
    
    def schedule_weekly_report(self, day: str = "monday", time_str: str = "18:00") -> None:
        """Schedule a weekly report generation."""
        schedule.every().monday.at(time_str).do(
            self.generate_report,
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now()
        )
    
    def schedule_monthly_report(self, day: int = 1, time_str: str = "18:00") -> None:
        """Schedule a monthly report generation."""
        def monthly_job():
            now = datetime.now()
            if now.day == day:
                self.generate_report(
                    start_date=datetime(now.year, now.month, 1),
                    end_date=now
                )
        
        schedule.every().day.at(time_str).do(monthly_job)
    
    def run_scheduler(self) -> None:
        """Run the scheduler loop."""
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    tracker = YNABRedFlagTracker()
    
    # Example: Generate a report for the last 30 days
    tracker.generate_report(
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        output_format="pdf"
    )
    
    # Example: Schedule daily reports at 6 PM
    tracker.schedule_daily_report("18:00")
    
    # Run the scheduler
    tracker.run_scheduler()

if __name__ == "__main__":
    main() 