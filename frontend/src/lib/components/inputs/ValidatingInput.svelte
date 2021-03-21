<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export var id;

    let extraClasses = '';
    /**
     * Extra classes for the container
     */
    export { extraClasses as class };

    /**
     * Controls whenever the input is valid
     */
    export let valid = true;
    /**
     * Validation error message, only displayed when valid is false
     */
    export let validationError: string;
    export let placeholder: string;

    const dispatch = createEventDispatcher();
</script>

<div class="flex flex-col {extraClasses}">
    <input
        id={id}
        class="text-2xl border-b outline-none focus:border-indigo-800"
        class:border-red-800={!valid}
        placeholder={placeholder}
        on:input
    />
    <!--{validationError ? <span className="text-base animate-pulse text-red-500">{validationError}</span> : null}-->
    {#if !valid}
    <span class="text-base animate-pulse text-red-500">
      {validationError}
    </span>
    {/if}
</div>
