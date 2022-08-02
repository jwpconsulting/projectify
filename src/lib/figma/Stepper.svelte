<script lang="ts">
    import StepperComponent from "$lib/figma/StepperComponent.svelte";
    import { firstStep, gotoStep, numSteps } from "$lib/stores/onboarding";

    const steps = [...Array(numSteps).keys()];
</script>

<div class="flex flex-row">
    {#each steps as step}
        <StepperComponent
            position={step === firstStep
                ? "first"
                : step === numSteps - 1
                ? "last"
                : "mid"}
            on:click={() => gotoStep(step)}
        />
    {/each}
</div>
