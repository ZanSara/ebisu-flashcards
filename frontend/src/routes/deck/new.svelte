<script lang="ts">

    import Page from "../../lib/components/Page.svelte";
    import ValidatingInput from "../../lib/components/inputs/ValidatingInput.svelte";
    import {parameterDetails} from "../../lib/components/page/deck/new/algos";
    import Toggle from "../../lib/components/inputs/Toggle.svelte";
    import {SvelteComponent} from "svelte";
    import FlatButton from "../../lib/components/inputs/buttons/FlatButton.svelte";
    import SectionHeader from "../../lib/components/utility/SectionHeader.svelte";

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
            <div class="flex flex-col gap-y-4">
                <SectionHeader class="font-bold text-xl">
                    DECK NAME
                </SectionHeader>
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
                <SectionHeader class="font-bold text-xl">
                    ALGORITHMS
                </SectionHeader>
                <div>
                    <p class="text-base text-gray-800">
                        Select your algorithm, which will select the new cards for you!
                    </p>
                    <p class="text-gray-500">
                        (Don't worry about this too much, you can edit it later!)
                    </p>
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
            <div class="flex-col-container">
                <svelte:component this={selectedAlgorithm}/>
            </div>
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