import { useRouter } from "next/router";
import { NextPage } from "next";
import PageCard, { Breadcrumb } from "../../../components/PageCard";
import { useEffect, useState } from "react";
import { CardModel } from "../../../lib/models/deck";
import { getCards } from "../../../lib/api";
import Loading from "../../../components/Loading";
import DeckCard from "../../../components/DeckCard";

function renderLoading() {
  return (
    <div className="flex-grow flex flex-col justify-center">
      <Loading message="Loading cards..." />
    </div>
  );
}

function renderCards(cards: CardModel[]) {
  return (
    <main className="flex-grow grid items-stretch lg:grid-cols-4 md:grid-cols-2 sm:grid-cols-1 auto-rows-max gap-8 p-8 bg-white">
      {cards.map((card) => (
        <DeckCard key={card.id} card={card} />
      ))}
    </main>
  );
}

const DeckCardsPage: NextPage = () => {
  useEffect(() => {
    document.querySelector("body")?.classList.add("bg-indigo-200");
  });

  const router = useRouter();
  const { id } = router.query;

  const [cards, setCards] = useState<CardModel[] | null>(null);
  useEffect(() => {
    if (typeof id === "string") {
      getCards(id).then(setCards);
    }
  }, [id]);

  const breadcrumbs: Breadcrumb[] = [{ name: "DECKS", href: "/decks" }, { name: "TEST_DECK" }, { name: "CARDS" }];

  return (
    <PageCard className="flex-grow flex flex-col bg-white" breadcrumbs={breadcrumbs}>
      {cards === null ? renderLoading() : renderCards(cards)}
    </PageCard>
  );
};

export default DeckCardsPage;
