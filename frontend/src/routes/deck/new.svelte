<script lang="ts">

    import Page from "../../lib/components/Page.svelte";
    import ValidatingInput from "../../lib/components/inputs/ValidatingInput.svelte";
    import { parameterDetails } from "../../lib/components/form/algo";
    import Toggle from "../../lib/components/inputs/Toggle.svelte";
    import { SvelteComponent } from "svelte";
    import FlatButton from "../../lib/components/inputs/buttons/FlatButton.svelte";

    // Parameters ----------------------------------------------------------------

    // Form state ----------------------------------------------------------------

    let submitting = false;

    let nameIsValid = true;
    let deckName = "";
    let selectedAlgorithm: SvelteComponent;

    // Validation functions ------------------------------------------------------

    function validateDeckName(event: InputEvent) {
        deckName = (event.target as HTMLInputElement).value;
        nameIsValid = deckName !== null && deckName.length > 0;
    }

    function handleSubmit(event: InputEvent) {
        console.log("Submitting...");
        submitting = true;
    }
</script>

<Page small={true}>

    <!-- Breadcrumbs content -->
    <div slot="breadcrumbs" class="breadcrumbs">
        <a class="underline text-gray-600" href="/decks">DECKS</a>
        <span>&gt;</span>
        {#if deckName.length > 0}
            <span>{deckName}</span>
        {:else}
            <!-- FIXME: overflow-ellipsis does not work in here -->
            <span class="overflow-ellipsis">NEW DECK</span>
        {/if}
    </div>

    <!-- Main content -->
    <form on:submit|preventDefault class="flex-col-container">
        <div class="flex-col-container align-top px-6 py-4 gap-y-6">

            <!-- Deck name -->
            <div class="flex flex-col gap-y-2">
                <label class="flex items-center gap-4" for="deck-name">
                    <span class="font-medium text-xl">DECK NAME</span>
                    <hr class="flex-grow border-b" />
                </label>
                <ValidatingInput
                    id="deck-name"
                    placeholder="Give the deck a name!"
                    validationError="Name should not be empty"
                    valid={nameIsValid}
                    on:input={validateDeckName}
                />
            </div>

            <!-- Algorithm selector -->
            <div class="flex flex-col gap-y-2">
                <div class="flex items-center gap-4">
                    <span class="font-medium text-xl">ALGORITHMS</span>
                    <hr class="flex-grow border-b" />
                </div>
                <div class="flex items-stretch rounded-2xl shadow-sm overflow-hidden">
                    {#each parameterDetails as param}
                        <Toggle bind:selected={selectedAlgorithm} value={param.component}>
                            {param.name}
                        </Toggle>
                    {/each}
                </div>
            </div>

            <!-- Algorithm options -->
            <svelte:component this={selectedAlgorithm} />
        </div>

        <!-- Save button -->
        <FlatButton color="green"
                    on:click={handleSubmit}
                    inprogress={submitting}>
            {#if !submitting}
                CREATE NEW DECK
            {:else}
                SAVING DECK...
            {/if}
        </FlatButton>
    </form>
</Page>