from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure the SQLite database exists and create the table if not present
def init_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('PRAGMA journal_mode=WAL;') 
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('signup'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = sqlite3.connect('users.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, age, email, password) VALUES (?, ?, ?, ?)", 
                           (name, age, email, hashed_password))
            conn.commit()
            conn.close()

            session['logged_in'] = True
            session['name'] = name 

            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please try a different email.')
            return redirect(url_for('signup'))

    return render_template('sp.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
            session['logged_in'] = True
            session['name'] = user[1]
            return redirect(url_for('dashboard')) 
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))

    return render_template('lp.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    name = session.get("name", "User")
    return render_template('db.html', name=name)

@app.route('/Problem-Solving')
def problem_solving():
    return render_template('psdb.html', quizzes=quizzes)

quizzes = {

    "Brain_Test": {
        "title": "BrainTest Quiz",
        "questions": [
            ("Do you have trouble remembering names, dates, or recent events?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel mentally fatigued after short periods of focus?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you find it hard to concentrate or stay focused on tasks?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you often forget where you placed objects like keys or phones?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience frequent mood swings or irritability?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced unexplained confusion or disorientation?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you find it challenging to follow conversations or instructions?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel mentally sluggish or unable to think clearly?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced unexplained headaches or head pressure?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have trouble sleeping or feel unrested upon waking?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you struggle to learn new skills or retain new information?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience difficulty with decision-making or problem-solving?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you often lose your train of thought during conversations?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you noticed a significant decline in your memory or thinking ability?", ["No", "Not sure", "Minor decline", "Significant decline"]),
            ("Do you have difficulty handling stress or pressure effectively?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience episodes of dizziness or lightheadedness?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you ever felt numbness or tingling in your body without cause?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel that your mental health affects your daily life?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel a lack of motivation or interest in activities you used to enjoy?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced difficulty expressing your thoughts or finding the right words?", ["Never", "Rarely", "Sometimes", "Often"]),
        ]
    },

    "Lungs_Test": {
        "title": "Lings Test Quiz",
        "questions": [
            ("Do you experience shortness of breath during everyday activities?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you frequently have a persistent cough?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you cough up mucus or phlegm regularly?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced wheezing or a whistling sound when breathing?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel chest tightness or discomfort while breathing?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you been diagnosed with asthma, COPD, or another lung condition?", ["No", "Not sure", "Mild condition", "Yes, diagnosed"]),
            ("Do you smoke or have you smoked in the past?", ["Never", "Quit years ago", "Occasionally", "Yes, regularly"]),
            ("Do you live or work in an area with high air pollution?", ["No", "Rarely", "Occasionally", "Yes, regularly"]),
            ("Do you have trouble breathing when exposed to strong odors or fumes?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced frequent respiratory infections (e.g., colds, pneumonia)?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you wake up at night feeling short of breath?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you been exposed to secondhand smoke regularly?", ["No", "Rarely", "Occasionally", "Yes, regularly"]),
            ("Do you have difficulty keeping up with physical activity due to breathing issues?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience fatigue or weakness after minor physical exertion?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you hear crackling sounds or unusual noises while breathing?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced unexplained weight loss along with breathing issues?", ["No", "Minor loss", "Moderate loss", "Significant loss"]),
            ("Do you have a family history of lung diseases?", ["No", "Not sure", "Some family members", "Yes, many family members"]),
            ("Do you have frequent allergies or hay fever symptoms affecting your breathing?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you ever worked in industries with exposure to dust or chemicals?", ["No", "Occasionally", "Sometimes", "Yes, frequently"]),
            ("Do you experience prolonged coughing after minor respiratory infections?", ["Never", "Rarely", "Sometimes", "Often"]),
        ]
    },

    "Nose_Test": {
        "title": "Nose Test Quiz",
        "questions": [
            ("Do you experience frequent nasal congestion or stuffiness?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel pressure or pain around your nose or sinuses?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you frequently have a runny nose?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience sneezing fits, especially in the morning?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have difficulty breathing through your nose?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you noticed a reduced sense of smell recently?", ["No", "Minor reduction", "Moderate reduction", "Significant reduction"]),
            ("Do you experience nosebleeds frequently?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel irritation or dryness in your nasal passages?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience symptoms of nasal allergies (e.g., itching, sneezing)?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you been diagnosed with sinus infections or sinusitis?", ["No", "Not sure", "Occasionally", "Yes, regularly"]),
            ("Do you snore or have breathing difficulties while sleeping?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do strong odors or perfumes irritate your nose?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced nasal polyps or other obstructions?", ["No", "Not sure", "Minor issues", "Yes, diagnosed"]),
            ("Do you feel your nasal symptoms worsen during allergy seasons?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you often use nasal sprays or decongestants?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced facial pain associated with nasal issues?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience frequent colds or nasal infections?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience nasal dripping into your throat (postnasal drip)?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel tired or fatigued due to nasal problems?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you live or work in environments with high dust or pollution?", ["No", "Rarely", "Occasionally", "Yes, frequently"]),
        ]
    },

    "Stomach_Test": {
        "title": "Stomach Test Quiz",
        "questions": [
            ("Do you experience stomach pain or cramps?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel bloated or full after eating?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you frequently experience heartburn or acid reflux?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have frequent diarrhea or constipation?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you often feel nauseous or vomit?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel fatigued or weak after eating?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience a loss of appetite?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you noticed blood in your stool?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have frequent belching or burping?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you suffer from indigestion or difficulty digesting food?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel a burning sensation in your stomach?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience weight loss without trying?", ["No", "Minor change", "Moderate change", "Significant change"]),
            ("Do you frequently use antacids or digestive aids?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have difficulty swallowing or a sensation of food stuck in your throat?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you been diagnosed with conditions like gastritis or ulcers?", ["No", "Not sure", "Minor issues", "Yes, diagnosed"]),
            ("Do you experience frequent gas or flatulence?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel excessively full even after a small meal?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel discomfort after eating fatty or spicy foods?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you been diagnosed with any food allergies or sensitivities?", ["No", "Not sure", "Minor issues", "Yes, diagnosed"]),
        ]
    },

    "Throat_Test": {
        "title": "Throat Test Quiz",
        "questions": [
            ("Do you experience a sore throat frequently?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have difficulty swallowing?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you often clear your throat?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have a hoarse or weak voice?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience pain or discomfort while swallowing?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have a dry throat or mouth?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you often cough, especially after talking?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you noticed a change in the sound of your voice?", ["No", "Minor change", "Moderate change", "Significant change"]),
            ("Do you feel like something is stuck in your throat?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you had a persistent cough lasting more than a week?", ["No", "Rarely", "Sometimes", "Often"]),
            ("Do you frequently experience a dry, scratchy throat?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you suffer from tonsillitis or frequent throat infections?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have difficulty breathing through your throat?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience post-nasal drip or mucus in your throat?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you snore or have difficulty sleeping due to throat issues?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have a history of acid reflux affecting your throat?", ["No", "Rarely", "Sometimes", "Often"]),
            ("Do you notice swelling in your neck or throat area?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel fatigued or out of breath due to throat issues?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience a metallic or bitter taste in your mouth?", ["Never", "Rarely", "Sometimes", "Often"]),
        ]
    },

    "Kidney_Test": {
        "title": "Kidney Test Quiz",
        "questions":[
            ("Do you experience frequent urination, especially at night?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you notice blood in your urine?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have pain or a burning sensation while urinating?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience swelling in your hands, feet, or face?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel fatigued or lack energy frequently?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience back pain or pain in your lower side?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you notice changes in the color of your urine?", ["No", "Minor change", "Moderate change", "Significant change"]),
            ("Do you suffer from high blood pressure?", ["No", "Rarely", "Sometimes", "Often"]),
            ("Do you have difficulty concentrating or experience brain fog?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience nausea or vomiting frequently?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you notice foamy or bubbly urine?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience a metallic taste in your mouth?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have a poor appetite or sudden weight loss?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience dry and itchy skin?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have a history of diabetes or high cholesterol?", ["No", "Rarely", "Sometimes", "Often"]),
            ("Do you frequently feel cold, even in warm environments?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience shortness of breath without exertion?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you notice puffiness around your eyes, especially in the morning?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you consume excessive salt or high-protein foods regularly?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience persistent thirst?", ["Never", "Rarely", "Sometimes", "Often"]),
        ]
    },

    "Heart_Test": {
        "title": "Heart Test Quiz",
        "questions":[
            ("Do you experience chest pain or discomfort during physical activity?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel shortness of breath while at rest or with minimal exertion?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you experienced irregular heartbeats or palpitations?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have swelling in your ankles, feet, or legs?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel fatigued or unusually tired most of the time?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Have you ever fainted or felt dizzy without an obvious cause?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have a family history of heart disease?", ["No", "I'm not sure", "Some family members", "Yes, many family members"]),
            ("Do you have high blood pressure?", ["No", "Not diagnosed, but I suspect", "Occasionally high", "Yes, diagnosed"]),
            ("Are you a smoker or have you smoked in the past?", ["Never", "Quit years ago", "Occasionally", "Yes, regularly"]),
            ("Do you frequently eat processed or unhealthy foods?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you engage in regular physical activity (e.g., exercise, sports)?", ["Yes, regularly", "Occasionally", "Rarely", "Never"]),
            ("Have you experienced unexplained pain in your jaw, back, or arms?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you have high cholesterol levels?", ["No", "Not sure", "Slightly elevated", "Yes, high"]),
            ("Have you gained significant weight recently?", ["No", "A little", "Moderate weight gain", "Significant weight gain"]),
            ("Do you experience difficulty sleeping or have sleep apnea?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you feel stressed or anxious most of the time?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you consume alcohol frequently?", ["Never", "Occasionally", "Sometimes", "Often"]),
            ("Have you been diagnosed with diabetes or prediabetes?", ["No", "Not sure", "Prediabetes", "Yes, diabetes"]),
            ("Do you frequently feel cold, especially in your hands or feet?", ["Never", "Rarely", "Sometimes", "Often"]),
            ("Do you experience headaches or vision problems due to high blood pressure?", ["Never", "Rarely", "Sometimes", "Often"]),
        ]
    },

    "Eye_Test": {
        "title": "Eye Test Quiz",
        "questions":[
            ("Can you read road signs clearly from a distance?", ["Always", "Sometimes", "Rarely", "Never"]),
            ("How well can you see the details of distant objects?", ["Very clearly", "Somewhat clearly", "Slightly blurry", "Very blurry"]),
            ("When watching TV, can you see the text on the screen clearly?", ["Perfectly clear", "Slightly blurry", "Mostly blurry", "Can't see at all"]),
            ("Do you experience discomfort or blurry vision when reading a book?", ["Never", "Rarely", "Sometimes", "Always"]),
            ("Can you see your phone screen clearly without moving it farther away?", ["Yes, perfectly clear", "Slightly blurry", "Mostly blurry", "Not at all"]),
            ("After prolonged reading or writing, do you feel eye strain or blurry vision?", ["Never", "Occasionally", "Often", "Always"]),
            ("When looking at a grid of straight lines, do the lines appear distorted?", ["No distortion", "Slight distortion", "Moderate distortion", "Very wavy"]),
            ("When shifting focus between near and far objects, do your eyes adjust quickly?", ["Always", "Occasionally slow", "Often slow", "Very slow or difficult"]),
            ("Do you frequently experience blurry vision at all distances?", ["Never", "Occasionally", "Often", "Always"]),
            ("When looking at red and green objects, do they appear:", ["Clearly different", "Slightly hard to distinguish", "Often confused", "Indistinguishable"]),
            ("When looking at a rainbow, can you identify all the colors?", ["Yes, clearly", "Mostly clear but a few are hard to see", "Many colors are missing", "Can't distinguish most colors"]),
            ("In a traffic light, how clearly can you identify the red, yellow, and green lights?", ["Perfectly clear", "Occasionally confusing", "Often confusing", "Always confusing"]),
            ("After prolonged screen time, do your eyes feel tired or strained?", ["Never", "Occasionally", "Frequently", "Always"]),
            ("Do you experience headaches after focusing on a screen or reading?", ["Never", "Occasionally", "Often", "Always"]),
            ("Do bright lights or glare bother your eyes?", ["Not at all", "Rarely", "Often", "Always"]),
            ("How well can you read text in dim lighting?", ["Very well", "Slightly difficult", "Very difficult", "Impossible"]),
            ("Do you experience double vision (seeing two images of the same object)?", ["Never", "Rarely", "Occasionally", "Frequently"]),
            ("Do you see spots, flashes, or floaters in your vision?", ["Never", "Occasionally", "Often", "Always"]),
            ("Do you feel pain or discomfort in your eyes regularly?", ["Never", "Rarely", "Occasionally", "Frequently"]),
            ("How often do you get your eyes checked by a professional?", ["Once a year or more", "Every few years", "Rarely", "Never"]),
        ]
    },
}

@app.route('/quiz/<disease>', methods=["GET", "POST"])
def quiz(disease):
    if disease not in quizzes:
        return "Invalid disease test", 404

    selected_quiz = quizzes[disease]
    questions = selected_quiz["questions"]
    selected_questions = random.sample(questions, 10)

    responses = []

    if request.method == 'POST':
        for i, question in enumerate(selected_questions):
            response = request.form.get(f'question_{i}')
            responses.append(response)
        issues_detected = evaluate_responses(responses)
        return render_template('psr.html', issues_detected=issues_detected, responses=responses)

    return render_template("psq.html", quiz=selected_quiz, questions=selected_questions)

def evaluate_responses(responses):
    issues_detected = []
    for response in responses:
        if response == 'Often': 
            issues_detected.append("Possible issue detected")
    return issues_detected

@app.route('/Track-Reports')
def Track_Reports():
    return render_template('trdb.html')

@app.route('/Locate-Nearby-Hospitals-and-Medical-Shops')
def Locate_Nearby_Hospitals_and_Medical_Shops():
    return render_template('nhsdb.html')

@app.route('/About-Us')
def About_Us():
    return render_template('audb.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  
    app.run(debug=True, use_reloader=False)
