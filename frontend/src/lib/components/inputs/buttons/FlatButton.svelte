<script lang="ts">
    export let color;
    export let inprogress;
</script>

<button on:click
        class="leading-10 
            font-bold text-gray-800 
            bg-{color}-300 hover:bg-{color}-400 
            transition-colors 
            w-full"
        class:barberpole={inprogress}
>
    <slot />
</button>