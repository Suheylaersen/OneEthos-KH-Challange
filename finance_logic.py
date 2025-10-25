from state_tax_data import STATE_TAX_RATES

def estimate_state_tax_rate(state_code: str) -> float:
    """
    Return estimated state income tax % for that state code.
    If unknown, default to 5% just so we don't crash.
    """
    return STATE_TAX_RATES.get(state_code.upper(), 0.05)

def build_financial_plan(monthly_salary: float, state_code: str):
    """
    Take user's monthly gross salary and state, return budget plan info.
    """

    # 1. Estimate state tax & take-home
    state_rate = estimate_state_tax_rate(state_code)
    est_state_tax_monthly = monthly_salary * state_rate
    take_home = monthly_salary - est_state_tax_monthly
    if take_home < 0:
        take_home = 0

    # 2. Split their *take-home* into 50/30/20 buckets
    needs = take_home * 0.50
    wants = take_home * 0.30
    future = take_home * 0.20

    # 3. Emergency fund target = 3 months of NEEDS
    emergency_goal_total = needs * 3

    # Put 50% of "future you" bucket toward building that fund each month
    monthly_to_emergency = future * 0.5
    months_to_goal = (
        emergency_goal_total / monthly_to_emergency
        if monthly_to_emergency > 0
        else None
    )

    # 4. Recommended housing cap: ~30% of take-home
    max_rent_util = take_home * 0.30

    # 5. Money left for debt snowball: the other half of "future you"
    debt_snowball = future * 0.5

    # We return a dictionary that we'll send as JSON to the browser
    return {
        "inputs": {
            "state": state_code.upper(),
            "gross_monthly_salary": monthly_salary,
            "estimated_state_tax_rate": state_rate,
            "estimated_state_tax_monthly": est_state_tax_monthly,
            "estimated_take_home_after_state_tax": take_home,
        },
        "budget": {
            "needs": needs,
            "wants": wants,
            "future": future,
            "max_recommended_rent_util": max_rent_util,
        },
        "goals": {
            "emergency_fund_target": emergency_goal_total,
            "emergency_fund_monthly": monthly_to_emergency,
            "emergency_fund_months_to_goal": months_to_goal,
            "debt_snowball_recommendation": debt_snowball,
            "note": (
                "Save ~3 months of essentials first. "
                "Use ~50% of your 'future you' money for that emergency fund "
                "until it's full, then throw that money at debt or investing. "
                "This calculation only uses state income tax, not federal or city."
            )
        }
    }
