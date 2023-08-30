<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import type { ButtonAction } from "$lib/funabashi/types";

    export let hasContentPadding = false;

    // TODO make required
    export let title: string | null = null;
    // TODO make required or swap for slot
    export let prompt: string | null = null;
    // TODO make not optional
    export let backAction: (() => void) | undefined = undefined;
    export let nextAction: ButtonAction = { kind: "a", href: "/" };
    export let nextLabel: string = $_("onboarding.continue");
    // TODO rename nextActionDisabled
    export let nextBtnDisabled = false;
    export let nextMessage: string | null = null;

    export let stepCount = 0;
    export let step: number | null = null;

    $: steps = Array(stepCount)
        .fill({})
        .map((_, inx) => inx + 1);

    function submit() {
        if (nextBtnDisabled) {
            throw new Error("nextBtnDisabled");
        }
        if (nextAction.kind !== "button") {
            throw new Error("Expected nextAction.kind to be button");
        }
        if (nextAction.disabled ?? false) {
            throw new Error("Expected nextAction.disabled to not be true");
        }
        nextAction.action();
    }
</script>

<form
    class="flex w-[600px] flex-col gap-16 px-12 py-20 pb-8"
    on:submit|preventDefault={submit}
>
    <!-- Message -->
    <div class="flex flex-col gap-4">
        {#if title}
            <h1 class="text-4xl font-bold">{title}</h1>
        {/if}
        <div class="text-lg">
            {#if prompt}
                {prompt}
            {:else}
                <slot name="prompt" />
            {/if}
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
                    style={{ kind: "tertiary", icon: null }}
                    color="blue"
                    size="medium"
                    action={{
                        kind: "button",
                        action: backAction,
                        disabled: nextBtnDisabled,
                    }}
                    label={$_("onboarding.back")}
                />
            {/if}
            {#if nextAction.kind === "button"}
                <Button
                    style={{ kind: "primary" }}
                    color="blue"
                    size="medium"
                    action={{ kind: "submit", disabled: nextBtnDisabled }}
                    label={nextLabel}
                />
            {:else}
                <Button
                    style={{ kind: "primary" }}
                    color="blue"
                    size="medium"
                    action={nextAction}
                    label={nextLabel}
                />
            {/if}
        </div>
        {#if nextMessage}
            <div>
                {nextMessage}
            </div>
        {/if}
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
    class:p-12={hasContentPadding}
    class:py-20={hasContentPadding}
    class="flex grow flex-col gap-6 bg-base-200"
>
    {#if $$slots["content-title"]}
        <h1 class="text-4xl font-bold">
            <slot name="content-title" />
        </h1>
    {/if}
    <slot name="content" />
</div>
