<script context="module" lang="ts">
    import {getDeck} from "../../../lib/api";

    export async function load({ page }) {
        const { id } = page.params;
        const deck = await getDeck(id);

        return {
            props: {
                deck,
            },
        };
    }
</script>

<script lang="ts">
    /*
    TODOS:
     - Table 
        - Single line
        - With edit button
     - Pagination buttons
     - Search bar
     */

    import {fade} from 'svelte/transition';

    import Page from "../../../lib/components/Page.svelte";
    import RoundLinkButton from "../../../lib/components/inputs/buttons/RoundLinkButton.svelte";
    import RoundPushButton from "../../../lib/components/inputs/buttons/RoundPushButton.svelte";
    import type {DeckModel} from "../../../lib/models/deck";
    import {getCards} from "../../../lib/api";
    import Loading from "../../../lib/components/utility/Loading.svelte";
    import FaIcon from "../../../lib/components/utility/FaIcon.svelte";
    import {faKeyboard} from "@fortawesome/free-solid-svg-icons";
    import Card from "../../../lib/components/page/deck/Card.svelte";

    let displayMode: 'grid' | 'table' = "table";

    export let deck: DeckModel;

    function handleAdd(event: InputEvent) {
        console.log("LOL");
    }

    function toggleDisplay(event: InputEvent) {
        console.log("Togging")
        displayMode = displayMode === 'grid' ? 'table' : 'grid';
    }
</script>

<svelte:window on:keydown={handleAdd} />

<Page>
    <!-- Breadcrumbs content -->
    <div slot="breadcrumbs" class="breadcrumbs">
        <a class="underline text-gray-600" href="/decks">DECKS</a>
        <span>&gt;</span>
        <span>{deck.name}</span>
        <span>&gt;</span>
        <span>CARDS</span>
    </div>

    <!-- Button slot -->
    <div slot="buttons" class="grid grid-cols-2 gap-x-2 gap-y-3">
            <!-- Add card button -->
            <RoundLinkButton color="green" href="card/new">
                <span>Add new card</span>
                <span class="hidden md:inline">
                    ('a' on <FaIcon class="inline" icon={faKeyboard} size="1em" />)
                </span>
            </RoundLinkButton>
            
            <!-- Deck settings button -->
            <RoundLinkButton href="/deck/{deck.id}/edit" color="indigo">
                <span>Deck settings</span>
            </RoundLinkButton>
            
            <!-- Table / Grid button -->
            <RoundPushButton color="green" class="col-span-2" on:click={toggleDisplay}>
                <span>
                    Display as { displayMode === 'table' ? 'grid' : 'table' }
                </span>
            </RoundPushButton>
    </div>

    <main class="flex-col-container justify-center text-center items-stretch w-full">
        {#await getCards(deck.id)}
            <Loading>Loading cards</Loading>
        {:then cards}
            {#if displayMode === 'table'}
                <table class="flex-grow w-full table-auto">
                    <thead>
                    <tr class="bg-gray-200 border-b border-gray-300">
                        <th class="py-2 px-4 text-right">Question</th>
                        <th class="py-2 px-4 text-left">Answer</th>
                    </tr>
                    </thead>
                    <tbody>
                    {#each cards as card}
                        <tr class="odd:bg-gray-50 hover:bg-indigo-100 cursor-pointer">
                            <td class="text-right py-2 px-4">
                                <p>{card.question.content}</p>
                                <div class="mt-2">
                                    {#each card.question.tags as tag}
                                        <span class="w-min p-1 m-1 border border-gray-800 border-dashed">{tag}</span>
                                    {/each}
                                </div>
                            </td>
                            <td class="text-left py-4 px-4">
                                <p>{card.answer.content}</p>
                                <div class="mt-2">
                                    {#each card.answer.tags as tag}
                                        <span class="w-min p-1 m-1 border border-gray-800 border-dashed">{tag}</span>
                                    {/each}
                                </div>
                            </td>
                        </tr>
                    {/each}
                    </tbody>
                </table>
            {:else}
                <div
                    class="flex-grow grid items-stretch gap-8
                lg:grid-cols-4 md:grid-cols-2 sm:grid-cols-1 auto-rows-max 
                p-8"
                >
                    {#each cards as card}
                        <Card {card} />
                    {/each}
                </div>
            {/if}
        {/await}
    </main>
</Page>
