import { FunctionComponent } from "react";
import { DeckModel } from "../lib/models";

import { faEdit, faList } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface DeckProps {
  deck: DeckModel;
}

// FIXME: When title is too long, the text will overflow
const Deck: FunctionComponent<DeckProps> = (props) => {
  return (
    <div className="flex flex-col border border-gray-500 shadow-md rounded-xl overflow-hidden">
      <main className="flex-grow flex flex-col gap-4 p-4">
        <header className="flex items-center justify-between border-b border-dashed border-gray-800 pb-2 max-w-full">
          <h1 className="uppercase text-2xl font-medium">{props.deck.name}</h1>
          <div className="flex gap-4">
            {/* TODO: Add tooltips */}
            <a href={`/deck/${props.deck.id}/cards`}>
              <FontAwesomeIcon icon={faList} />
            </a>
            <a href={`/deck/${props.deck.id}/edit`}>
              <FontAwesomeIcon icon={faEdit} />
            </a>
          </div>
        </header>
        <div className="flex-grow">
          Some content I guess Some content I guess Some content I guess Some content I guess
        </div>
        <div className="flex flex-wrap gap-2">
          {props.deck.tags.map((tag) => (
            <span key={tag} className="border border-dashed border-gray-800 px-4 py-1">
              {tag}
            </span>
          ))}
        </div>
      </main>
      <a
        className="leading-10 text-center bg-indigo-400 hover:bg-indigo-500 transition-colors text-white font-bold"
        href={`deck/${props.deck.id}/study`}
      >
        STUDY
      </a>
    </div>
  );
};

export default Deck;
