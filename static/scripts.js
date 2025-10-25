const button = document.getElementById('submitBtn');
const input = document.getElementById('salaryInput');
const cardsContainer = document.getElementById('cardsContainer');

button.addEventListener('click', () => {
    const salary = input.value.trim();
    cardsContainer.innerHTML = ''; // Clear any existing cards


    const card = document.createElement('div');
    card.className = 'bg-white rounded-lg shadow-md p-6 text-center';
    card.innerHTML = `<p class="text-lg font-medium">Your Budget</p>`;
    cardsContainer.appendChild(card);

});