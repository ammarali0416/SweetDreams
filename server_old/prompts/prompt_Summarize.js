export function generateSystemMessage(chapter) {
    const systemMessage = `Provide a brief summary highlighting only the main plot points and key character developments from the chapter provided. Avoid unnecessary phrases like "in this chapter" and refrain from analyzing the text.
${chapter}`
    return systemMessage;
}