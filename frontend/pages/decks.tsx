import Deck from "../components/Deck";
import { DeckModel } from "../lib/models/deck";
import { useEffect } from "react";
import { NextPage } from "next";
import PageCard, { Breadcrumb } from "../components/page/PageCard";
import LinkButton from "../components/inputs/buttons/LinkButton";

function generateModel(id: number): DeckModel {
  const nameRand = Math.floor(Math.random() * 3 + 1);
  const name: string = Array.from({ length: nameRand }, () => `Deck ${id}`).join(" - ");

  const tagRand = Math.floor(Math.random() * 10 + 1);
  const tags: string[] = Array.from({ length: tagRand }, () => "hello");

  return {
    id: id,
    name: name,
    description: `This is the description for Deck ${id}`,
    tags: tags,
  };
}

// let testData: DeckModel[] = [
//     {id: 1, name: "Deck 1", description: "This is the description for Deck 1", tags: ["hello?", "hello?", "hello?", "hello?", "hello?", "hello?", "hello?"]},
//     {id: 2, name: "Deck 2", description: "This is the description for Deck 2", tags: ["hello?"]},
//     {id: 3, name: "Deck 3", description: "This is the description for Deck 3", tags: ["hello?"]},
//     {id: 4, name: "Deck 4", description: "This is the description for Deck 4", tags: ["hello?"]},
// ];

const testData: DeckModel[] = Array.from({ length: 50 }, (v, k) => generateModel(k));

const DecksPage: NextPage = () => {
  useEffect(() => {
    document.querySelector("body")?.classList.add("bg-indigo-200");
  });

  const buttons = [
    <LinkButton color="green" title="New Deck" href="/deck/new" />,
    <LinkButton color="red" title="Logout" href="/logout" />,
  ];

  const breadcrumbs: Breadcrumb[] = [{ name: "DECKS" }];

  return (
    <PageCard className="flex-grow flex flex-col" headerButtons={buttons} breadcrumbs={breadcrumbs}>
      <main className="flex-grow grid items-stretch lg:grid-cols-4 md:grid-cols-2 sm:grid-cols-1 auto-rows-max gap-8 p-8 bg-white">
        {testData.map((deckModel) => (
          <Deck key={deckModel.id} deck={deckModel} />
        ))}
      </main>
    </PageCard>
  );
};

export default DecksPage;
