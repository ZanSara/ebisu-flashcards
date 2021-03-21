import EbisuParameters from "./EbisuParameters.svelte";
import RandomParameters from "./RandomParameters.svelte";
import AnkiParameters from "./AnkiParameters.svelte";
import type { SvelteComponent } from "svelte";

export interface AlgorithmDetail {
  name: string;
  component: SvelteComponent;
}

export const parameterDetails: AlgorithmDetail[] = [
  {
    name: "Ebisu",
    component: EbisuParameters,
  },
  {
    name: "Anki",
    component: AnkiParameters,
  },
  {
    name: "Random",
    component: RandomParameters,
  },
];
