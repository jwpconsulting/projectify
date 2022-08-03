<script lang="ts">
    import StepperComponent from "$lib/figma/StepperComponent.svelte";
    import { gotoStep, numSteps, currentStep } from "$lib/stores/onboarding";

    const steps = [...Array(numSteps).keys()];
</script>

<div class="flex flex-row">
    {#each steps as step}
        <StepperComponent
            position={step === numSteps - 1 ? "last" : "not-last"}
            state={step > $currentStep
                ? "inactive"
                : step == $currentStep
                ? "this"
                : "next"}
            on:click={() => gotoStep(step)}
        />
    {/each}
</div>
