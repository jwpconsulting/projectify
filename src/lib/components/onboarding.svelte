<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let hasContentPadding = false;

    export let title = null;
    export let prompt = null;
    export let nextBtnLabel = null;
    export let nextBtnDisabled = false;
    export let viewBackButton = false;
    export let nextMessage = null;

    export let stepCount = 0;
    export let step = null;

    $: steps = Array(stepCount)
        .fill({})
        .map((it, inx) => inx + 1);

    const dispatch = createEventDispatcher();
</script>

<div class="flex w-[600px] flex-col gap-16 px-12 py-20 pb-8">
    <!-- Message -->
    <div class="flex flex-col gap-4">
        {#if title}
            <h1 class="text-4xl font-bold">{title}</h1>
        {/if}
        <div class="text-block text-lg">
            {#if prompt}
                {prompt}
            {:else}
                <slot name="prompt" />
            {/if}
        </div>
    </div>

    <!-- Inputs -->
    {#if $$slots["inputs"]}
        <div class="flex flex-col">
            <slot name="inputs" />
        </div>
    {/if}

    <!-- Navigation buttons -->
    <div class="flex flex-col gap-2">
        <div class="flex gap-2">
            {#if viewBackButton}
                <button
                    class="btn btn-ghost"
                    disabled={nextBtnDisabled}
                    on:click={() => dispatch("back")}>{"Back"}</button
                >
            {/if}
            <button
                class="btn btn-primary"
                disabled={nextBtnDisabled}
                on:click={() => dispatch("next")}
                >{nextBtnLabel || "Continue"}</button
            >
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
                {#each steps as s, inx}
                    <li class:step-primary={inx < step} class="step" />
                {/each}
            </ul>
        </div>
    {/if}
</div>

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
