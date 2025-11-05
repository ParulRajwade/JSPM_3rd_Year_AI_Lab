📩 SMS Spam Detector

A simple Machine Learning project that detects whether an SMS message is Spam or Not Spam (Ham) using Python and Scikit-learn.

🚀 Features

Detects spam messages with high accuracy

Uses text preprocessing (stopword removal, stemming, tokenization)

Based on Bagging Classifier

Easy to run and modify

🧠 Technologies Used

Python

Scikit-learn

NLTK

Pandas

NumPy

Matplotlib

⚙️ How to Run
1. Clone this repository
git clone https://github.com/<your-username>/SMS_Spam_Detector.git
cd SMS_Spam_Detector

2. Install dependencies
pip install -r requirements.txt

3. Train the model
python train_model.py

4. Run the app

If it’s a Streamlit app:

streamlit run app.py


If it’s a normal Python script:

python app.py

📊 Example

Input:

Congratulations! You have won a free vacation. Click here to claim.

Output:

🛑 Spam Message

Input:

Hey, are we still meeting today?

Output:

✅ Not Spam

📈 Model Info

Algorithm: Bagging Classifier

Accuracy: ~98%

Dataset: SMS Spam Collection Dataset (UCI)

💡 Future Improvements

Add email spam detection

Deploy using Streamlit Cloud or Flask

Improve accuracy using deep learning models

👨‍💻 Author

Saurabh Dalal

⭐ If you like this project, consider giving it a star!