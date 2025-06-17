// Get references to key DOM elements
const numberGrid = document.getElementById('number-grid');
const ticketGrid = document.getElementById('ticket-grid');
const drawnGrid = document.getElementById('drawn-grid');
const drawBtn = document.getElementById('draw-btn');
const resetBtn = document.getElementById('reset-btn');
const resultMessage = document.getElementById('result-message');

const MAX_SELECTION = 6;  // Max numbers user can select
let selectedNumbers = []; // Array to store user's selected numbers

// Create the grid of numbers from 1 to 49 for selection
function createNumberGrid() {
  for (let i = 1; i <= 49; i++) {
    const numEl = document.createElement('div');
    numEl.textContent = i;
    numEl.classList.add('number');
    // Add click event to select or deselect the number
    numEl.addEventListener('click', () => selectNumber(i, numEl));
    numberGrid.appendChild(numEl);
  }
}

// Handle selecting or deselecting a number
function selectNumber(num, element) {
  if (selectedNumbers.includes(num)) {
    // If already selected, remove from selection and update UI
    selectedNumbers = selectedNumbers.filter(n => n !== num);
    element.classList.remove('selected');
  } else {
    // If less than max selection, add the number and update UI
    if (selectedNumbers.length < MAX_SELECTION) {
      selectedNumbers.push(num);
      element.classList.add('selected');
    }
  }
  // Enable the draw button only when exactly MAX_SELECTION numbers are selected
  drawBtn.disabled = selectedNumbers.length !== MAX_SELECTION;
  
  // Clear any previous result messages
  resultMessage.textContent = '';

  // Update the ticket display with selected numbers
  displayTicket();
}

// Display the selected numbers in the ticket grid (sorted ascending)
function displayTicket() {
  ticketGrid.innerHTML = '';
  selectedNumbers.sort((a, b) => a - b);
  selectedNumbers.forEach(num => {
    const el = document.createElement('div');
    el.textContent = num;
    el.classList.add('ticket-number');
    ticketGrid.appendChild(el);
  });
}

// Randomly generate 6 unique numbers between 1 and 49 (the draw)
function generateDrawnNumbers() {
  const numbers = Array.from({ length: 49 }, (_, i) => i + 1);
  const drawn = [];
  while (drawn.length < MAX_SELECTION) {
    const idx = Math.floor(Math.random() * numbers.length);
    drawn.push(numbers.splice(idx, 1)[0]);
  }
  drawn.sort((a, b) => a - b);
  return drawn;
}

// Display the drawn numbers on the UI
function displayDrawnNumbers(drawn) {
  drawnGrid.innerHTML = '';
  drawn.forEach(num => {
    const el = document.createElement('div');
    el.textContent = num;
    el.classList.add('drawn-number');
    drawnGrid.appendChild(el);
  });
}

// Calculate which selected numbers matched the drawn numbers
function calculateWin(drawn) {
  return selectedNumbers.filter(n => drawn.includes(n));
}

// Show the result message based on how many numbers matched
function showResult(matched) {
  const count = matched.length;
  if (count === 6) {
    resultMessage.textContent = `Congratulations! You won the Grand Prize! 🎉🎉🎉`;
  } else if (count > 0) {
    resultMessage.textContent = `You guessed ${count} number(s): ${matched.join(', ')}. Try again!`;
  } else {
    resultMessage.textContent = `You didn't guess any numbers. Try again!`;
  }
}

// Handle the draw button click: perform the draw and show results
drawBtn.addEventListener('click', () => {
  displayTicket();                  // Show selected ticket numbers
  const drawn = generateDrawnNumbers(); // Draw random numbers
  displayDrawnNumbers(drawn);       // Show drawn numbers on UI
  const matched = calculateWin(drawn);  // Calculate matches
  showResult(matched);              // Display result message
  drawBtn.disabled = true;          // Disable draw button after use
});

// Handle the reset button click: reset game state and UI
resetBtn.addEventListener('click', () => {
  selectedNumbers = [];
  ticketGrid.innerHTML = '';
  drawnGrid.innerHTML = '';
  resultMessage.textContent = '';
  drawBtn.disabled = true;

  // Clear selection styles on all numbers
  document.querySelectorAll('.number.selected').forEach(el => {
    el.classList.remove('selected');
  });
});

// Initialize the game by creating the number grid on page load
createNumberGrid();
