import Deck from "../components/Deck";
import { DeckModel } from "../lib/models/deck";
import { useEffect, useState } from "react";
import { NextPage } from "next";
import PageCard, { Breadcrumb } from "../components/PageCard";
import LinkButton from "../components/inputs/buttons/LinkButton";
import Loading from "../components/Loading";
import { getDecks } from "../lib/api";

function renderLoading() {
  return (
    <div className="flex-grow flex flex-col justify-center">
      <Loading message="Loading decks..." />
    </div>
  );
}

function renderDecks(decks: DeckModel[]) {
  return (
    <main className="flex-grow grid items-stretch lg:grid-cols-4 md:grid-cols-2 sm:grid-cols-1 auto-rows-max gap-8 p-8 bg-white">
      {decks.map((deck) => (
        <Deck key={deck.id} deck={deck} />
      ))}
    </main>
  );
}

const DecksPage: NextPage = () => {
  useEffect(() => {
    document.querySelector("body")?.classList.add("bg-indigo-200");
  });

  const [decks, setDecks] = useState<DeckModel[] | null>(null);
  useEffect(() => {
    if (decks === null) {
      getDecks().then(setDecks);
    }
  }, [decks]);

  const buttons = [
    <LinkButton color="green" title="New Deck" href="/deck/new" />,
    <LinkButton color="red" title="Logout" href="/logout" />,
  ];

  const breadcrumbs: Breadcrumb[] = [{ name: "DECKS" }];

  return (
    <PageCard className="flex-grow flex flex-col bg-white" headerButtons={buttons} breadcrumbs={breadcrumbs}>
      {decks === null ? renderLoading() : renderDecks(decks)}
    </PageCard>
  );
};

export default DecksPage;
