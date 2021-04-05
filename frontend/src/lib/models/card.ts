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