<script lang="ts">
    import { Check } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    export let checked: boolean;
    export let disabled: boolean;
    // TODO document what this is for
    export let contained: boolean;
    export let required = false;

    let outerStyle: string;
    $: {
        if (contained) {
            outerStyle =
                checked && !disabled
                    ? "bg-primary border-primary text-foreground group-hover:bg-primary-hover"
                    : disabled
                    ? ""
                    : "group-hover:bg-secondary-hover group-hover:border-foreground";
        } else {
            outerStyle =
                checked && !disabled
                    ? "bg-primary border-primary text-foreground hover:bg-primary-hover"
                    : disabled
                    ? ""
                    : "hover:bg-secondary-hover hover:border-foreground";
        }
    }
</script>

<!-- TODO improve -->
<div
    class={`relative m-0.5 h-4 w-4 rounded border border-secondary-hover ${outerStyle}`}
>
    {#if checked && !disabled}
        <Icon src={Check} class="absolute" theme="outline" />
    {/if}
    <input
        class="absolute -left-[3px] -top-[3px] h-5 w-5 appearance-none rounded-md border border-transparent focus:border-base-content focus:outline-none"
        type="checkbox"
        bind:checked
        {disabled}
        {required}
    />
</div>
