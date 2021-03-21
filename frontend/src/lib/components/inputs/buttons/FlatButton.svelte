<script lang="ts">
    export let color;
    export let inprogress;
</script>

<button on:click
        class="leading-10 font-bold text-gray-800 bg-{color}-400 hover:bg-{color}-500 transition-colors w-full"
        class:barberpole={inprogress}
>
    <slot />
</button>