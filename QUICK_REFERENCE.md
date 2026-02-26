# Quick Reference: Using Advanced Features

## 🔴 CRITICAL: API Key Security
Never expose API keys in code, README, or commits!
```bash
# Store keys in .env file only
GEMINI_API_KEY=xxx
OPENROUTER_API_KEY=xxx
GOLD_API_KEY=xxx
```

---

## 1️⃣ Spending Predictions

### Basic (Linear Regression)
```python
from app.ml_model import SpendingPredictor

predictor = SpendingPredictor()
result = predictor.predict_next_month(user_id=1, use_advanced_ml=False)

print(f"Total: ₹{result['total_predicted']}")
print(f"Model: {result['model_used']}")  # Shows 'Linear Regression'
```

### Advanced (LSTM + ARIMA)
```python
predictor = SpendingPredictor()
result = predictor.predict_next_month(user_id=1, use_advanced_ml=True)

print(f"Total: ₹{result['total_predicted']}")
print(f"Daily Average: ₹{result['daily_average']}")
print(f"Peak Days: {result['high_spending_days']}")
print(f"Model: {result['model_used']}")  # Shows 'Ensemble (LSTM + ARIMA)'
```

---

## 2️⃣ Financial Health Check

```python
from app.financial_modeling import FinancialHealthAnalyzer

metrics = FinancialHealthAnalyzer.calculate_financial_metrics(
    monthly_income=100000,
    monthly_expenses=60000,
    current_balance=500000
)

# Access metrics
print(f"Savings Rate: {metrics['savings_rate_percent']:.1f}%")
print(f"Emergency Fund: {metrics['emergency_fund_months']:.1f} months")
print(f"Health Score: {metrics['financial_health_score']['overall_score']}/100")
print(f"Rating: {metrics['financial_health_score']['rating']}")

# Get recommendations
for rec in metrics['recommendations']:
    print(f"• {rec}")
```

---

## 3️⃣ Risk Assessment

```python
from app.risk_analysis import RiskAnalyzer

risks = RiskAnalyzer.calculate_financial_risks(
    monthly_income=100000,
    monthly_expenses=60000,
    current_balance=500000,
    fixed_obligations=15000,  # EMIs, loans
    health_insurance_coverage=500000,
    life_insurance_coverage=1000000
)

print(f"Risk Score: {risks['overall_risk_score']}/100")
print(f"Risk Rating: {risks['risk_rating']}")

# Check alerts
for alert in risks['risk_alerts']:
    print(f"{alert['type']}: {alert['title']}")
    print(f"  → {alert['description']}")

# Action items
for strategy in risks['mitigation_strategies']:
    print(f"{strategy['priority']}: {strategy['action']}")
```

---

## 4️⃣ Portfolio Optimization

```python
from app.financial_modeling import PortfolioOptimizer

optimizer = PortfolioOptimizer()
allocation = optimizer.generate_allocation(
    monthly_surplus=20000,
    risk_profile='moderate',  # or 'conservative', 'aggressive'
    age=35,
    months_to_retirement=300  # 25 years
)

# Investment breakdown
for asset, details in allocation['allocation'].items():
    if details['monthly_amount'] > 0:
        print(f"{asset}:")
        print(f"  ₹{details['monthly_amount']:,.0f}/month ({details['allocation_percent']:.1f}%)")

print(f"\nExpected Annual Return: {allocation['expected_annual_return_percent']:.1f}%")
print(f"Projected Value at Retirement: ₹{allocation['projected_value_at_retirement']:,.0f}")
```

---

## 5️⃣ Retirement Planning

```python
from app.financial_modeling import FutureValueCalculator

# 20-year SIP projection
sip = FutureValueCalculator.calculate_sip_returns(
    monthly_investment=20000,
    annual_return=0.12,  # 12% expected
    years=20
)

print(f"Monthly Investment: ₹{sip['monthly_investment']:,.0f}")
print(f"Total Invested: ₹{sip['total_invested']:,.0f}")
print(f"Future Value: ₹{sip['future_value']:,.0f}")
print(f"Total Returns: ₹{sip['total_returns']:,.0f}")
print(f"ROI: {sip['return_on_investment_percent']:.1f}%")

# Retirement corpus
retirement = FutureValueCalculator.retirement_planner(
    current_age=35,
    retirement_age=60,
    annual_expenses=600000,
    inflation_rate=0.06
)

print(f"\nCorpus Needed (4% rule): ₹{retirement['total_corpus_needed_4pct_rule']:,.0f}")
print(f"Inflation-Adjusted Expense at 60: ₹{retirement['projected_annual_expense_at_retirement']:,.0f}")
```

---

## 6️⃣ All-in-One Comprehensive Analysis

```python
from app.ml_model import ComprehensiveFinancialAnalysis

analyzer = ComprehensiveFinancialAnalysis()
report = analyzer.generate_comprehensive_report(
    user_id=1,
    user_balance=500000,
    total_income=100000,
    total_expenses=60000,
    age=35
)

# Access all sections
print("=== FINANCIAL HEALTH ===")
health = report['sections']['financial_health']
print(f"Score: {health['financial_health_score']['overall_score']}/100")

print("\n=== RISK ASSESSMENT ===")
risk = report['sections']['risk_assessment']
print(f"Score: {risk['overall_risk_score']}/100")

print("\n=== PORTFOLIO ===")
portfolio = report['sections']['portfolio_recommendation']
print(f"Expected Return: {portfolio['expected_annual_return_percent']:.1f}%")

print("\n=== RETIREMENT ===")
retirement = report['sections']['retirement_plan']
print(f"Corpus Needed: ₹{retirement['total_corpus_needed_4pct_rule']:,.0f}")
```

---

## 7️⃣ Advanced Features

### Volatility Analysis
```python
from app.advanced_ml import GARCHVolatilityModel

volatility = GARCHVolatilityModel.calculate_volatility(
    returns_data=stock_returns,
    window=20
)

print(f"Current Volatility: {volatility['current_volatility']:.2%}")
print(f"Annualized: {volatility['annualized_volatility']:.2%}")
print(f"Value at Risk (95%): {volatility['value_at_risk_95']:.2%}")
print(f"Risk Level: {volatility['risk_level']}")
```

### Portfolio Stress Testing
```python
from app.risk_analysis import VaRCalculator

stress_results = VaRCalculator.stress_test_portfolio(
    current_balance=1000000,
    asset_allocation={
        'Equity (Large Cap)': 0.40,
        'Bonds': 0.30,
        'Gold': 0.20,
        'Cash': 0.10
    }
)

for scenario, result in stress_results['stress_test_results'].items():
    print(f"{scenario}:")
    print(f"  New Value: ₹{result['new_portfolio_value']:,.0f}")
    print(f"  Loss: ₹{result['loss_amount']:,.0f}")
```

### Sensitivity Analysis
```python
from app.risk_analysis import SensitivityAnalyzer

sensitivity = SensitivityAnalyzer.sensitivity_to_returns(
    initial_investment=500000,
    annual_contribution=120000,
    years=20,
    base_return_rate=0.10
)

for rate, outcome in sensitivity['sensitivity_analysis'].items():
    print(f"{rate}: ₹{outcome['future_value']:,.0f} (ROI: {outcome['roi_percent']:.1f}%)")
```

---

## ⚠️ Error Handling

```python
from app.advanced_ml import LSTMPredictor

lstm = LSTMPredictor()
result = lstm.predict(spending_data)

if 'error' in result:
    print(f"LSTM failed: {result['error']}")
    print("Falling back to ARIMA or Linear Regression")
else:
    print(f"LSTM Success: {result['total_predicted']}")
```

---

## 📋 Model Selection Decision Tree

```
Do you have spending data?
├─ NO → Wait for more data, use assumptions
└─ YES → How much data?
    ├─ < 10 points → Linear Regression (fast, simple)
    ├─ 10-20 points → ARIMA (statistical)
    └─ > 20 points → Ensemble (LSTM + ARIMA, most accurate)
```

---

## 🔧 Configuration

### Environment Variables (.env)
```env
# API Keys
GEMINI_API_KEY=your-key
OPENROUTER_API_KEY=your-key
GOLD_API_KEY=your-key

# ML Configuration (optional)
TENSORFLOW_CPP_MIN_LOG_LEVEL=2  # Reduce TensorFlow verbosity
```

### Feature Flags
```python
# Enable/disable advanced ML
USE_ADVANCED_ML = True
ENSEMBLE_ENABLED = True
RISK_ANALYSIS_ENABLED = True
```

---

## 📊 Common Outputs

### Spending Prediction
```python
{
    'total_predicted': 185000.50,
    'daily_average': 6166.68,
    'high_spending_days': [15, 8, 22],
    'model_used': 'Ensemble (LSTM + ARIMA)',
    'model_confidence': 'High'
}
```

### Health Metrics
```python
{
    'savings_rate_percent': 40.0,
    'emergency_fund_months': 8.33,
    'financial_health_score': {
        'overall_score': 87,
        'rating': 'Good ✅'
    },
    'monthly_surplus': 40000.0
}
```

### Risk Assessment
```python
{
    'overall_risk_score': 32,
    'risk_rating': 'Low Risk 🟢',
    'risk_alerts': [...],
    'mitigation_strategies': [...]
}
```

---

## 🐛 Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Check what's installed
from app.advanced_ml import HAS_TENSORFLOW, HAS_STATSMODELS
print(f"TensorFlow: {HAS_TENSORFLOW}")
print(f"Statsmodels: {HAS_STATSMODELS}")

# Get detailed error messages
try:
    result = lstm.predict(data)
except Exception as e:
    logger.exception("LSTM error:", exc_info=True)
```

---

**Pro Tip**: Always check for 'error' key in response dictionaries!

```python
result = predictor.predict_next_month(user_id=1)
if 'error' in result:
    # Handle error gracefully
    print(f"Prediction failed: {result['error']}")
else:
    # Use result
    print(f"Prediction: ₹{result['total_predicted']}")
```
