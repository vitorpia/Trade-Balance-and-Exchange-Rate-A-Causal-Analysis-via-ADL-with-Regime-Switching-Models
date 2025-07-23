📊 Exchange Rate Volatility and the Trade Balance: Evidence from Brazil Using ARDL and Regime-Switching Models
This repository investigates how exchange rate depreciation impacts Brazil's trade balance, and how exchange rate volatility modifies this relationship. We test the hypothesis of the J-Curve using ARDL and VAR models, and then explore nonlinear behavior via volatility-based regimes using rolling standard deviation.


The classic J-Curve hypothesis suggests that currency depreciation initially worsens the trade balance before improving it, due to delayed contract adjustments and price rigidities.

However, in emerging markets like Brazil, this mechanism may break down under high exchange rate volatility. In such cases, depreciation might amplify uncertainty and reduce trade flows instead of improving them.

This study seeks to answer:

Does BRL depreciation improve Brazil’s trade balance?

How does volatility alter this effect?

Are there nonlinear regime-dependent dynamics?

2. 🧠 Methodology
🔹 ARDL: Autoregressive Distributed Lag
Captures short- and long-term relationships:

Equation:

Yₜ = α + ∑βᵢYₜ₋ᵢ + ∑δⱼXₜ₋ⱼ + εₜ

Where:

Yₜ = trade balance

Xₜ = BRL/USD exchange rate

🔹 VAR with IRFs (Impulse Response Functions)
Estimates the trajectory of the trade balance after a shock in the exchange rate, verifying the J-Curve behavior.

🔹 Regime-Switching via Rolling Std
Instead of using a Markov Switching model, we define regimes based on rolling standard deviation of Δ(BRL/USD). This allows us to detect periods of high vs. low volatility.

Rolling volatility:

σₜ = √(1/n ∑(rₜ₋ᵢ - r̄)²)

Threshold: regime = 1 if volatility > rolling average; else regime = 0.

Each regime is analyzed with a separate ARDL model.

3. 📌 Results
🔹 Step 1: ARDL on Full Sample
Variable	Coef.	Std. Err.	z-value	p-value
Constant	–0.991	0.804	–1.23	0.223
Δ(BRL/USD)	–24.41	4.378	–5.57	0.000

Model: ARDL(0, 0)

Observations: 56

Durbin-Watson: 2.08

✅ Strong evidence of a J-Curve: depreciation initially worsens the trade balance, but IRFs indicate subsequent improvement.

🔹 Step 2: ARDL by Volatility Regime
📉 Regime 0 – Low Volatility (31 obs.)
ARDL(3, 2)

Short-run effect: Δ(BRL/USD) = –23.91 (p = 0.004)

The J-Curve dynamic holds — initial drop, then recovery.

📉 Regime 1 – High Volatility (25 obs.)
ARDL(3, 0)

Short-run effect: Δ(BRL/USD) = –36.44 (p = 0.001)

No significant long-run correction.

📌 Conclusion: Under high volatility, the depreciation has a stronger negative effect and the J-Curve fails — possibly due to trade uncertainty and risk aversion.

4. 📚 References
Bahmani-Oskooee, M. & Ratha, A. (2004). The J-Curve: A Literature Review. Applied Economics.

Clarida, R. & Davis, J. (2001). Exchange Rate Volatility in Emerging Markets. NBER Working Paper.

Hsing, Y. (2009). Test of the J-Curve for Brazil. International Journal of Applied Economics.

Pesaran, M. H., Shin, Y., & Smith, R. (2001). Bounds Testing for Level Relationships. Journal of Applied Econometrics.

Hamilton, J. D. (1989). New Approach to Economic Time Series with Regime Changes. Econometrica.

👨‍💻 Author
Developed by Vitor Piagetti as part of a broader study on the effects of exchange rate volatility on macroeconomic outcomes in emerging economies.
