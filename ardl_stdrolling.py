import pandas as pd
import matplotlib.pyplot as plt
import os
import yfinance as yf
from bcb import sgs
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.ardl import ardl_select_order
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tsa.api import VAR
from sklearn.preprocessing import StandardScaler

# 1. Parameters
start_date = '2015-01-01'
end_date = '2025-01-01'
output_dir = "your_output_directory_here"  # Change this to the folder where you want to save your results
os.makedirs(output_dir, exist_ok=True)

# 2. Downloading trade data from BCB (Brazilian Central Bank)
print("🔍 Downloading BCB trade data...")
bcb_data = sgs.get({'exports': 1, 'imports': 4}, start=start_date, end=end_date)
bcb_data['trade_balance'] = bcb_data['exports'] - bcb_data['imports']
bcb_data = bcb_data.resample('ME').last().dropna()

# 3. Downloading BRL/USD exchange rate via Yahoo Finance
print("🔍 Downloading BRL/USD exchange rate...")
fx_raw = yf.download("BRL=X", start=start_date, end=end_date, interval="1d", progress=False)
fx_monthly = fx_raw[['Close']].resample("ME").last().dropna()
fx_monthly.columns = ['brlusd']

# 4. Merging and differencing
df_level = pd.concat([bcb_data['trade_balance'], fx_monthly['brlusd']], axis=1).dropna()
df_diff = df_level.diff().dropna()
df_diff.columns = ['delta_trade_balance', 'delta_brlusd']

# 5. Volatility regimes via Rolling Std
rolling_std = df_diff['delta_brlusd'].rolling(window=6).std()
threshold = rolling_std.median()
df_diff['regime'] = (rolling_std > threshold).astype(int)  # 1 = high volatility regime

# 6. ADF Stationarity Tests
def adf_test(series, name):
    result = adfuller(series.dropna(), autolag='AIC')
    print(f"ADF test for {name}: p-value = {result[1]:.4f}")

print("\n📉 ADF Tests:")
adf_test(df_diff['delta_trade_balance'], 'ΔTrade Balance')
adf_test(df_diff['delta_brlusd'], 'ΔBRL/USD')

# 7. General ARDL estimation
print("\n📈 Estimating general ARDL model...")
selected = ardl_select_order(endog=df_diff['delta_trade_balance'],
                             exog=df_diff[['delta_brlusd']],
                             maxlag=4, maxorder=2, ic='aic')
model = selected.model.fit()
print(model.summary())

# 8. General Diagnostics
print("\n📊 General Diagnostics:")
print("Ljung-Box p-value:", acorr_ljungbox(model.resid, lags=[12], return_df=True).iloc[0]['lb_pvalue'])
print("ARCH-LM p-value:", het_arch(model.resid)[1])
print("Durbin-Watson:", durbin_watson(model.resid))

# 9. VAR and Impulse Response Functions
print("\n📈 Estimating VAR...")
var_model = VAR(df_diff[['delta_trade_balance', 'delta_brlusd']])
var_fitted = var_model.fit(4)
irf = var_fitted.irf(10)
irf.plot(orth=False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IRFs_VAR.png"))
plt.close()

# 10. ARDL estimation by regime
for regime in [0, 1]:
    regime_df = df_diff[df_diff['regime'] == regime]
    print(f"\n📌 Estimating ARDL for Regime {regime} with {len(regime_df)} observations.")
    if len(regime_df) < 10:
        print("⚠️ Too few observations.")
        continue
    selected_model = ardl_select_order(endog=regime_df['delta_trade_balance'],
                                       exog=regime_df[['delta_brlusd']],
                                       maxlag=3, maxorder=2, ic='aic')
    model_fit = selected_model.model.fit()
    print(model_fit.summary())

    # Diagnostics for regime model
    print("Ljung-Box p-value:", acorr_ljungbox(model_fit.resid, lags=[12], return_df=True).iloc[0]['lb_pvalue'])
    print("ARCH-LM p-value:", het_arch(model_fit.resid)[1])
    print("Durbin-Watson:", durbin_watson(model_fit.resid))

    # Save summary
    with open(os.path.join(output_dir, f"summary_ardl_regime_{regime}.txt"), "w") as f:
        f.write(str(model_fit.summary()))

# 11. Plot BRL/USD colored by regime
plt.figure(figsize=(12, 5))
for regime in [0, 1]:
    sub = df_diff[df_diff['regime'] == regime]
    plt.plot(sub.index, sub['delta_brlusd'], label=f'Regime {regime}')
plt.title("ΔBRL/USD by Volatility Regime (via rolling std)")
plt.axhline(0, color='gray', linestyle='--')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "brlusd_by_regime.png"))
plt.close()

# 12. Save general ARDL summary
with open(os.path.join(output_dir, "summary_ardl_general.txt"), "w") as f:
    f.write(str(model.summary()))

print("✅ All results were successfully generated and saved.")
