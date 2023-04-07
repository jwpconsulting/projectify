<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Plus, X } from "@steeze-ui/heroicons";
    import type { FloatingActionButtonIcon } from "$lib/figma/types";

    export let action: () => void;

    export let icon: FloatingActionButtonIcon;
    export let disabled = false;

    let iconC: typeof Plus;
    $: iconC = {
        plus: Plus,
        close: X,
    }[icon];
</script>

<button
    class="group inline rounded-llg border border-transparent p-1 focus:border-border-focus focus:outline-none"
    {disabled}
    on:click={action}
    on:keydown={action}
>
    <div
        class="rounded-lg bg-primary px-7 py-2 text-primary-content shadow-context-menu group-hover:bg-primary-hover group-active:bg-primary-pressed group-disabled:bg-disabled group-disabled:text-disabled-primary-content"
    >
        <Icon src={iconC} class="w-6" theme="outline" />
    </div>
</button>
