<script lang="ts">
  import { getDecks } from "../lib/api";
  import Deck from "../lib/components/Deck.svelte";
  import RoundButton from "../lib/components/inputs/buttons/RoundButton.svelte";
  import Page from "../lib/components/Page.svelte";
  import Loading from "../lib/components/utility/Loading.svelte";
</script>

<svelte:head>
  <title>Ebisu - Decks</title>
</svelte:head>

<Page>
  <!-- Breadcrumb slot -->
  <div slot="breadcrumbs" class="breadcrumbs">
    <span>DECKS</span>
  </div>

  <!-- Button slot -->
  <div slot="buttons" class="flex gap-4">
    <RoundButton href="/deck/new" color="indigo">New deck</RoundButton>
    <RoundButton href="/logout" color="red">Logout</RoundButton>
  </div>
  <!-- Main content -->
  <main class="flex-grow flex">
    {#await getDecks()}
      <div class="flex-grow flex flex-col justify-center">
        <Loading>Loading decks</Loading>
      </div>
    {:then decks}
      <div class="flex-grow grid items-stretch lg:grid-cols-4 md:grid-cols-2 sm:grid-cols-1 auto-rows-max gap-8 p-8">
        {#each decks as deck}
          <Deck deck={deck} />
        {/each}
      </div>
    {/await}
  </main>
</Page>