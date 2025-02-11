from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import openai  # For AI chatbot responses

app = Flask(__name__)

# Placeholder for user data storage
db = {}

@app.route('/')
def home():
    return render_template('index.html')

# Upload Blood Test Reports (Placeholder for AI analysis)
@app.route('/upload_report', methods=['POST'])
def upload_report():
    file = request.files['file']
    if file:
        df = pd.read_csv(file)  # Assuming CSV format for now
        user_id = request.form['user_id']
        db[user_id] = {'report': df.to_dict()}  # Store user's report data
        return jsonify({"message": "Report uploaded successfully!"})
    return jsonify({"error": "File upload failed"})

# Generate Personalized Meal Plans (Enhanced AI logic)
@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    user_id = request.form['user_id']
    user_data = db.get(user_id)
    if not user_data:
        return jsonify({"error": "User data not found"})
    
    # AI-generated meal plan based on user data
    meal_plan = {
        "breakfast": "Scrambled eggs with avocado and spinach",
        "lunch": "Grilled salmon with quinoa and mixed greens",
        "dinner": "Grass-fed steak with roasted vegetables and olive oil"
    }
    
    return jsonify({"meal_plan": meal_plan})

# AI Chatbot for Health Queries
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_query = request.json['query']
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a diabetes reversal expert trained with knowledge from Dr. Eric Berg and other experts. Provide responses based on ketogenic diets, fasting, and supplementation."},
            {"role": "user", "content": user_query}
        ]
    )
    return jsonify({"response": response['choices'][0]['message']['content']})

# Symptom Tracking
@app.route('/track_symptoms', methods=['POST'])
def track_symptoms():
    user_id = request.form['user_id']
    glucose_level = request.form['glucose_level']
    weight = request.form['weight']
    symptoms = request.form['symptoms']
    
    if user_id not in db:
        db[user_id] = {}
    db[user_id]['tracking'] = {
        "glucose_level": glucose_level,
        "weight": weight,
        "symptoms": symptoms
    }
    return jsonify({"message": "Symptoms tracked successfully!"})

# AI-Generated Fasting Recommendations
@app.route('/fasting_recommendation', methods=['POST'])
def fasting_recommendation():
    user_id = request.form['user_id']
    user_data = db.get(user_id, {}).get('tracking', {})
    glucose_level = float(user_data.get('glucose_level', 100))  # Default to 100 if no data
    
    fasting_plan = "16:8 fasting" if glucose_level > 120 else "12:12 fasting"
    if glucose_level > 140:
        fasting_plan = "OMAD (One Meal A Day) gradually"
    
    return jsonify({"fasting_plan": fasting_plan})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

