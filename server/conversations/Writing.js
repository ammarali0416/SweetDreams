import OpenAI from 'openai';
import 'dotenv/config';
import { SystemMessage } from '../prompts/prompt_Writing.js';
import { generateSystemMessage } from '../prompts/prompt_Summarize.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

export class Author {
    constructor(apiKey) {
        this.OpenAI = new OpenAI({ apiKey });
        this.systemMessage = SystemMessage;
        this.chapters = [];
    }

    async sendChatCompletion(message) {
        return await this.OpenAI.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [
                { "role": "system", "content": this.systemMessage },
                { "role": "user", "content": message }
            ],
            temperature: 1,
            max_tokens: 4096,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0,
            response_format: { "type": "json_object" }
        });
    }
}

class Summarizer {
    constructor(apiKey) {
        this.OpenAI = new OpenAI({ apiKey });
    }

    async sendChatCompletion(chapter) {
        let systemMessage = generateSystemMessage(chapter);
        return await this.OpenAI.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: [
                { "role": "system", "content": systemMessage },
            ],
            temperature: 1,
            max_tokens: 4096,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0,
            response_format: { "type": "text" }
        });
    }
}

async function run() {
    let outline = JSON.parse(fs.readFileSync('./BookOutlines/BookOutline.json', 'utf8'));
    let plan = JSON.parse(fs.readFileSync('./BookPlans/BookPlan.json', 'utf8'));
    let priorSummaries = [];
    let author = new Author(process.env.OPENAI_API_KEY);
    let summarizer = new Summarizer(process.env.OPENAI_API_KEY);
    for (let i = 0; i < outline.length; i++) {
        console.log(`Now writing: Chapter ${i + 1}`)
        let message = JSON.stringify({"bookPlan" : plan["bookPlan"], "chatperOutline": outline[i], "priorSummaries": JSON.stringify(priorSummaries)});
        console.log(`Chapter ${i + 1} message: ${message}`)
        let response = await author.sendChatCompletion(message);
        author.chapters.push(JSON.parse(response.choices[0].message.content));
        let summary = await summarizer.sendChatCompletion(response.choices[0].message.content);
        console.log(`Chapter ${i + 1} Summary: ${summary.choices[0].message.content}`);
        let summarykey = `Chapter ${i + 1}`;
        priorSummaries.push({[summarykey] : summary.choices[0].message.content});
    //console.log(response.choices[0].message.content);
    //console.log(summary.choices[0].message.content);
    }
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);

    let filePath = './Book/Book.json';
    fs.writeFileSync(filePath, JSON.stringify(author.chapters));
}

run();