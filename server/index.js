import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { ensureThreadExists, handleChatInteraction, getBookPlan, myThread } from './conversations/bookPlan.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { OutlineGenerator } from './conversations/bookOutlining.js';
//import BookOutline from './BookOutlines/BookOutline.json' assert {type: "json"};


const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// To do
// 1. check for null thread_id and create a new thread if it is null to handle multiple sessions
// 2. integrate database support to store thread_id and user messages

const app = express();

const PORT = 3001;

app.use(cors({
  origin: 'http://localhost:3000',
  methods: "GET,HEAD,PUT,PATCH,POST,DELETE"
}));

app.use(express.json());


app.post('/chat', async (req, res) => {
  const userMessage = req.body.message;
  try {
    await ensureThreadExists();
    const botReply = await handleChatInteraction(userMessage);

    // Check if botReply contains the string
    const isSummaryComplete = botReply.includes('"status": "Summary Complete"');
    if (isSummaryComplete) {
      const bookPlan = await getBookPlan(myThread.id);
      console.log('Book Plan:', bookPlan);
      // simulate storing the book plan in the database
      const filePath = path.join(__dirname, 'BookPlans', 'BookPlan.json');
      fs.writeFileSync(filePath, JSON.stringify(bookPlan));
    }
    // Add the Summary Complete flag to the response if detected
    res.json({ reply: botReply, summaryComplete: isSummaryComplete });
  } catch (error) {
    console.error('Error handling chat interaction:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/bookOutline', async (req, res) => {
  try {
    const generator = new OutlineGenerator(process.env.OPENAI_API_KEY);
    await generator.generate();
    const outline = generator.outline;
    console.log(outline);
    const filePath = path.join(__dirname, 'BookOutlines', 'BookOutline.json');
    fs.writeFileSync(filePath, JSON.stringify(outline));
    
    res.json({ status: 'outline complete', outline: JSON.stringify(outline)});
  } catch (error) {
    console.error('Error generating book outline:', error);
    res.status(500).json({ error: 'Internal server error' });

  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
