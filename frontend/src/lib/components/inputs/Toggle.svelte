<script lang="ts">
    export let selected: any;
    export let value: any;
    export let checked = false;
    
    $: updateRadio(selected, value);

    function updateRadio(selected, value) {
        checked = selected === value
    }
</script>

<label class="flex-grow text-center select-none cursor-pointer bg-indigo-200 py-2 transition-colors" 
       class:bg-indigo-500={checked}
       class:text-white={checked}>
    <input
        type="radio"
        class="hidden"
        on:click
        bind:group={selected}
        value={value}
    />
    <slot />
</label>