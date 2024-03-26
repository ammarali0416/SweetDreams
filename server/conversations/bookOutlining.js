import { system_message } from "../prompts/prompt_BookOutlining.js";
import OpenAI from 'openai';
import 'dotenv/config';

let outlineComplete = false

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});


let msg_array = [
    { "role": "system", "content": system_message },
    { "role": "user", "content": "BEGIN" },
];

while (outlineComplete === false) {
    const response = await openai.chat.completions.create({
        model: "gpt-4",
        messages: msg_array,
        temperature: 1,
        max_tokens: 5000,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0,
    });
    console.log(response.usage)
    msg_array.push(response.choices[0].message)

    let assistant_msg = response.choices[0].message.content

    if (assistant_msg.includes("<<OUTLINE COMPLETE>>")) {
        console.log("Outline complete")
        outlineComplete = true;
    } else {
        console.log("Outline not complete yet")
        msg_array.push({ "role": "user", "content": "NEXT" });
    }
}

if (outlineComplete) {
    console.log('total tokens used: ', response.usage)
    for (let i = 1; i < msg_array.length; i++) {
        console.log(`role: ${msg_array[i].role} msg: ${msg_array[i].content}`)
    }
}