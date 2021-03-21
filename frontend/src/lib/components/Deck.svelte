<script lang="typescript">
    import type {DeckModel} from '../models/deck';

    export let deck: DeckModel;
</script>

<div class="flex flex-col border border-gray-500 shadow-md rounded-xl overflow-hidden">
    <main class="flex-grow flex flex-col gap-4 p-4">
        <header class="flex items-center justify-between border-b border-dashed border-gray-800 gap-4 pb-2 max-w-full">
            <h1 class="uppercase text-2xl font-medium truncate">{deck.name}</h1>
            <div class="flex gap-4">
                <!-- TODO: Add tooltips-->
                <a href="/deck/{deck.id}/cards">
                    Cards
                </a>
                <a href="/deck/{deck.id}/cards">
                    Edit
                </a>
            </div>
        </header>
        <div class="flex-grow">
            {deck.description}
        </div>
        <div class="flex flex-wrap gap-2">
            {#each deck.tags as tag}
                <span class="border border-dashed border-gray-800 px-4 py-1">
                  {tag}
                </span>
            {/each}
        </div>
    </main>
    <a class="leading-10 text-center bg-indigo-400 hover:bg-indigo-500 transition-colors text-white font-bold"
       href={`deck/${deck.id}/study`}>
        STUDY
    </a>
</div>