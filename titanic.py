# -*- coding: utf-8 -*-
"""titanic.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CKYg4OSfPGxxkilLtRGPsHeRCmktzOsa
"""

import pandas as pd

df = pd.read_csv("/content/train.csv")

df

df.columns

#pip install pandas-profiling

import pandas as pd
#from ydata_profiling import ProfileReport

#x=ProfileReport(df)

#x

df.columns

df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'],inplace=True)

df.columns

df.info()

df.describe()

df.head()

import os

new_directory = "main_dataset"

if not os.path.exists(new_directory):
  os.makedirs(new_directory)
  print(f"Directory is created at {new_directory}")
else:
  print(f"Directory already exists at {new_directory}")

df.isnull()

df.isnull().sum()

len(df)

df1 = df.dropna()

len(df1)

df1.isnull().sum()

df1.head()

df1["Sex"] = df1["Sex"].map({"male":0,"female":1})

df1["Embarked"] = df1["Embarked"].map({"C":1,"Q":2,"S":3})

df1

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

df1[["Age","Fare"]] = scaler.fit_transform(df1[["Age","Fare"]])

df1

file_path = os.path.join("main_dataset","main_dataset.csv")

df1.to_csv(file_path,index=False)

mdf = pd.read_csv("/content/main_dataset/main_dataset.csv")

mdf

from sklearn.model_selection import train_test_split

X = mdf.drop(columns=["Survived"])

y = mdf[["Survived"]]

len(X),len(y)



from sklearn.linear_model import LogisticRegression

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model = LogisticRegression()

model.fit(X_train,y_train)

y_predict = model.predict(X_test)

accuracy = model.score(X_test,y_test)

accuracy

from sklearn.ensemble import RandomForestClassifier

model1 = RandomForestClassifier()

model1.fit(X_train,y_train)

yyy_predict = model1.predict(X_test)

accuracy = model1.score(X_test,y_test)

accuracy

!pip install streamlit

import streamlit as st

from sklearn.metrics import accuracy_score, classification_report

st.title("Titanic Survival Prediction")

st.sidebar.header("Options")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Dataset:")
    st.dataframe(df)

    required_columns = ["Survived", "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
    if all(col in df.columns for col in required_columns):
        st.write("### Preprocessing Data...")
        df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
        df["Embarked"] = df["Embarked"].map({"C": 1, "Q": 2, "S": 3})
        df.dropna(inplace=True)

        X = df.drop("Survived", axis=1)
        y = df["Survived"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        st.write("### Data After Preprocessing:")
        st.dataframe(pd.DataFrame(X_train, columns=X.columns).head())

        st.write("### Training the Model...")
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train_scaled, y_train)

        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        st.write("### Model Performance:")
        st.write(f"Accuracy: {accuracy:.2f}")
        st.text("Classification Report:")
        st.text(classification_report(y_test, y_pred))

        st.write("### Make Predictions:")
        with st.form("prediction_form"):
            st.write("Enter passenger details to predict survival:")
            Pclass = st.selectbox("Passenger Class (Pclass)", options=[1, 2, 3], index=2)
            Sex = st.selectbox("Sex", options=["Male", "Female"])
            Age = st.number_input("Age (in years)", min_value=0, max_value=100, value=30)
            SibSp = st.number_input("Number of Siblings/Spouses Aboard (SibSp)", min_value=0, max_value=10, value=0)
            Parch = st.number_input("Number of Parents/Children Aboard (Parch)", min_value=0, max_value=10, value=0)
            Fare = st.number_input("Passenger Fare (Fare)", min_value=0.0, value=30.0)
            Embarked = st.selectbox("Port of Embarkation (Embarked)", options=["Cherbourg (C)", "Queenstown (Q)", "Southampton (S)"])

            submitted = st.form_submit_button("Predict")

            if submitted:
                Sex = 0 if Sex == "Male" else 1
                Embarked = {"Cherbourg (C)": 1, "Queenstown (Q)": 2, "Southampton (S)": 3}[Embarked]

                input_data = pd.DataFrame({
                    "Pclass": [Pclass],
                    "Sex": [Sex],
                    "Age": [Age],
                    "SibSp": [SibSp],
                    "Parch": [Parch],
                    "Fare": [Fare],
                    "Embarked": [Embarked],
                })

                input_data_scaled = scaler.transform(input_data)

                prediction = model.predict(input_data_scaled)
                prediction_label = "Survived" if prediction[0] == 1 else "Did Not Survive"

                st.write(f"### Prediction: {prediction_label}")
    else:
        st.error(f"Dataset must contain the following columns: {', '.join(required_columns)}")
else:
    st.write("Upload a dataset to get started.")

