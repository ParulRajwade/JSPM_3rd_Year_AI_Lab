const express = require('express');
const { GoogleGenerativeAI } = require('@google/generative-ai'); // ✅ fixed spelling
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize Google Generative AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// API endpoint to generate quiz
app.post('/generate-quiz', async (req, res) => {
  try {
    const { topic, level, numQuestions } = req.body;

    // Validate input
    if (!topic || !level || !numQuestions) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    if (numQuestions < 1 || numQuestions > 20) {
      return res.status(400).json({ error: 'Number of questions must be between 1 and 20' });
    }

    // Construct the prompt
    const geminiPrompt = `
      You are an expert quiz creator. Your task is to generate a multiple-choice quiz.

      Topic: "${topic}"
      Difficulty Level: "${level}"
      Number of Questions: ${numQuestions}

      Instructions:
      1. Generate exactly ${numQuestions} questions.
      2. Each question must have 4 options (A, B, C, D).
      3. There must be only one correct answer for each question.
      4. The questions and options should be appropriate for the specified difficulty level.

      CRITICAL: You MUST respond with ONLY a valid JSON array. No explanations, no markdown, no extra text.

      The JSON format must be exactly this structure:
      [
        {
          "question": "Question text here?",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": "Correct option text"
        }
      ]

      Example:
      [
        {
          "question": "What is the capital of France?",
          "options": ["Berlin", "Madrid", "Paris", "Rome"],
          "answer": "Paris"
        },
        {
          "question": "What is 2 + 2?",
          "options": ["3", "4", "5", "6"],
          "answer": "4"
        }
      ]

      Generate the quiz now:
    `;

    // Get the model
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-pro" });

    // Generate quiz
    const result = await model.generateContent(geminiPrompt);
    const response = await result.response;
    let text = response.text();

    // Clean JSON formatting
    text = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();

    // Parse JSON
    const quizData = JSON.parse(text);

    // Debug: Log the structure to understand the format
    console.log('Raw quiz data:', JSON.stringify(quizData, null, 2));

    if (!Array.isArray(quizData)) {
      throw new Error('Invalid response format from AI');
    }

    // Validate and fix the structure of each question
    const validatedQuizData = quizData.map((question, index) => {
      if (!question.question || !question.options || !question.answer) {
        console.log(`Invalid question at index ${index}:`, question);
        throw new Error(`Invalid question structure at index ${index}`);
      }

      // Ensure options is an array
      if (!Array.isArray(question.options)) {
        console.log(`Options is not an array at index ${index}:`, question.options);
        throw new Error(`Options must be an array at index ${index}`);
      }

      return {
        question: question.question,
        options: question.options,
        answer: question.answer
      };
    });

    res.json(validatedQuizData);

  } catch (error) {
    console.error('Error generating quiz:', error);
    
    if (error.message.includes('API key')) {
      res.status(500).json({ error: 'Invalid API key. Please check your GEMINI_API_KEY in the .env file.' });
    } else if (error.message.includes('JSON')) {
      res.status(500).json({ error: 'Failed to parse quiz data. Please try again.' });
    } else {
      res.status(500).json({ error: 'Failed to generate quiz. Please try again.' });
    }
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
