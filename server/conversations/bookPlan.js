import OpenAI from 'openai';
import 'dotenv/config';

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

let myThread = null;

export const ensureThreadExists = async () => {
    if (!myThread) {
        myThread = await openai.beta.threads.create();
        console.log(`Thread created with ID: ${myThread.id}`);
    }
};

// Async function to handle chat interaction
export const handleChatInteraction = async (userMessage) => {
    // Create a new thread for the interaction
    console.log(myThread.id)
    // Add user message to the thread
    await addUserMsg(myThread.id, userMessage);

    // Get bot's reply
    const botReply = await getBotReply(myThread.id);

    return botReply;
};

// Updated addUserMsg to include thread_id as parameter
const addUserMsg = async (thread_id, message) => {
    console.log(`Adding user message: ${message}`);
    const response = await openai.beta.threads.messages.create(thread_id, { role: 'user', content: message });
    console.log(response);
};

const getBotReply = async (thread_id) => {
    console.log('Creating run..');
    //console.log(process.env.ASSISTANT_ID)
    const myRun = await openai.beta.threads.runs.create(
        thread_id,
        { assistant_id: process.env.ASSISTANT_ID });

    console.log(`Run ID: ${myRun.id}`);

    let keepRetrievingRun;

    while (myRun.status === "queued" || myRun.status === "in_progress") {
        keepRetrievingRun = await openai.beta.threads.runs.retrieve(
            (thread_id),
            (myRun.id)
        );
        console.log(`Run status: ${keepRetrievingRun.status}`);

        if (keepRetrievingRun.status === "completed") {
            console.log("\n");

            // Step 6: Retrieve the Messages added by the Assistant to the Thread
            const allMessages = await openai.beta.threads.messages.list(
                (thread_id)
            );

            return allMessages.data[0].content[0].text.value;
        } else if (
            keepRetrievingRun.status === "queued" ||
            keepRetrievingRun.status === "in_progress"
        ) {
            // pass
        } else {
            console.log(`Run status: ${keepRetrievingRun.status}`);
            break;
        }
    }

}