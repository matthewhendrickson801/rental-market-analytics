# StateofJax Affordable Housing Dashboard

Interactive dashboard for exploring affordable housing opportunities in Duval County, Florida.

## Features

- **Summary Statistics**: Total ZIPs, average rents, affordable count
- **Interactive Filters**: 
  - Filter by affordability category
  - Set minimum savings threshold
- **Visualizations**:
  - Bar chart: Top 15 affordable ZIPs
  - Pie chart: Affordability distribution
- **Data Table**: Detailed ZIP-level information (top 20)

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install dash plotly pandas
```

## Running the Dashboard

From the `d4_modeling` directory:

```bash
python3 dashboard/duval_dashboard.py
```

Or from the `dashboard` directory:

```bash
python3 duval_dashboard.py
```

The dashboard will start on: **http://127.0.0.1:8050**

Open this URL in your web browser.

## Usage

1. **View Summary**: Top section shows key metrics
2. **Filter Data**: 
   - Select affordability category from dropdown
   - Adjust minimum savings slider
3. **Explore Charts**:
   - Hover over bars to see details
   - Click pie chart legend to filter
4. **Review Table**: Scroll through top 20 ZIPs matching filters

## Affordability Categories

- **Highly Affordable** (Green): >$100/month below market
- **Affordable** (Light Green): $50-$100 below market
- **Market Rate** (Yellow): ±$50 of market
- **Overpriced** (Orange): $50-$100 above market
- **Highly Overpriced** (Red): >$100 above market

## Data Source

Dashboard uses predictions from the city-normalized XGBoost model:
- File: `d4_modeling/data/predictions_city_normalized.csv`
- Model: R² = 0.8615 (validation)
- ZIPs: 30 Duval County ZIPs in dataset

## Stopping the Dashboard

Press `Ctrl+C` in the terminal to stop the server.

## Troubleshooting

**Port already in use:**
```bash
# Change port in duval_dashboard.py line 234:
app.run_server(debug=True, port=8051)  # Use different port
```

**Module not found:**
```bash
# Make sure you're in the correct directory
cd d4_modeling
python3 dashboard/duval_dashboard.py
```

**Data file not found:**
```bash
# Verify predictions file exists:
ls data/predictions_city_normalized.csv
```

## Future Enhancements

- Map visualization with ZIP boundaries
- Export filtered results to CSV
- Comparison tool (select 2 ZIPs side-by-side)
- Historical trend analysis
- Neighborhood clustering
