import { NextPage, NextPageContext } from "next";
import { useEffect, useState } from "react";
import { DeckCard, DeckModel } from "../../../lib/models/deck";
import PageCard, { Breadcrumb } from "../../../components/PageCard";
import { faFish } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { getNextCard } from "../../../lib/api";

export interface StudyProps {
  deck: DeckModel;
}

enum CardState {
  UNINITIALIZED,
  LOADING,
  HIDDEN,
  REVEALED,
  ANSWERED_OK,
  ANSWERED_NOK,
}

/**
 * Function responsible rendering the inner loading screen
 */
const renderLoading = () => {
  return (
    <div className="flex flex-col items-center">
      {/* Let's take this fish out for a swimming */}
      <FontAwesomeIcon icon={faFish} size="3x" color="gray" className="animate-swim" />
      <span className="text-2xl">Loading next card...</span>
    </div>
  );
};

/**
 * Function responsible rendering the current card
 */
const renderCard = (card: DeckCard, state: CardState, setState: (state: CardState) => void) => {
  /**
   * Inner function responsible for rendering the buttons, depending on the current state
   */
  const renderButtons = () => {
    switch (state) {
      case CardState.HIDDEN:
        return (
          <button
            className="leading-10 font-bold bg-green-300 hover:bg-green-400 transition-colors w-full"
            onClick={() => setState(CardState.REVEALED)}
          >
            SHOW ANSWER
          </button>
        );
      case CardState.REVEALED:
        return (
          <>
            <button
              key="answer-ok"
              className="leading-10 font-bold bg-green-300 hover:bg-green-400 transition-colors w-1/2"
              onClick={() => setState(CardState.ANSWERED_OK)}
            >
              REMEMBERED
            </button>
            <button
              key="answer-nok"
              className="leading-10 font-bold bg-red-300 hover:bg-red-400 transition-colors w-1/2"
              onClick={() => setState(CardState.ANSWERED_NOK)}
            >
              FORGOT
            </button>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <main className="flex-grow flex flex-col md:justify-center text-center items-stretch w-full">
      <div className="flex-grow flex flex-col p-6">
        <div className="flex gap-x-4 justify-center">
          {card.answer.tags.map((tag) => (
            <span className="border border-gray-500 bg-gray-100 rounded p-2">{tag}</span>
          ))}
        </div>
        <div className="flex-grow flex flex-col justify-center">
          <span className="text-4xl">{card.question.content}</span>
        </div>
        <hr className="border-dashed border-gray-500 mx-4 my-6" />
        <div className="flex gap-x-4 justify-center">
          {card.question.tags.map((tag) => (
            <span className="border border-gray-500 bg-gray-100 rounded p-2">{tag}</span>
          ))}
        </div>
        <div className="flex-grow flex flex-col justify-center gap-y-4">
          <span className={`transition-opacity text-4xl ${state === CardState.HIDDEN ? "opacity-0" : ""}`}>
            {card.answer.content}
          </span>
        </div>
      </div>

      <div className="flex">{renderButtons()}</div>
    </main>
  );
};

const StudyDeckPage: NextPage<StudyProps> = (props) => {
  const breadcrumbs: Breadcrumb[] = [{ name: "DECKS", href: "/decks" }, { name: props.deck?.name || "TEST DECK" }];

  useEffect(() => {
    document.querySelector("body")?.classList.add("bg-indigo-200");
  });

  const [card, setCard] = useState<DeckCard | null>(null);
  const [state, setState] = useState(CardState.UNINITIALIZED);

  useEffect(() => {
    switch (state) {
      case CardState.ANSWERED_OK:
      case CardState.ANSWERED_NOK:
      case CardState.UNINITIALIZED:
        setState(CardState.LOADING);
        getNextCard().then((c) => {
          setState(CardState.HIDDEN);
          setCard(c);
        });
        return;
    }
  }, [state]);

  return (
    <PageCard className="flex-grow flex flex-col bg-white" breadcrumbs={breadcrumbs}>
      <div className="flex-grow flex flex-col sm:items-stretch md:items-center justify-center">
        {state === CardState.LOADING ? renderLoading() : card === null ? null : renderCard(card, state, setState)}
      </div>
    </PageCard>
  );
};

export async function getServerSideProps(context: NextPageContext) {
  return {
    props: {
      id: context.query.id,
    }, // will be passed to the page component as props
  };
}

export default StudyDeckPage;
