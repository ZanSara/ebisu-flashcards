<script lang="ts">
    import {getDecks} from "../lib/api";
    import Deck from "../lib/components/page/decks/Deck.svelte";
    import RoundLinkButton from "../lib/components/inputs/buttons/RoundLinkButton.svelte";
    import Page from "../lib/components/Page.svelte";
    import Loading from "../lib/components/utility/Loading.svelte";
    import FaIcon from "../lib/components/utility/FaIcon.svelte";
    import {faLayerGroup} from "@fortawesome/free-solid-svg-icons";
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
        <!-- New deck button -->
        <RoundLinkButton href="/deck/new" color="indigo">
            <FaIcon slot="icon" class="inline" icon={faLayerGroup} size="1rem" />
            <span>New deck</span>
        </RoundLinkButton>
        <!-- Logout button -->
        <RoundLinkButton href="/logout" color="red">
            <span>Logout</span>
        </RoundLinkButton>
    </div>
    <!-- Main content -->
    <main class="flex-grow flex">
        {#await getDecks()}
            <div class="flex-grow flex flex-col justify-center">
                <Loading>Loading decks</Loading>
            </div>
        {:then decks}
            <div
                class="flex-grow grid items-stretch gap-8
                lg:grid-cols-4 md:grid-cols-2 sm:grid-cols-1 auto-rows-max 
                py-4 px-8"
            >
                {#each decks as deck}
                    <Deck {deck} />
                {/each}
            </div>
        {/await}
    </main>
</Page>
