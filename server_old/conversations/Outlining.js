import OpenAI from 'openai';
import 'dotenv/config';
import { generateSystemMessage } from "../prompts/prompt_Outlining.js";


export class OutlineGenerator {
    
    constructor(apiKey) {
        this.openai = new OpenAI({ apiKey });
        this.systemMessage = generateSystemMessage("./BookPlans/BookPlan.json");;
        this.msgArray = [
            { "role": "system", "content": this.systemMessage },
            { "role": "user", "content": "BEGIN" }
        ];
        this.outline = [];
        this.outlineComplete = false;
    }

    async sendChatCompletion() {
        return await this.openai.chat.completions.create({
            model: "gpt-4-turbo-preview",
            messages: this.msgArray,
            temperature: 1,
            max_tokens: 4096,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0,
            response_format: { "type": "json_object" }
        });
    }

    async generate(returnvals = false) {
        let response;
        while (!this.outlineComplete) {
            response = await this.sendChatCompletion();
            console.log(response.usage);
            this.msgArray.push(response.choices[0].message);
            this.outline.push(JSON.parse(response.choices[0].message.content));

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

}

// async function run() {
//     const generator = new OutlineGenerator(process.env.OPENAI_API_KEY, SystemMessage);
//     await generator.generate();
//     const outline = generator.outline;
//     console.log(outline);
//     console.log(typeof outline);
//     console.log(JSON.stringify(outline, null, 2))
// }

// run();
