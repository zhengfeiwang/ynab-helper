import os
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
from ynab_client import YNABClient

class CNYDashboard:
    def __init__(self):
        self.client = YNABClient()
        self.console = Console()
        self.cny_budget_id = "639270bb-7e47-4a46-b622-8308ce02b3d8"  # CNY Budget ID
        
    def get_date_range(self):
        """Get custom date range from user."""
        while True:
            try:
                start_date_str = Prompt.ask("Enter start date (YYYY-MM-DD)")
                end_date_str = Prompt.ask("Enter end date (YYYY-MM-DD)")
                
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                
                if end_date < start_date:
                    rprint("[red]End date cannot be before start date[/red]")
                    continue
                    
                return start_date, end_date
            except ValueError:
                rprint("[red]Invalid date format. Please use YYYY-MM-DD[/red]")
    
    def get_account_selection(self):
        """Get account selection from user."""
        accounts = self.client.get_accounts()
        cny_accounts = [acc for acc in accounts if acc["on_budget"]]
        
        if not cny_accounts:
            rprint("[yellow]No CNY accounts found[/yellow]")
            return None
            
        # Create account selection table
        table = Table(title="Available CNY Accounts")
        table.add_column("Index", style="cyan")
        table.add_column("Account Name", style="green")
        table.add_column("Balance", style="yellow")
        
        for idx, account in enumerate(cny_accounts, 1):
            balance = float(account["balance"]) / 1000  # Convert to CNY
            table.add_row(
                str(idx),
                account["name"],
                f"¥{balance:,.2f}"
            )
        
        self.console.print(table)
        
        while True:
            try:
                selection = Prompt.ask(
                    "Select account number (or 'all' for all accounts)",
                    default="all"
                )
                
                if selection.lower() == "all":
                    return None
                    
                idx = int(selection) - 1
                if 0 <= idx < len(cny_accounts):
                    return cny_accounts[idx]["id"]
                else:
                    rprint("[red]Invalid account number[/red]")
            except ValueError:
                rprint("[red]Please enter a valid number or 'all'[/red]")
    
    def generate_dashboard(self):
        """Generate and display the dashboard."""
        self.console.print(Panel.fit(
            "[bold blue]CNY Budget Red Flag Dashboard[/bold blue]",
            border_style="blue"
        ))
        
        # Get date range
        start_date, end_date = self.get_date_range()
        
        # Get account selection
        account_id = self.get_account_selection()
        
        # Get transactions
        transactions = self.client.get_red_flag_transactions(
            start_date=start_date,
            end_date=end_date,
            account_id=account_id
        )
        
        if not transactions:
            self.console.print("[yellow]No red-flagged transactions found in the selected period[/yellow]")
            return
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(transactions)
        df["amount"] = df["amount"].astype(float) / 1000  # Convert to CNY
        df["date"] = pd.to_datetime(df["date"])
        
        # Calculate statistics
        total_amount = df["amount"].sum()
        avg_amount = df["amount"].mean()
        transaction_count = len(df)
        
        # Group by category
        category_stats = df.groupby("category_name")["amount"].agg(["sum", "count"]).reset_index()
        category_stats = category_stats.sort_values("sum", ascending=False)
        
        # Create dashboard
        self.console.print("\n[bold]Summary Statistics[/bold]")
        stats_table = Table(show_header=False, box=None)
        stats_table.add_row("Total Amount:", f"¥{total_amount:,.2f}")
        stats_table.add_row("Average Amount:", f"¥{avg_amount:,.2f}")
        stats_table.add_row("Number of Transactions:", str(transaction_count))
        self.console.print(stats_table)
        
        self.console.print("\n[bold]Category Breakdown[/bold]")
        category_table = Table()
        category_table.add_column("Category", style="cyan")
        category_table.add_column("Total Amount", style="yellow", justify="right")
        category_table.add_column("Count", style="green", justify="right")
        
        for _, row in category_stats.iterrows():
            category_table.add_row(
                row["category_name"],
                f"¥{row['sum']:,.2f}",
                str(row["count"])
            )
        
        self.console.print(category_table)
        
        self.console.print("\n[bold]Recent Transactions[/bold]")
        transaction_table = Table()
        transaction_table.add_column("Date", style="cyan")
        transaction_table.add_column("Payee", style="green")
        transaction_table.add_column("Category", style="yellow")
        transaction_table.add_column("Amount", style="red", justify="right")
        
        for _, row in df.sort_values("date", ascending=False).head(10).iterrows():
            transaction_table.add_row(
                row["date"].strftime("%Y-%m-%d"),
                row["payee_name"],
                row["category_name"],
                f"¥{row['amount']:,.2f}"
            )
        
        self.console.print(transaction_table)
        
        # Export option
        if Prompt.ask("\nWould you like to export this data?", choices=["y", "n"], default="n") == "y":
            export_format = Prompt.ask(
                "Choose export format",
                choices=["csv", "excel"],
                default="csv"
            )
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if export_format == "csv":
                filename = f"reports/cny_red_flags_{timestamp}.csv"
                df.to_csv(filename, index=False)
            else:
                filename = f"reports/cny_red_flags_{timestamp}.xlsx"
                df.to_excel(filename, index=False)
            
            self.console.print(f"[green]Data exported to {filename}[/green]")

if __name__ == "__main__":
    dashboard = CNYDashboard()
    dashboard.generate_dashboard() 