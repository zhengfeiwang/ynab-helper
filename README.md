# YNAB Red Flag Transaction Tracker

An automation tool to track, sum, and report red-flagged transactions in YNAB.

## Features

- Automatic identification of red-flagged transactions
- Transaction filtering by date range and category
- Report generation in multiple formats (PDF, CSV, Excel)
- Automated scheduled reports
- Email notifications

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your YNAB API token:
   ```
   YNAB_API_TOKEN=your_api_token_here
   ```
4. Run the application:
   ```bash
   python src/main.py
   ```

## Configuration

The application can be configured through the `config.yaml` file. See `config.yaml.example` for available options.

## Usage

1. Set up your YNAB API token in the `.env` file
2. Configure your preferences in `config.yaml`
3. Run the application
4. Access the dashboard at `http://localhost:5000`

## Development

- Python 3.8+
- Uses YNAB API v1
- Built with pandas for data processing
- ReportLab for PDF generation
- Schedule for automated tasks 