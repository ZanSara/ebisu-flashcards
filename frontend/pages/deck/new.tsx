import { NextPage } from "next";
import { FunctionComponent, useEffect, useState } from "react";
import Selector, { SelectorOption } from "../../components/inputs/Selector";
import ValidatingTextField from "../../components/inputs/ValidatingTextField";
import PageCard, { Breadcrumb } from "../../components/PageCard";
import EbisuForm from "../../components/forms/EbisuForm";
import TypeAForm from "../../components/forms/TypeAForm";

interface AlgorithmOptions extends SelectorOption {
  name: string;
  component: FunctionComponent;
}

const algorithmOptions: AlgorithmOptions[] = [
  {
    name: "EBISU",
    color: "indigo",
    component: EbisuForm,
  },
  {
    name: "Type A",
    color: "indigo",
    component: TypeAForm,
  },
];

const breadcrumbs: Breadcrumb[] = [
  {
    name: "DECKS",
    href: "/decks",
  },
  {
    name: "NEW",
  },
];

function typeSelectionChanged(selection: SelectorOption) {
  console.log(selection);
}

function validateDeckName(value: string): string | null {
  if (value.length > 0) {
    return null;
  } else {
    return "Deck name should not be empty";
  }
}

const NewDeckPage: NextPage = () => {
  useEffect(() => {
    document.querySelector("body")?.classList.add("bg-indigo-200");
  });

  const [algorithm, setAlgorithm] = useState<AlgorithmOptions>();

  return (
    <PageCard className="flex flex-col max-w-2xl" breadcrumbs={breadcrumbs}>
      <form className="flex-grow flex flex-col bg-white">
        <div className="p-8">
          <ValidatingTextField className="text-4xl w-full" placeholder="New deck name" validate={validateDeckName} />
          <Selector className="mt-4" options={algorithmOptions} onChange={setAlgorithm} />
        </div>

        {algorithm?.component({})}

        <button className="leading-10 font-bold bg-green-300 hover:bg-green-400 transition-colors">SAVE</button>
      </form>
    </PageCard>
  );
};

export default NewDeckPage;
