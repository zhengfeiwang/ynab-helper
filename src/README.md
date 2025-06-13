# YNAB Red Flag Transaction Tracker

## Project Structure

- **`src/`**: Contains all source code
  - **`ynab_client.py`**: YNAB API client for fetching transactions, categories, and accounts.
  - **`report_generator.py`**: Generates reports in PDF, CSV, and Excel formats.
  - **`web_dashboard.py`**: Flask web app for interactive dashboard and API endpoints.

- **`tests/`**: Contains all test scripts
  - **`test_connection.py`**: Script to test YNAB API connection and basic functionality.
  - **`test_accounts.py`**: Lists all accounts for the current budget.
  - **`test_accounts_cny.py`**: Lists all accounts for the CNY budget (using explicit budget ID).
  - **`test_red_flags.py`**: Lists red-flagged transactions for different date ranges.
  - **`list_red_flagged_cny.py`**: Lists all red-flagged transactions for the CNY budget over the last year.
  - **`verify_token.py`**: Verifies the YNAB API token and lists available budgets.

## Setup Instructions

1. **Environment Setup**  
   Create a `.env` file in the project root with the following variables:
   ```
   YNAB_API_TOKEN=your_ynab_api_token_here
   YNAB_BUDGET_ID=your_budget_id_here
   ```

2. **Install Dependencies**  
   Run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Web Dashboard**  
   Start the Flask app:
   ```bash
   python src/web_dashboard.py
   ```
   Open your browser and go to `http://localhost:5000`.

4. **Test Scripts**  
   - Test YNAB connection: `python tests/test_connection.py`
   - List accounts: `python tests/test_accounts.py`
   - List CNY accounts: `python tests/test_accounts_cny.py`
   - List red-flagged transactions: `python tests/test_red_flags.py`
   - List CNY red-flagged transactions: `python tests/list_red_flagged_cny.py`
   - Verify token: `python tests/verify_token.py`

## Features

- **YNAB Integration**: Fetches transactions, categories, and accounts.
- **Red Flag Filtering**: Filters transactions by red flag status, date range, category, and account.
- **Reporting**: Generates reports in PDF, CSV, and Excel formats.
- **Web Dashboard**: Interactive dashboard with charts and transaction details.
- **API Endpoints**: Check total amount of red-flagged transactions via `/api/red-flag-amount`.

## Future Enhancements

- Budget selector in the dashboard.
- Email notifications for new red-flagged transactions.
- Custom report templates.
- Mobile app. 