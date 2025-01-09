<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f9f9f9;
        }
        .card {
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .grid {
            display: grid;
            gap: 20px;
        }
        .grid-cols-4 {
            grid-template-columns: repeat(4, 1fr);
        }
        .grid-cols-2 {
            grid-template-columns: repeat(2, 1fr);
        }
        .text-blue-600 {
            color: #2563eb;
        }
        .text-lg {
            font-size: 1.125rem;
        }
        .text-2xl {
            font-size: 1.5rem;
        }
        .font-bold {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <header>
        <h1 class="text-blue-600 text-2xl font-bold">Dynamic Dashboard</h1>
    </header>
    <section class="grid grid-cols-4">
        <div class="card">
            <h3 class="text-lg">Steps</h3>
            <p id="steps-value" class="text-blue-600 text-2xl font-bold">8234</p>
        </div>
        <div class="card">
            <h3 class="text-lg">Heart Rate</h3>
            <p id="heart-rate-value" class="text-blue-600 text-2xl font-bold">72 bpm</p>
        </div>
        <div class="card">
            <h3 class="text-lg">Blood Pressure</h3>
            <p id="blood-pressure-value" class="text-blue-600 text-2xl font-bold">120/80</p>
        </div>
        <div class="card">
            <h3 class="text-lg">Weight</h3>
            <p id="weight-value" class="text-blue-600 text-2xl font-bold">150 lbs</p>
        </div>
    </section>
    <section class="grid grid-cols-2">
        <div class="card">
            <h2 class="text-blue-600 text-lg font-bold">Health Overview</h2>
            <canvas id="health-overview-chart"></canvas>
        </div>
        <div class="card">
            <h2 class="text-blue-600 text-lg font-bold">Weekly Activity</h2>
            <canvas id="weekly-activity-chart"></canvas>
        </div>
    </section>
    <section>
        <div class="card">
            <h2 class="text-blue-600 text-lg font-bold">Upcoming Appointments</h2>
            <ul id="appointments-list">
                <li>Dr. Smith - General Checkup - Memorial Hospital - Tomorrow, 10:00 AM</li>
                <li>Dr. Johnson - Dental Cleaning - City Dental Clinic - Next Week, 2:00 PM</li>
                <li>Dr. Williams - Eye Exam - Vision Care Center - Jul 15, 11:30 AM</li>
            </ul>
        </div>
    </section>
    <script>
        // Data for charts
        const healthData = {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                { label: 'Steps', data: [4000, 3000, 2000, 2780, 1890, 2390], borderColor: '#2563eb', fill: false },
                { label: 'Calories', data: [2400, 1398, 9800, 3908, 4800, 3800], borderColor: '#34d399', fill: false },
                { label: 'Weight', data: [150, 151, 152, 151, 150, 149], borderColor: '#fbbf24', fill: false },
            ]
        };
        
        const activityData = {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                { label: 'Walking', data: [30, 20, 25, 15, 30, 40, 35], backgroundColor: '#2563eb' },
                { label: 'Running', data: [0, 15, 0, 20, 0, 30, 0], backgroundColor: '#34d399' },
                { label: 'Cycling', data: [0, 0, 30, 0, 20, 0, 40], backgroundColor: '#fbbf24' },
            ]
        };

        // Render charts
        const healthOverviewChart = new Chart(document.getElementById('health-overview-chart').getContext('2d'), {
            type: 'line',
            data: healthData,
            options: { responsive: true, maintainAspectRatio: false }
        });

        const weeklyActivityChart = new Chart(document.getElementById('weekly-activity-chart').getContext('2d'), {
            type: 'bar',
            data: activityData,
            options: { responsive: true, maintainAspectRatio: false }
        });

        // Update values dynamically
        const stepsElement = document.getElementById('steps-value');
        const heartRateElement = document.getElementById('heart-rate-value');
        const bloodPressureElement = document.getElementById('blood-pressure-value');
        const weightElement = document.getElementById('weight-value');
        setInterval(() => {
            const steps = Math.floor(Math.random() * 10000);
            const heartRate = Math.floor(Math.random() * 40) + 60;
            const bloodPressure = `${Math.floor(Math.random() * 20) + 110}/${Math.floor(Math.random() * 10) + 70}`;
            const weight = Math.floor(Math.random() * 5) + 145;

            stepsElement.textContent = steps;
            heartRateElement.textContent = `${heartRate} bpm`;
            bloodPressureElement.textContent = bloodPressure;
            weightElement.textContent = `${weight} lbs`;
        }, 5000);
    </script>
</body>
</html>
