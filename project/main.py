import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# =========================
# Read the data and train our Model
# =========================
data = pd.read_csv("Heart_Disease_Emergency.csv")

X = data[
    [
        "Age",
        "Sex",
        "Blood Pressure (BP)",
        "Max HR",
        "ST depression (ECG)",
        "Blood Glucose",
    ]
]

y = data["Heart Disease"]

model = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression())])

model.fit(X, y)


# =========================
# Prediction Function
# =========================
def predict_risk():
    try:
        age = int(age_entry.get())
        sex = 1 if sex_var.get() == "Male" else 0
        bp = float(bp_entry.get())
        hr = float(hr_entry.get())
        st = float(st_entry.get())
        glucose = float(glucose_entry.get())

        input_data = np.array([[age, sex, bp, hr, st, glucose]])
        prob = model.predict_proba(input_data)[0][1]
        percentage = prob * 100

        # Risk Level
        if percentage < 30:
            risk = "Low Risk"
        elif percentage < 60:
            risk = "Medium Risk"
        else:
            risk = "High Risk"

        # Explanation
        reasons = []
        if bp >= 140:
            reasons.append("High Blood Pressure")
        if glucose > 140:
            reasons.append("High Blood Glucose")
        if hr > 130:
            reasons.append("Abnormal Heart Rate")
        if st > 1:
            reasons.append("Abnormal ST depression (ECG)")

        explanation = (
            "\n".join(reasons) if reasons else "All readings are within normal range."
        )

        result_label.config(
            text=f"Heart Disease Probability: {percentage:.2f}%\nRisk Level: {risk}"
        )
        explanation_label.config(text=f"Reason(s):\n{explanation}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")


# =========================
# GUI
# =========================
root = tk.Tk()
root.title("Emergency Heart Risk Assessment System")
root.geometry("500x600")

tk.Label(root, text="Patient Readings", font=("Arial", 16, "bold")).pack(pady=10)


def add_entry(label):
    tk.Label(root, text=label).pack()
    entry = tk.Entry(root)
    entry.pack()
    return entry


age_entry = add_entry("Age")
bp_entry = add_entry("Blood Pressure (BP)")
hr_entry = add_entry("Heart Rate (Max HR)")
st_entry = add_entry("ST depression (ECG)")
glucose_entry = add_entry("Blood Glucose")

tk.Label(root, text="Sex").pack()
sex_var = tk.StringVar(value="Male")
tk.OptionMenu(root, sex_var, "Male", "Female").pack()

tk.Button(root, text="Predict Risk", command=predict_risk, bg="green", fg="white").pack(
    pady=15
)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

explanation_label = tk.Label(root, text="", wraplength=450, justify="left")
explanation_label.pack(pady=10)

tk.Label(
    root,
    text="⚠️ This tool is a decision support system, not a medical diagnosis.",
    fg="red",
    wraplength=450,
).pack(pady=20)

root.mainloop()
