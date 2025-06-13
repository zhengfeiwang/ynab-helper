# YNAB Red Flag Transaction Tracker - Tests

This directory contains all test scripts for the YNAB Red Flag Transaction Tracker.

## Test Scripts

- **`test_connection.py`**: Tests the YNAB API connection and basic functionality.
- **`test_accounts.py`**: Lists all accounts for the current budget.
- **`test_accounts_cny.py`**: Lists all accounts for the CNY budget (using explicit budget ID).
- **`test_red_flags.py`**: Lists red-flagged transactions for different date ranges.
- **`list_red_flagged_cny.py`**: Lists all red-flagged transactions for the CNY budget over the last year.
- **`verify_token.py`**: Verifies the YNAB API token and lists available budgets.

## Running Tests

Run any test script using:
```bash
python tests/<script_name>.py
```

Example:
```bash
python tests/test_connection.py
```

## Notes

- Ensure your `.env` file is set up with `YNAB_API_TOKEN` and `YNAB_BUDGET_ID`.
- These tests are designed to verify the functionality of the YNAB client and report generation. 