
import OpenAI from 'openai';
import 'dotenv/config';

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

let thread_id = "thread_p00jVwUAZ9FD5NKSlPGU8aEf"

// Function to find the book plan from each message
const getBookPlan = async (thread_id) => {
    const messages = await openai.beta.threads.messages.list(thread_id);
    const assistantMessages = messages.data.filter(message => message.role === 'assistant');

    for (const message of assistantMessages) {
        const text = message.content[0].text.value;
        const startIndex = text.indexOf('{');
        const endIndex = text.lastIndexOf('}');

        if (startIndex !== -1 && endIndex !== -1) {
            const jsonString = text.substring(startIndex, endIndex + 1);

            try {
                const potentialBookPlan = JSON.parse(jsonString);
                if (potentialBookPlan.bookPlan && potentialBookPlan.bookPlan.title) {
                    return potentialBookPlan;
                }
            } catch (error) {
                console.error("Error parsing potential book plan JSON:", error);
            }
        }
    }

    console.log("No book plan found in the conversation.");
    return null;
};
  

  getBookPlan(thread_id).then((bookPlan) => {
    console.log(bookPlan);
  });