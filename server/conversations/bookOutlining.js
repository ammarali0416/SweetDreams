import OpenAI from 'openai';
import 'dotenv/config';
import { system_message } from "../prompts/prompt_BookOutlining.js";

class OutlineGenerator {
    constructor(apiKey, systemMessage) {
        this.openai = new OpenAI({ apiKey });
        this.systemMessage = systemMessage;
        this.msgArray = [
            { "role": "system", "content": systemMessage },
            { "role": "user", "content": "BEGIN" }
        ];
        this.outlineComplete = false;
    }

    async sendChatCompletion() {
        return await this.openai.chat.completions.create({
            model: "gpt-4",
            messages: this.msgArray,
            temperature: 1,
            max_tokens: 5000,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0,
        });
    }

    async generate(returnvals = false) {
        let response;
        while (!this.outlineComplete) {
            response = await this.sendChatCompletion();
            console.log(response.usage);
            this.msgArray.push(response.choices[0].message);

            if (response.choices[0].message.content.includes("<<OUTLINE COMPLETE>>")) {
                console.log("Outline complete");
                this.outlineComplete = true;
            } else {
                console.log("Outline not complete yet");
                this.msgArray.push({ "role": "user", "content": "NEXT" });
            }
        }

        if (returnvals) {
            return { msgArray: this.msgArray, usage: response.usage };
        }
    }

    getOutline() {
        // Filter messages where the role is "assistant" and map to get just the content
        const assistantMessagesContent = this.msgArray
            .filter(msg => msg.role === "assistant")
            .map(msg => msg.content);
        return assistantMessagesContent;
    }

}

async function run() {
    const generator = new OutlineGenerator(process.env.OPENAI_API_KEY, system_message);
    await generator.generate();
    const outline = generator.getOutline();
    console.log(type(outline));
}

run();
