<script context="module" lang="ts">
    import { getDeck } from "../../../lib/api";

    export async function load({ page }) {
        const { id } = page.params;
        const deck = await getDeck(id);

        return {
            props: {
                deck
            }
        };
    }
</script>

<script lang="ts">
    import Page from "../../../lib/components/Page.svelte";
    import Loading from "../../../lib/components/utility/Loading.svelte";
    import { getNextCard } from "../../../lib/api";
    import type { DeckModel } from "../../../lib/models/deck";

    export let deck: DeckModel;
    let hidden = true;

    let card = getNextCard(deck?.id, null);

    function handleAnswer(remembered: boolean): void {
        hidden = true;
        card = getNextCard("0", "0");
    }
</script>

<Page>
    <!-- Breadcrumbs content -->
    <div slot="breadcrumbs" class="breadcrumbs">
        <a class="underline text-gray-600" href="/decks">DECKS</a>
        <span>&gt;</span>
        <span>{deck.name}</span>
    </div>
    <!-- Main content -->
    <main class="flex-grow flex flex-col md:justify-center text-center items-stretch w-full">
        {#await card}
            <Loading>Loading next card</Loading>
        {:then card}
            <div class="flex-grow flex flex-col items-center">
                <div class="flex-grow flex flex-col justify-center pb-4 px-4 md:px-12">
                    <span class="block text-2xl">{card.question.content.toString()}</span>
                </div>
                <div class="flex-grow flex flex-col justify-center px-4 md:px-12 transition-opacity"
                     class:hidden={hidden}>
                    <span class="block text-2xl">{card.answer.content.toString()}</span>
                </div>
            </div>

            {#if hidden}
                <button on:click={() => hidden = false}
                        class="leading-10 font-medium text-gray-800 bg-green-300 hover:bg-green-400 transition-colors w-full">
                    SHOW ANSWER
                </button>
            {:else}
                <div class="flex">
                    <button on:click={() => handleAnswer(true)}
                            class="leading-10 font-medium text-gray-800 bg-green-300 hover:bg-green-400 transition-colors w-1/2">
                        REMEMBERED
                    </button>
                    <button on:click={() => handleAnswer(false)}
                            class="leading-10 font-medium text-gray-800 bg-red-300 hover:bg-red-400 transition-colors w-1/2">
                        FORGOT
                    </button>
                </div>
            {/if}
        {/await}
    </main>
</Page>