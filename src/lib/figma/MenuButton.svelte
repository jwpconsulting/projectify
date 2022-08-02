<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import type { MenuButtonState } from "$lib/figma/types";
    export let label: string;
    export let icon: IconSource;
    export let state: MenuButtonState;

    $: style = {
        normal: "hover:bg-secondary active:bg-secondary active:text-base-100",
        selected: "bg-primary-hover text-base-100",
        accordion: "bg-base-200 text-base-content",
    }[state];

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class={`flex-start flex flex-row items-center gap-2 px-4 py-3 text-xs font-bold focus:bg-base-300 focus:text-base-content focus:outline-none ${style}`}
>
    <Icon src={icon} theme="outline" class="h-4 w-4" />
    <div class="first-letter:uppercase">
        {label}
    </div>
</button>
