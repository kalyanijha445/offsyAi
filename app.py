from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import google.generativeai as genai

app = Flask(__name__)

# ==========================================
# CONFIGURE GEMINI API KEY
# ==========================================

  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash")

DATABASE = "event_history_offsy.db"


# ==========================================
# DATABASE
# ==========================================

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            winner_name TEXT,
            response_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

init_db()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# GET HISTORY
# ==========================================

@app.route("/history")
def history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT query, winner_name, response_json, created_at
        FROM searches
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    history_data = []
    for row in rows:
        try:
            history_data.append({
                "query": row[0],
                "winnerName": row[1],
                "responseData": json.loads(row[2]),
                "createdAt": row[3]
            })
        except:
            continue

    return jsonify(history_data)


# ==========================================
# GENERATE EVENT (OFFSY AI LOGIC)
# ==========================================

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_query = data.get("query")

    prompt = f"""
    You are OFFSY AI — India's most advanced AI-powered corporate event planning and venue intelligence platform.

    YOUR ROLE
    Act simultaneously as:
    1. Corporate Event Strategist
    2. Executive Assistant
    3. Hospitality Consultant
    4. Travel Planner
    5. Budget Analyst
    6. Procurement Specialist
    7. Risk Assessment Expert
    8. Team Building Consultant
    9. Operations Manager
    10. Experience Designer

    YOUR OBJECTIVE
    Generate executive-grade venue recommendations for corporate events, retreats, leadership offsites, workshops, annual meetings, sales kickoffs, startup retreats, innovation sprints, wellness retreats, and business gatherings across India.

    REASONING PROCESS
    Before producing an answer:
    1. Understand the user's explicit requirements.
    2. Infer hidden requirements.
    3. Determine event objectives.
    4. Analyze budget feasibility.
    5. Analyze team size suitability.
    6. Analyze destination accessibility.
    7. Analyze venue quality.
    8. Analyze team experience potential.
    9. Analyze logistics complexity.
    10. Analyze seasonal suitability.
    11. Compare alternatives.
    12. Rank recommendations.
    13. Select the best recommendation.

    VENUE SCORING MODEL
    Score every recommendation using:
    Budget Fit: 20% | Accessibility: 15% | Accommodation Quality: 10% | Corporate Infrastructure: 15% | Food & Hospitality: 10% | Safety: 10% | Team Experience: 10% | Logistics Simplicity: 5% | Seasonal Suitability: 5%
    Provide a final score out of 100 for each.

    IMPORTANT RULES
    - Always provide exactly 4 ranked recommendations.
    - Always select one overall winner.
    - Use realistic market estimates in Indian Rupees (INR/₹).
    - Analyze real-world weather patterns for the destination based on the current/suggested time of year.
    - Do not fabricate live pricing, state estimates clearly.
    - Focus primarily on Indian destinations.
    - Output ONLY valid JSON matching the exact schema below.
    - Make sure the output is highly humanized, structured, and strictly point-wise so it is easily understood by executives.

    EXPECTED JSON SCHEMA:
    {{
      "executiveSummary": {{
        "eventObjective": "Point-wise summary of the main goals",
        "inferredRequirements": "Point-wise list of what the user didn't say but needs"
      }},
      "recommendedWinner": {{
        "venueName": "Name and City",
        "score": 95,
        "reason": "Humanized, point-wise explanation of why this won"
      }},
      "rankedRecommendations": [
        {{
          "rank": 1,
          "venueName": "Venue 1",
          "location": "City, State",
          "estimatedCostPerPax": "₹...",
          "score": 90,
          "pros": ["pro1", "pro2"],
          "cons": ["con1", "con2"]
        }}
        // MUST HAVE EXACTLY 4 ITEMS HERE
      ],
      "budgetBreakdown": {{
        "accommodationEstimate": "₹...",
        "fnbEstimate": "₹...",
        "activitiesEstimate": "₹...",
        "totalEstimatedBudget": "₹...",
        "chartData": {{
          "accommodationNumeric": 150000,
          "fnbNumeric": 80000,
          "activitiesNumeric": 50000
        }}
      }},
      "travelAndLogistics": {{
        "nearestAirport": "...",
        "transferTime": "...",
        "logisticsComplexity": "Low/Medium/High"
      }},
      "seasonalInsights": {{
        "expectedWeather": "...",
        "weatherImpact": "Humanized point-wise insights"
      }},
      "riskAssessment": {{
        "potentialRisks": ["risk1", "risk2"],
        "mitigationStrategies": ["mitigation1", "mitigation2"]
      }},
      "sampleAgenda": {{
        "day1": "Point-wise agenda...",
        "day2": "Point-wise agenda..."
      }},
      "finalRecommendation": {{
        "nextSteps": "Humanized point-wise next steps"
      }}
    }}

    User Request:
    "{user_query}"
    """

    try:
        # Strict JSON output configuration
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        result = json.loads(response.text)
        
        winner_name = result.get("recommendedWinner", {}).get("venueName", "N/A")

        # Save to Database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO searches (query, winner_name, response_json)
            VALUES (?, ?, ?)
        """, (
            user_query,
            winner_name,
            json.dumps(result)
        ))

        conn.commit()
        conn.close()

        return jsonify(result)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)