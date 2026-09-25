# 🇩🇪 German Credit Risk Dashboard & Analysis

An interactive Streamlit web dashboard for exploratory data analysis, historical insights, and machine learning model evaluation using the German Credit dataset.

## 🔗 Quick Links
* **Live Web Dashboard:** [View Streamlit App](https://german-credit-dashboard-5jqbswljq3vvy7e3ajiq4r.streamlit.app)
  
* **Google Colab Notebook:** [Open Google Colab Code](https://colab.research.google.com/drive/1GiT98uZgL8_uAqkqc36yffHUD38SXeV2?usp=sharing)

---
After Pulling the dataset from OpenML (because I didn't have it saved anywhere on my phone/ Laptop and pulling it straight from the cloud is just faster and cleaner anyway 😌), here's what I found — and what it all actually means.

## 🏦 Let Me Tell You guys a Story About Money and Trust

Picture this: a bank sits across the table from a stranger who wants to borrow money. The bank has one big question — "If I give you this money, will you pay me back?" That's it. That's the whole game. And for decades, banks answered that question with gut feeling, paperwork, and a bit of prayer.
Then, back in 1994, a professor named Hans Hofmann at the University of Hamburg said "enough of this guessing" — so he and his team gathered real records of 1,000 loan applicants in Germany: their age, how much they earned, whether they had a savings account, how long they'd lived at their current address, what they wanted the loan for, and — most importantly — whether they eventually paid the loan back or defaulted. They packaged this into what the data world now calls the German Credit Dataset, and it's been used ever since to train machines to answer that same question banks have always asked: good risk, or bad risk?
That's the dataset I picked up and ran through Google Colab. And honestly, by the time I was done, it told a story way bigger than just numbers in a spreadsheet.

🧹 First, I Had to Clean the House
Before any analysis is trustworthy, you have to check the data isn't lying to you. So I checked:
Missing values? Zero. Not one blank cell across all 1,000 rows and 21 columns.
Duplicate entries? None either.
Clean data, straight out of the box. That almost never happens in the real world, so this was a nice head start.

📊 What's Actually Inside
The dataset has 20 pieces of information about each person (things like checking_status, credit_history, duration of the loan, credit_amount, age, job, housing, purpose of the loan) plus one final answer: class — good or bad credit risk.
And here's the first surprising thing I noticed: out of 1,000 people, 700 were labeled "good" credit risks and only 300 were "bad." That imbalance matters a lot, and I'll come back to it — it quietly shapes everything the model does later.

🔗 What the Numbers Whispered to Me (Correlation & EDA)
When I ran the correlation heatmap, one relationship jumped out immediately: loan duration and loan amount move together (0.62 correlation) — basically, the bigger the loan, the longer people take to pay it back. Makes sense, honestly, even a 9-year-old saving up allowance for a bigger toy knows it takes longer to save for the expensive one.
The charts also showed something eye-opening about checking_status — people with "no checking account" were overwhelmingly labeled good risks, while people with a negative checking balance ("<0") were flagged bad far more often. Basically: how a person manages the small, everyday account tells you more about them than you'd expect.

🤖 Then Came the Machine Learning Verdict
So after running the regression analysis (I used Logistic Regression, since we're predicting one of two outcomes — good or bad, yes or no, like a light switch), here's exactly what I observed:
Accuracy: 70% — the model got the right answer 7 times out of 10.
AUC Score: 0.73 — meaning it's genuinely better than a coin flip at telling good risk from bad risk (0.5 = coin flip, 1.0 = perfect).
The confusion matrix told the real story though: out of the actual "bad" credit people in the test set, the model only correctly caught 23 out of 60 — that's just a 38% recall on bad credit. It was much better at spotting "good" credit people (117 out of 140 correct, 84% recall).
Translation: imagine a teacher trying to guess who forgot their homework. She's really good at spotting the kids who did their homework (she gets that right almost every time), but she's not so good at catching the ones who didn't — she misses more than half of them. That's exactly what's happening here.
And that's the single most important, practical finding in this whole project.
The strongest individual predictors, from the model's own coefficients, were:
checking_status (biggest positive push toward "good")
purpose of the loan
installment_commitment and credit_amount (bigger commitments and amounts pushed toward "bad")
duration of the loan (longer loans, more risk)

💡 So — What Should Companies Actually DO With This?
Here's where I bring it home, The practical Solutions:
Don't let the model make the final call alone. Because it misses more than half of actual bad-risk applicants, using it as the only gatekeeper is like hiring a security guard who lets in 6 out of 10 people who shouldn't be there. Use it as a first filter, then have a human underwriter double-check anyone the model flags as "borderline good."
Fix the imbalance in the training data. Since the model saw way more "good" examples (700) than "bad" (300) during training, it naturally leans toward guessing "good." Companies should feed it more balanced examples (a technique called SMOTE, or simply collecting more bad-risk cases) so it stops being so trigger-happy about approving people.
Watch the checking account and loan duration closely. These were the loudest signals in the whole dataset. A simple, practical move: flag applications with negative checking balances AND long loan durations for extra manual review — that combo is where the real risk hides.
Tier the decision, don't binary it. Instead of a flat "approve/reject," companies can use the model's probability score to create three lanes: Auto-approve (very high confidence good), Auto-review (uncertain — human eyes needed), Auto-decline (very high confidence bad). This respects what the model is actually good at, and protects against what it's bad at.
Keep retraining it. Credit behavior changes with the economy. A model trained on 1994 Germany shouldn't be treated as gospel for 2026 anywhere else — it needs fresh, local data periodically.

🎯 The Bottom Line
This little 1,000-row dataset, from over 30 years ago, still teaches a lesson every modern fintech company needs: a machine learning model isn't magic — it's a flashlight, not a judge. It shines light on where to look closer; it shouldn't be the one slamming the door shut. Companies that treat AI credit scoring as a decision support tool rather than a decision maker protect both their business and the people asking for a fair shot at a loan.


And so that's the Findings and the end of my Journey with this German credit Dataset 
thank youuu for walking it with me.
