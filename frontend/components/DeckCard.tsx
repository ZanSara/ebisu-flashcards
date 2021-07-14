import { FunctionComponent } from "react";
import { CardModel } from "../lib/models/deck";

interface DeckCardViewProps {
  card: CardModel;
}

// FIXME: When title is too long, the text will overflow
const DeckCard: FunctionComponent<DeckCardViewProps> = (props) => {
  return (
    <div className="flex flex-col border border-gray-500 shadow-md rounded-xl overflow-hidden">
      <div className="flex-grow flex flex-col p-6">
        <div className="flex gap-x-4 justify-center">
          {props.card.answer.tags.map((tag) => (
            <span className="border border-gray-500 bg-gray-100 rounded p-2">{tag}</span>
          ))}
        </div>
        <div className="flex-grow flex flex-col justify-center">
          <span className="text-xl">{props.card.question.content}</span>
        </div>
        <hr className="border-dashed border-gray-500 mx-4 my-6" />
        <div className="flex flex-wrap gap-4 justify-center">
          {props.card.question.tags.map((tag) => (
            <span className="border border-gray-500 bg-gray-100 rounded p-2">{tag}</span>
          ))}
        </div>
        <div className="flex-grow flex flex-col justify-center gap-y-4">
          <span className="text-xl">{props.card.answer.content}</span>
        </div>
      </div>
      <button className="leading-10 text-center bg-indigo-400 hover:bg-indigo-500 transition-colors text-white font-bold">
        EDIT
      </button>
    </div>
  );
};

export default DeckCard;
