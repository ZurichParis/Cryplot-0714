# Bitcoin Price Predictor 📈

A simple Bitcoin price prediction app built with Python and Dash, using linear regression to forecast future BTC prices.

## 📊 Features

- historical Bitcoin data
- Future price predictor for fun
- Upper and lower bond for price
- If current price is close to upper or lower bond, show it on top banner

## ⚠️ Important Disclaimer

**This predictor is for educational and entertainment purposes only. Do NOT use this for actual financial decisions or investment advice. Cryptocurrency markets are highly volatile and unpredictable. Past performance does not guarantee future results.**

## 🔧 Technology Behind the App

This app uses **simple linear regression** to predict Bitcoin prices based on historical data:

- **X-axis**: Day number (1st day, 2nd day, 3rd day, etc.)
- **Y-axis**: Bitcoin prices (in USD) or log₂ transformed prices
- **Model**: Linear regression to find the best-fit line through historical data points

### Why Use Log₂ Transformation?

In original price data, recent prices change looks more obvious than early period data. It is quite misleading. Using log₂ (logarithm base 2) transformation will allow us easily compare early period's price data's change, or growth rate,  with recent data.:

 **Meaningful Interpretation**: Each unit increase in log₂ price represents a doubling of the original price. For example:
   - If log₂(price) increases by 1, the actual price doubled
   - If log₂(price) increases by 2, the actual price quadrupled

## 🚀 Setup Instructions

### Option 1: Using Docker (Recommended)

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd cryplot
```

2. **Build the Docker image**:
```bash
docker build -t cryplot .
```

3. **Run the container**:
```bash
docker run -p 8050:8050 cryplot
```

4. **Access the app**:
Open your browser and navigate to `http://localhost:8050`

### Option 2: Using pip and Virtual Environment

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd cryplot
```

2. **Create a virtual environment**:
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Run the application**:
```bash
python app.py
```

6. **Access the app**:
Open your browser and navigate to `http://localhost:8050`

7. **Deactivate virtual environment** (when done):
```bash
deactivate
```

## 📋 Requirements

Make sure your `requirements.txt` includes:
```
dash==2.16.1
yfinance==0.2.65
pandas==2.2.1
plotly==5.19.0
numpy==1.26.4
scikit-learn==1.5.1
```

## 🔧 Troubleshooting

### App Not Loading
- Check that the app is running on `http://localhost:8050`
- Look at the terminal output for any error messages
- Make sure no firewall is blocking the connection


## 🤝 Contributing

This is an educational project. Feel free to fork and experiment, but remember: **never use this for actual trading decisions!**

## 📄 License

This project is for educational purposes only. Use at your own risk.

---

**Remember: This is a toy model for learning purposes. Real financial markets are complex and cannot be predicted with simple linear regression. Always consult with qualified financial advisors for investment decisions.**