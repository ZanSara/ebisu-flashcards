import { DeckCard } from "./models/deck";
import { LoremIpsum } from "lorem-ipsum";

const lorem = new LoremIpsum({
  sentencesPerParagraph: {
    max: 8,
    min: 4,
  },
  wordsPerSentence: {
    max: 16,
    min: 4,
  },
});

export function login(username: string, password: string): Promise<Response> {
  return fetch("/api/login", {
    method: "POST",
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
}

export async function getNextCard(): Promise<DeckCard> {
  const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

  await wait(1000);

  const questionTagNum = Math.floor(Math.random() * 5 + 1);
  const questionTags: string[] = Array.from({ length: questionTagNum }, () => lorem.generateWords(1));

  const answerTagNum = Math.floor(Math.random() * 5 + 1);
  const answerTags: string[] = Array.from({ length: answerTagNum }, () => lorem.generateWords(1));

  return {
    question: {
      type: "text",
      tags: questionTags,
      content: lorem.generateSentences(1),
    },
    answer: {
      type: "text",
      tags: answerTags,
      content: lorem.generateSentences(1),
    },
  };
}
