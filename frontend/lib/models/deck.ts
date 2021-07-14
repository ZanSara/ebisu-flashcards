import * as url from "url";

export interface DeckModel {
  id: number;
  name: string;
  description: string;
  tags: string[];
}

export interface CardModel {
  id: number;
  question: {
    type: "text" | "image";
    tags: string[];
    content: string;
  };
  answer: {
    type: "text" | "image";
    tags: string[];
    content: string;
  };
}
