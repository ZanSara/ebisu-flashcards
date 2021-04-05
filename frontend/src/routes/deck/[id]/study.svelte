<script context="module" lang="ts">
    import { getDeck } from "../../../lib/api";

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
    import Page from "../../../lib/components/Page.svelte";
    import Loading from "../../../lib/components/utility/Loading.svelte";
    import {getNextCard} from "../../../lib/api";
    import type {DeckModel} from "../../../lib/models/deck";
    import FlatButton from "../../../lib/components/inputs/buttons/FlatButton.svelte";
    import LinkButton from "../../../lib/components/inputs/buttons/LinkButton.svelte";
    import FaIcon from "../../../lib/components/utility/FaIcon.svelte";
    import {faLayerGroup, faStickyNote} from "@fortawesome/free-solid-svg-icons";

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

    <!-- Button slot -->
    <div slot="buttons" class="flex gap-4">
        <LinkButton href="/deck/edit" color="indigo">
            <FaIcon slot="icon" icon={faStickyNote} size="1.25rem" />
            <span>Edit card</span>
        </LinkButton>
        <LinkButton href="/deck/edit" color="indigo">
            <FaIcon slot="icon" icon={faLayerGroup} size="1.25rem" />
            <span>Edit deck</span>
        </LinkButton>
    </div>

    <!-- Main content -->
    <main
        class="flex-col-container justify-center text-center items-stretch w-full"
    >
        {#await card}
            <Loading>Loading next card</Loading>
        {:then card}
            <div class="flex-col-container justify-center gap-y-8">
                <!-- FIXME: Division looks like, if the top part would be taller then the botton, as the header is white -->
                <!-- Question part -->
                <span class="text-2xl">
                    {card.question.content.toString()}
                </span>
                <div class="flex flex-row w-full justify-center gap-2">
                    {#each card.question.tags as tag}
                        <span
                            class="bg-gray-100 border border-gray-300 px-2 py-1 rounded"
                            >{tag}</span
                        >
                    {/each}
                </div>

                <!-- Divider -->
                <hr class="self-stretch border-b border-dashed mx-8" />

                <!-- Answer part -->
                <span
                    class="text-2xl transition-opacity"
                    class:opacity-0={hidden}
                >
                    {card.answer.content.toString()}
                </span>
                <div
                    class="flex flex-row w-full justify-center gap-2 transition-opacity"
                    class:opacity-0={hidden}
                >
                    {#each card.answer.tags as tag}
                        <span
                            class="bg-gray-100 border border-gray-300 px-2 py-1 rounded"
                            >{tag}</span
                        >
                    {/each}
                </div>
            </div>

            {#if hidden}
                <FlatButton color="green" on:click={() => (hidden = false)}>
                    SHOW ANSWER
                </FlatButton>
            {:else}
                <div class="flex">
                    <FlatButton
                        color="green"
                        on:click={() => handleAnswer(true)}
                    >
                        REMEMBERED
                    </FlatButton>
                    <FlatButton
                        color="red"
                        on:click={() => handleAnswer(false)}
                    >
                        FORGOT
                    </FlatButton>
                </div>
            {/if}
        {/await}
    </main>
</Page>
