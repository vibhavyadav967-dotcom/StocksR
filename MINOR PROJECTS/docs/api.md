# API Documentation

## Health

GET /health

Returns application health status.

## Stock list

GET /api/stocks

Returns available symbols.

## Stock summary

GET /api/stocks/{symbol}

Returns the latest trading information for a symbol.

## Analysis

GET /api/stocks/{symbol}/analysis

This is the main endpoint. It performs:
- market-data retrieval
- technical indicator calculation
- news collection
- sentiment evaluation
- final recommendation scoring

It returns the complete analysis result in JSON.
