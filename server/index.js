const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.post('/chat', (req, res) => {
  const userMessage = req.body.message;
  console.log(`Received message: ${userMessage}`);
  // For now, we are responding with a fixed reply. Later, this will be replaced with OpenAI's response.
res.json({ reply: `The user said: "${userMessage}"` });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
