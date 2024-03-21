import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { ensureThreadExists, handleChatInteraction } from './conversations/bookPlan.js';

// To do
// 1. check for null thread_id and create a new thread if it is null to handle multiple sessions
// 2. integrate database support to store thread_id and user messages

const app = express();

const PORT = 3001;

app.use(cors({
    origin: 'http://localhost:3000',
    methods: "GET,HEAD,PUT,PATCH,POST,DELETE"
}   ));

app.use(express.json());


app.post('/chat', async (req, res) => {
    const userMessage = req.body.message;
    try {
      await ensureThreadExists();
      const botReply = await handleChatInteraction(userMessage);
      
      // Check if botReply contains the string
      const isSummaryComplete = JSON.stringify(botReply).includes('<status>Summary Complete</status>');

      // Add it to the response if detected
      res.json({ reply: botReply, summaryComplete: isSummaryComplete });
    } catch (error) {
      console.error('Error handling chat interaction:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
