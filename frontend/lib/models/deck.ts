export interface DeckModel {
  id: number;
  name: string;
  description: string;
  tags: string[];
}

export interface DeckCard {
  question: string;
  answer: string;
}
