<script lang="ts">
    import type {CardModel} from "../../../models/card";

    export let card: CardModel;
</script>

<div class="flex flex-col
        border border-gray-500 shadow-md rounded-xl overflow-hidden bg-white 
        hover:bg-indigo-50
        cursor-pointer
        transform transition-all hover:scale-105 hover:z-50">
    <div class="flex-grow flex flex-col justify-center gap-4 p-4">
        <div>
            {card.question.content}
        </div>
        <div class="flex flex-wrap justify-center gap-2">
            {#each card.question.tags as tag}
                <span class="border border-dashed border-gray-800 px-4 py-1">
                  {tag}
                </span>
            {/each}
        </div>
    </div>
    <hr class="w-full border border-dashed border-gray-400 box-border px-10" />
    <div class="flex-grow flex flex-col justify-center gap-4 p-4">
        <div>
            {card.answer.content}
        </div>
        <div class="flex flex-wrap justify-center gap-2">
            {#each card.answer.tags as tag}
                <span class="border border-dashed border-gray-800 px-4 py-1">
                  {tag}
                </span>
            {/each}
        </div>
    </div>
</div>