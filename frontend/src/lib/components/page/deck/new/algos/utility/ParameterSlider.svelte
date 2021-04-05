<script lang="ts">
    import SectionHeader from "../../../../../utility/SectionHeader.svelte";
    export let id: string;
    export let name: string;
    export let unit: string;
    
    export let min: number;
    export let max: number;
    export let step: number;
    export let value: number;
</script>

<div class="flex-col-container gap-y-2">
    <label for={id}>
        <SectionHeader class="text-xl">{name} &rightarrow; {value}{unit ? unit : ''}</SectionHeader>
    </label>
    <input id={id}
           class="flex-grow"
           type="range"
           min={min}
           max={max}
           step={step}
           bind:value={value}>
</div>