// Get DOM elements
const form = document.getElementById('quiz-form');
const generateBtn = document.getElementById('generate-btn');
const loader = document.getElementById('loader');
const quizContainer = document.getElementById('quiz-container');

// Add event listener to the form
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Get form values
    const topic = document.getElementById('topic-input').value.trim();
    const level = document.getElementById('level-select').value;
    const numQuestions = parseInt(document.getElementById('questions-input').value);
    
    // Basic validation
    if (!topic) {
        showError('Please enter a topic for the quiz.');
        return;
    }
    
    if (!level) {
        showError('Please select a difficulty level.');
        return;
    }
    
    if (numQuestions < 1 || numQuestions > 20) {
        showError('Number of questions must be between 1 and 20.');
        return;
    }
    
    // Generate the quiz
    await generateQuiz(topic, level, numQuestions);
});

// Function to generate quiz
async function generateQuiz(topic, level, numQuestions) {
    try {
        // Show loader and clear previous content
        showLoader();
        clearQuiz();
        
        // Make API request
        const response = await fetch('/generate-quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: topic,
                level: level,
                numQuestions: numQuestions
            })
        });
        
        const data = await response.json();
        
        // Hide loader
        hideLoader();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate quiz');
        }
        
        // Display the quiz
        displayQuiz(data);
        
    } catch (error) {
        hideLoader();
        console.error('Error generating quiz:', error);
        showError(`Failed to generate quiz: ${error.message}`);
    }
}

// Function to display the quiz
function displayQuiz(quizData) {
    if (!Array.isArray(quizData) || quizData.length === 0) {
        showError('No quiz data received.');
        return;
    }
    
    // Clear any previous content
    clearQuiz();
    
    // Create quiz header
    const quizHeader = document.createElement('div');
    quizHeader.className = 'success-message';
    quizHeader.innerHTML = `
        <h3>🎉 Your Quiz is Ready!</h3>
        <p>Answer the questions below. Good luck!</p>
    `;
    quizContainer.appendChild(quizHeader);
    
    // Create each question
    quizData.forEach((questionData, index) => {
        const questionElement = createQuestionElement(questionData, index + 1);
        quizContainer.appendChild(questionElement);
    });
    
    // Scroll to quiz
    quizContainer.scrollIntoView({ behavior: 'smooth' });
}

// Function to create a question element
function createQuestionElement(questionData, questionNumber) {
    const questionDiv = document.createElement('div');
    questionDiv.className = 'quiz-question';
    
    // Question number and text
    const questionNumberDiv = document.createElement('div');
    questionNumberDiv.className = 'question-number';
    questionNumberDiv.textContent = `Question ${questionNumber}`;
    
    const questionTextDiv = document.createElement('div');
    questionTextDiv.className = 'question-text';
    questionTextDiv.textContent = questionData.question;
    
    // Options list
    const optionsList = document.createElement('ul');
    optionsList.className = 'options-list';
    
    questionData.options.forEach((option, index) => {
        const optionElement = createOptionElement(option, index, questionData.answer);
        optionsList.appendChild(optionElement);
    });
    
    // Assemble the question
    questionDiv.appendChild(questionNumberDiv);
    questionDiv.appendChild(questionTextDiv);
    questionDiv.appendChild(optionsList);
    
    return questionDiv;
}

// Function to create an option element
function createOptionElement(optionText, index, correctAnswer) {
    const optionLi = document.createElement('li');
    optionLi.className = 'option';
    
    // Option letter (A, B, C, D)
    const optionLetter = document.createElement('div');
    optionLetter.className = 'option-letter';
    optionLetter.textContent = String.fromCharCode(65 + index); // A, B, C, D
    
    // Option text
    const optionTextDiv = document.createElement('div');
    optionTextDiv.className = 'option-text';
    optionTextDiv.textContent = optionText;
    
    // Add click handler for interactive feedback
    optionLi.addEventListener('click', () => {
        // Remove previous selections from this question
        const question = optionLi.closest('.quiz-question');
        const allOptions = question.querySelectorAll('.option');
        allOptions.forEach(opt => {
            opt.classList.remove('selected', 'correct', 'incorrect');
        });
        
        // Mark this option as selected
        optionLi.classList.add('selected');
        
        // Check if it's correct
        if (optionText === correctAnswer) {
            optionLi.classList.add('correct');
            optionLi.style.borderColor = '#28a745';
            optionLi.style.backgroundColor = '#d4edda';
        } else {
            optionLi.classList.add('incorrect');
            optionLi.style.borderColor = '#dc3545';
            optionLi.style.backgroundColor = '#f8d7da';
            
            // Also highlight the correct answer
            allOptions.forEach(opt => {
                if (opt.querySelector('.option-text').textContent === correctAnswer) {
                    opt.classList.add('correct');
                    opt.style.borderColor = '#28a745';
                    opt.style.backgroundColor = '#d4edda';
                }
            });
        }
    });
    
    optionLi.appendChild(optionLetter);
    optionLi.appendChild(optionTextDiv);
    
    return optionLi;
}

// Function to show loader
function showLoader() {
    loader.classList.remove('hidden');
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';
}

// Function to hide loader
function hideLoader() {
    loader.classList.add('hidden');
    generateBtn.disabled = false;
    generateBtn.textContent = 'Generate Quiz';
}

// Function to clear quiz content
function clearQuiz() {
    quizContainer.innerHTML = '';
}

// Function to show error message
function showError(message) {
    clearQuiz();
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <h3>❌ Error</h3>
        <p>${message}</p>
    `;
    quizContainer.appendChild(errorDiv);
}
