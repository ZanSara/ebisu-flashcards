import { NextPage, NextPageContext } from "next";
import { useEffect, useState } from "react";
import { DeckCard, DeckModel } from "../../../lib/models/deck";
import PageCard, { Breadcrumb } from "../../../components/page/PageCard";
import Card from "../../../components/Card";
import Selector, { SelectorOption } from "../../../components/inputs/Selector";
import { faFish } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { getNextCard } from "../../../lib/api";

interface StudyProps {
  deck: DeckModel;
}

const onRecallAnswer = (anwer: string) => {
  console.log(anwer);
};

const loadingComponent = () => {
  return (
    <div className="flex flex-col items-center">
      <FontAwesomeIcon icon={faFish} size="3x" color="gray" className="animate-swim" />
      <span className="text-2xl">Loading next card...</span>
    </div>
  );
};

const cardComponent = (card: DeckCard, p: () => void) => {
  const buttons: SelectorOption[] = [
    { name: "Yes", color: "green" },
    { name: "No", color: "red" },
  ];

  return (
    <Card className="flex flex-col items-center border border-gray-500 md:w-1/3 m-4 p-8">
      <span className="text-4xl">A</span>
      <div className="border-b border-dashed border-gray-500 w-full my-4" />
      <span className="text-2xl">Did you recall your answer?</span>
      <Selector className="w-full mt-4 text-2xl" options={buttons} onChange={p} />
    </Card>
  );
};

const StudyDeckPage: NextPage<StudyProps> = (props) => {
  useEffect(() => {
    document.querySelector("body")?.classList.add("bg-indigo-200");
  });

  const breadcrumbs: Breadcrumb[] = [{ name: "DECKS", href: "/decks" }, { name: props.deck?.name || "TEST DECK" }];

  const [card, setCard] = useState<DeckCard | null>(null);
  useEffect(() => {
    if (card === null) {
      getNextCard().then((c) => {
        setCard(c);
        console.log(c);
      });
    }
  }, [card]);

  return (
    <PageCard className="flex-grow flex flex-col bg-white" breadcrumbs={breadcrumbs}>
      <main className="flex-grow flex flex-col items-center justify-center">
        {card === null ? loadingComponent() : cardComponent(card, () => setCard(null))}
      </main>
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
