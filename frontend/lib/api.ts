import { DeckCard } from "./models/deck";

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
  return {
    question: "A",
    answer: "B",
  };
}
