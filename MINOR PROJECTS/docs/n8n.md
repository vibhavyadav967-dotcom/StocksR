# n8n Workflow Guide

Import the workflow file located in n8n/workflows/stock_analysis_workflow.json.

## Scheduling

The workflow is scheduled for every 1 hour by default. For testing, switch the interval to 5 minutes.

## Workflow Behavior

1. Trigger schedule runs
2. Load stock symbols
3. For each symbol, call the FastAPI analysis endpoint
4. Receive the analysis JSON
5. Save the result to PostgreSQL
6. Format a Telegram-ready message
7. Send Telegram notification
8. Send email report
9. Log workflow result

## Secret Handling

Do not place API keys directly inside workflow JSON. Use n8n credentials or environment variables.
