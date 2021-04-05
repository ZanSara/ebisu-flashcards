<script lang="ts">
    import ParameterSlider from "./utility/ParameterSlider.svelte";
    import ExplanationBox from "./utility/ExplanationBox.svelte";

    let initialAlpha = 3.0;
    let initialBeta = 3.0;
    let initialTime = 3.0;
    let initialHalfLife = 30;
</script>

<div class="flex-col-container justify-start gap-y-6 px-4">
    <div class="flex flex-col gap-y-2">
        <ParameterSlider
            id="parameter-t"
            name="Initial half-life"
            min={10}
            max={3600}
            step={5}
            unit=" minutes"
            bind:value={initialHalfLife}
        />
        <ExplanationBox>
            <span slot="title">What is half-life?</span>
            <span slot="explanation">
                It's magical!
            </span>
        </ExplanationBox>
    </div>
    
    <!-- Parameter Alpha -->
    <div class="flex flex-col gap-y-2">
        <ParameterSlider
            id="parameter-alpha"
            name="Initial &alpha;"
            min={1.0}
            max={30.0}
            step={0.1}
            bind:value={initialAlpha}
        />
        <ExplanationBox>
            <span slot="title">What is &alpha;?</span>
            <span slot="explanation">
                It's magical!
            </span>
        </ExplanationBox>
    </div>

    <div class="flex flex-col gap-y-2">
        <ParameterSlider
            id="parameter-beta"
            name="Initial &beta;"
            min={1.0}
            max={30.0}
            step={0.1}
            bind:value={initialBeta}
        />
        <ExplanationBox>
            <span slot="title">What is &beta;?</span>
            <span slot="explanation">
                It's magical!
            </span>
        </ExplanationBox>
    </div>

    <div class="flex flex-col gap-y-2">
        <ParameterSlider
            id="parameter-t"
            name="Initial t"
            min={1.0}
            max={30.0}
            step={0.1}
            bind:value={initialTime}
        />
        <ExplanationBox>
            <span slot="title">What is initial t?</span>
            <span slot="explanation">
                It's magical!
            </span>
        </ExplanationBox>
    </div>
</div>