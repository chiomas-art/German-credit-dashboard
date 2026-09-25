# 🇩🇪 German Credit Risk Dashboard & Analysis

An interactive Streamlit web dashboard for exploratory data analysis, historical insights, and machine learning model evaluation using the German Credit dataset.

## 🔗 Quick Links
* **Live Web Dashboard:** [View Streamlit App](https://german-credit-dashboard-5jqbswljq3vvy7e3ajiq4r.streamlit.app)
  
* **Google Colab Notebook:** [Open Google Colab Code](https://colab.research.google.com/drive/1GiT98uZgL8_uAqkqc36yffHUD38SXeV2?usp=sharing)

---
After Pulling the dataset from OpenML (because I didn't have it saved anywhere on my phone/ Laptop and pulling it straight from the cloud is just faster and cleaner anyway 😌), here's what I found — and what it all actually means.

## 🏦 Let Me Tell You guys a Story About Money and Trust
Picture this: a bank sits across the table from a stranger who wants to borrow money[span_0](start_span)[span_0](end_span). The bank has one big question — *"If I give you this money, will you pay me back?"* That's it[span_1](start_span)[span_1](end_span). That's the whole game[span_2](start_span)[span_2](end_span). And for decades, banks answered that question with gut feeling, paperwork, and a bit of prayer[span_3](start_span)[span_3](end_span).

Then, back in 1994, a professor named Hans Hofmann at the University of Hamburg said *"enough of this guessing"* — so he and his team gathered real records of 1,000 loan applicants in Germany: their age, how much they earned, whether they had a savings account, how long they'd lived at their current address, what they wanted the loan for, and — most importantly — whether they eventually paid the loan back or defaulted[span_4](start_span)[span_4](end_span). They packaged this into what the data world now calls the German Credit Dataset, and it's been used ever since to train machines to answer that same question banks have always asked: good risk, or bad risk[span_5](start_span)[span_5](end_span)?

That's the dataset I pulled straight from OpenML into Google Colab to run my analysis[span_6](start_span)[span_6](end_span). And honestly, by the time I was done, it told a story way bigger than just numbers in a spreadsheet[span_7](start_span)[span_7](end_span).

---

## 🧹 First, I Had to Clean the House
Before any analysis is trustworthy, you have to check the data isn't lying to you[span_8](start_span)[span_8](end_span). So I checked:
* **Missing values:** Zero. Not one blank cell across all 1,000 rows and 21 columns[span_9](start_span)[span_9](end_span).
* **Duplicate entries:** None either[span_10](start_span)[span_10](end_span).
* Clean data, straight out of the box — a rare head start in the real world[span_11](start_span)[span_11](end_span).

---

## 📊 What's Actually Inside
The dataset has 20 pieces of information about each person (`checking_status`, `credit_history`, duration of the loan, `credit_amount`, age, job, housing, purpose of the loan) plus one final answer: `class` — good or bad credit risk[span_12](start_span)[span_12](end_span).

* Out of 1,000 people, **700 were labeled "good" credit risks** and only **300 were "bad."**[span_13](start_span)[span_13](end_span)
* This class imbalance matters immensely, as it quietly shapes everything the model learns and predicts later[span_14](start_span)[span_14](end_span).

---

## 🔗 What the Numbers Whispered to Me (Correlation & EDA)
When I ran the correlation heatmap, one relationship jumped out immediately: **loan duration and loan amount move together ($0.62$ correlation)** — basically, the bigger the loan, the longer people take to pay it back[span_15](start_span)[span_15](end_span). 

The charts also revealed something eye-opening about `checking_status`:
* People with **"no checking account"** were overwhelmingly labeled good risks[span_16](start_span)[span_16](end_span).
* People with a negative checking balance (`<0`) were flagged as bad risks far more often[span_17](start_span)[span_17](end_span). 
* *Insight:* How a person manages their small, everyday account tells you much more about them than you might expect[span_18](start_span)[span_18](end_span).

---

## 🤖 The Machine Learning Verdict
Using Logistic Regression (since we're predicting one of two outcomes — good or bad, like a light switch), here's what the model achieved[span_19](start_span)[span_19](end_span):
* **Accuracy:** 70% — the model got the right answer 7 times out of 10[span_20](start_span)[span_20](end_span).
* **AUC Score:** 0.73 — proving it is genuinely better than a coin flip at separating good risk from bad risk ($0.5 = \text{coin flip}$, $1.0 = \text{perfect}$)[span_21](start_span)[span_21](end_span).

### The Confusion Matrix Real Story:
Out of the actual "bad" credit people in the test set, the model only correctly caught **23 out of 60** — that's just a **38% recall on bad credit**[span_22](start_span)[span_22](end_span). However, it was much better at spotting "good" credit people (**117 out of 140 correct, 84% recall**)[span_23](start_span)[span_23](end_span).

> **Analogy:** Imagine a teacher trying to guess who forgot their homework. She's great at spotting the kids who did their homework, but she misses more than half of the ones who didn't. That's exactly what's happening here[span_24](start_span)[span_24](end_span).

### Strongest Individual Predictors:
1. `checking_status` (biggest positive push toward "good")[span_25](start_span)[span_25](end_span)
2. Purpose of the loan[span_26](start_span)[span_26](end_span)
3. `installment_commitment` and `credit_amount` (bigger commitments and amounts pushed toward "bad")[span_27](start_span)[span_27](end_span)
4. Duration of the loan (longer loans equal more risk)[span_28](start_span)[span_28](end_span)

---

## 💡 What Should Companies Actually DO With This?
* **Don't let the model make the final call alone:** Because it misses more than half of actual bad-risk applicants, use it as a first filter, then have a human underwriter double-check borderline cases[span_29](start_span)[span_29](end_span).
* **Fix training data imbalance:** Use techniques like SMOTE or collect more bad-risk samples so the model stops being overly trigger-happy about approving loans[span_30](start_span)[span_30](end_span).
* **Monitor checking accounts & duration:** Flag applications featuring negative checking balances combined with long loan durations for extra manual review[span_31](start_span)[span_31](end_span).
* **Tier the decision process:** Instead of a strict binary approve/reject, use probability scores to create three lanes: Auto-approve, Auto-review (human eyes needed), and Auto-decline[span_32](start_span)[span_32](end_span).
* **Keep retraining:** Credit behavior shifts with the economy; a model trained on 1994 data requires fresh, periodic updates[span_33](start_span)[span_33](end_span).

---

## 🎯 The Bottom Line
This 1,000-row dataset from over 30 years ago still teaches a lesson every modern fintech company needs: **a machine learning model isn't magic — it's a flashlight, not a judge[span_34](start_span)[span_34](end_span).** It shines light on where to look closer; it shouldn't be the one slamming the door shut[span_35](start_span)[span_35](end_span). Companies that treat AI credit scoring as a decision-support tool rather than a decision-maker protect both their business and people asking for a fair shot[span_36](start_span)[span_36](end_span).
