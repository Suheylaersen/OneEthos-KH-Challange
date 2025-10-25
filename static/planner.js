const button = document.getElementById('submitBtn');
const salaryInput = document.getElementById('salaryInput');
const stateInput = document.getElementById('stateInput');
const cardsContainer = document.getElementById('cardsContainer');

function money(n) {
    return n.toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    });
}

button.addEventListener('click', async () => {
    const salaryVal = parseFloat(salaryInput.value.trim());
    const stateVal = stateInput.value.trim().toUpperCase();

    cardsContainer.innerHTML = '';

    if (isNaN(salaryVal) || salaryVal <= 0) {
        cardsContainer.innerHTML = `
            <div class="bg-red-100 border border-red-300 text-red-800 rounded-lg p-4 text-center col-span-full">
                <p class="font-semibold">Please enter a valid monthly salary.</p>
            </div>
        `;
        return;
    }

    const res = await fetch("/api/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ salary: salaryVal, state: stateVal })
    });

    const data = await res.json();

    if (data.error) {
        cardsContainer.innerHTML = `
            <div class="bg-red-100 border border-red-300 text-red-800 rounded-lg p-4 text-center col-span-full">
                <p class="font-semibold">${data.error}</p>
            </div>
        `;
        return;
    }

    // Card 1: Income / tax info
    const incomeCard = document.createElement('div');
    incomeCard.className = 'bg-white rounded-xl shadow-md p-6 text-center border border-gray-200';
    incomeCard.innerHTML = `
        <h3 class="text-xl font-bold text-black mb-2">Your Income in ${data.inputs.state}</h3>
        <p class="text-gray-700"><strong>Gross Monthly:</strong> ${money(data.inputs.gross_monthly_salary)}</p>
        <p class="text-gray-700"><strong>Est. State Tax Rate:</strong> ${(data.inputs.estimated_state_tax_rate * 100).toFixed(2)}%</p>
        <p class="text-gray-700"><strong>Est. State Tax Paid Monthly:</strong> ${money(data.inputs.estimated_state_tax_monthly)}</p>
        <p class="text-gray-700 mt-2"><strong>Est. Take-Home After State Tax:</strong><br>${money(data.inputs.estimated_take_home_after_state_tax)}</p>
        <p class="text-xs text-gray-500 mt-3">
            State only. No federal / Social Security / Medicare / city tax.
        </p>
    `;
    cardsContainer.appendChild(incomeCard);

    // Card 2: Budget
    const budgetCard = document.createElement('div');
    budgetCard.className = 'bg-white rounded-xl shadow-md p-6 text-center border border-gray-200';
    budgetCard.innerHTML = `
        <h3 class="text-xl font-bold text-black mb-2">Suggested Monthly Budget</h3>
        <p class="text-gray-700"><strong>Essentials (50%):</strong> ${money(data.budget.needs)}</p>
        <p class="text-gray-700"><strong>Wants (30%):</strong> ${money(data.budget.wants)}</p>
        <p class="text-gray-700"><strong>Future You (20%):</strong> ${money(data.budget.future)}</p>
        <p class="text-gray-700 mt-2"><strong>Max Rent + Utilities Goal:</strong> ${money(data.budget.max_recommended_rent_util)}</p>
        <p class="text-xs text-gray-500 mt-3">
            Try to keep rent + utilities ≈30% of take-home.
        </p>
    `;
    cardsContainer.appendChild(budgetCard);

    // Card 3: Goals
    const goalsCard = document.createElement('div');
    goalsCard.className = 'bg-white rounded-xl shadow-md p-6 text-center border border-gray-200';
    goalsCard.innerHTML = `
        <h3 class="text-xl font-bold text-black mb-2">Your Next Money Goals</h3>
        <p class="text-gray-700"><strong>Emergency Fund Target (3 mo needs):</strong> ${money(data.goals.emergency_fund_target)}</p>
        <p class="text-gray-700"><strong>Save Each Month:</strong> ${money(data.goals.emergency_fund_monthly)}</p>
        <p class="text-gray-700"><strong>Months To Goal:</strong> ${
            data.goals.emergency_fund_months_to_goal
                ? data.goals.emergency_fund_months_to_goal.toFixed(1)
                : "N/A"
        }</p>
        <p class="text-gray-700"><strong>Debt Snowball Monthly:</strong> ${money(data.goals.debt_snowball_recommendation)}</p>
        <p class="text-xs text-gray-500 mt-3">${data.goals.note}</p>
    `;
    cardsContainer.appendChild(goalsCard);
});
