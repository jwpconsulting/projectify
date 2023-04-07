<script lang="ts">
    import StepperVariant from "$lib/figma/buttons/StepperVariant.svelte";
    import { currentStep, gotoStep, numSteps } from "$lib/stores/onboarding";

    const steps = [...Array(numSteps).keys()];
</script>

<div class="flex flex-row">
    {#each steps as step}
        <StepperVariant
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
