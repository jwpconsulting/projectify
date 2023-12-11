<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import type { ButtonAction } from "$lib/funabashi/types";

    // TODO make not optional
    export let backAction: ButtonAction | undefined = undefined;
    type NextAction =
        | (ButtonAction & { kind: "submit"; submit: () => void })
        | (ButtonAction & { kind: "a" })
        | (ButtonAction & { kind: "button" });
    export let nextAction: NextAction;

    $: submit = nextAction.kind === "submit" ? nextAction.submit : undefined;

    export let nextLabel: string = $_("onboarding.continue");

    export let stepCount = 0;
    export let step: number | null = null;

    $: steps = Array(stepCount)
        .fill({})
        .map((_, inx) => inx + 1);
</script>

<main class="flex grow flex-col md:grid md:grid-cols-2 xl:grid-cols-3">
    <form
        class="col-span-1 flex shrink grow flex-col gap-16 px-12 py-20 pb-8"
        on:submit|preventDefault={submit}
    >
        <!-- Message -->
        <div class="flex flex-col gap-4">
            <h1 class="min-w-fit max-w-lg text-4xl font-bold">
                <slot name="title" />
            </h1>
            <div class="flex flex-col gap-2 text-lg">
                <slot name="prompt" />
            </div>
        </div>

        <!-- Inputs -->
        {#if $$slots.inputs}
            <div class="flex flex-col">
                <slot name="inputs" />
            </div>
        {/if}

        <!-- Navigation buttons -->
        <div class="flex flex-col gap-2">
            <div class="flex gap-2">
                {#if backAction}
                    <Button
                        style={{ kind: "tertiary" }}
                        color="blue"
                        size="medium"
                        action={backAction}
                        label={$_("onboarding.back")}
                    />
                {/if}
                <Button
                    style={{ kind: "primary" }}
                    color="blue"
                    size="medium"
                    action={nextAction}
                    label={nextLabel}
                />
            </div>
        </div>

        <div class="grow" />

        {#if step && stepCount}
            <div class="flex justify-center">
                <ul class="steps steps-horizontal">
                    {#each steps as _, inx}
                        <li class:step-primary={inx < step} class="step" />
                    {/each}
                </ul>
            </div>
        {/if}
    </form>

    <div
        class="hidden h-full min-w-0 shrink grow flex-col items-center justify-center overflow-hidden bg-background md:flex xl:col-span-2"
    >
        <slot name="content" />
    </div>
</main>
