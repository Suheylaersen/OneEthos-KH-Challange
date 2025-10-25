from flask import Flask, jsonify, request, render_template
from models import db, Plan
from finance_logic import build_financial_plan

app = Flask(__name__)

# use sqlite db file called finance.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

################################
# PAGE ROUTES
################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plan')
def plan_page():
    # templates/features/financial_planning.html
    return render_template('features/financial_planning.html')

@app.route('/coach')
def coach_page():
    # templates/features/ai_coach.html
    return render_template('features/ai_coach.html')

################################
# API ROUTES
################################

@app.route('/api/plan', methods=['POST'])
def api_plan():
    data = request.get_json()
    salary = float(data.get("salary", 0))
    state = data.get("state", "FL").upper()

    if salary <= 0:
        return jsonify({"error": "Please enter a valid monthly salary > 0."}), 400

    result = build_financial_plan(salary, state)

    # save plan to DB for history
    plan_row = Plan(
        state=result["inputs"]["state"],
        gross_monthly_salary=result["inputs"]["gross_monthly_salary"],
        est_state_tax_rate=result["inputs"]["estimated_state_tax_rate"],
        est_state_tax_monthly=result["inputs"]["estimated_state_tax_monthly"],
        est_take_home=result["inputs"]["estimated_take_home_after_state_tax"],
        needs=result["budget"]["needs"],
        wants=result["budget"]["wants"],
        future=result["budget"]["future"],
        max_rent_util=result["budget"]["max_recommended_rent_util"],
        emergency_goal_total=result["goals"]["emergency_fund_target"],
        emergency_monthly=result["goals"]["emergency_fund_monthly"],
        emergency_months_to_goal=result["goals"]["emergency_fund_months_to_goal"],
        debt_snowball=result["goals"]["debt_snowball_recommendation"],
    )
    db.session.add(plan_row)
    db.session.commit()

    return jsonify(result), 200


@app.route('/api/coach', methods=['POST'])
def api_coach():
    data = request.get_json()
    user_msg = data.get("message", "").strip()

    answer = (
        "Here's general guidance (not legal/tax advice):\n"
        "- Build an emergency fund (~3 months of essentials) first.\n"
        "- Keep rent+utilities around 30% of your take-home.\n"
        "- Use your 'future you' bucket to kill high-interest debt.\n"
        "- High-tax states (CA, NY, HI) = lower take-home, cut 'wants'.\n"
        "- No-income-tax states (FL, TX, WA) = push more into savings.\n\n"
        f'Your question was: "{user_msg}"'
    )

    return jsonify({"answer": answer}), 200


################################
# START APP
################################

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
