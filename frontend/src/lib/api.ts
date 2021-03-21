import type { CardModel, DeckModel } from "./models/deck";
import { LoremIpsum } from "lorem-ipsum";

// ============================================================================
// PROTOTYPE UTILITIES
// ============================================================================

function wait(ms: number) {
  return new Promise((trigger) => setTimeout(trigger, ms));
}

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

const decks = Array.from({ length: 50 }, (v, k) => generateDeck(k));
const deckCards = Array.from({ length: decks.length }, () =>
  Array.from({ length: 50 }, (v, k) => generateCard(k))
);

function generateCard(id: number): CardModel {
  const questionTagNum = Math.floor(Math.random() * 5 + 1);
  const questionTags: string[] = Array.from({ length: questionTagNum }, () =>
    lorem.generateWords(1)
  );

  const answerTagNum = Math.floor(Math.random() * 5 + 1);
  const answerTags: string[] = Array.from({ length: answerTagNum }, () =>
    lorem.generateWords(1)
  );

  return {
    id: id,
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

function generateDeck(id: number): DeckModel {
  const nameLength = Math.floor(Math.random() * 5 + 1);

  const tagRand = Math.floor(Math.random() * 10 + 1);
  const tags: string[] = Array.from({ length: tagRand }, () => "hello");

  return {
    id: id.toString(),
    name: lorem.generateWords(nameLength),
    description: lorem.generateSentences(1),
    tags: tags,
  };
}

// ============================================================================
// API FUNCTIONS
// ============================================================================

export function login(username: string, password: string): Promise<Response> {
  return fetch("/api/login", {
    method: "POST",
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
}

export async function getDecks(): Promise<DeckModel[]> {
  await wait(1000);
  return decks;
}

export async function getDeck(deckId: string): Promise<DeckModel> {
  await wait(1000);

  const deckIdNum = parseInt(deckId);
  return decks[deckIdNum];
}

export async function getCards(deckId: string): Promise<CardModel[]> {
  await wait(1000);
  return deckCards[parseInt(deckId)];
}

export async function getNextCard(
  deckId: string,
  cardId?: string
): Promise<CardModel> {
  console.log("Getting next card!");
  await wait(1000);

  const deckIdNum = parseInt(deckId);

  const cards = deckCards[deckIdNum];

  if (cardId === null) {
    return cards[0];
  } else {
    const cardIdNum = parseInt(cardId);
    if (cardIdNum >= cards.length) {
      return cards[0];
    } else {
      return cards[cardIdNum];
    }
  }
}
