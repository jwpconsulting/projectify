<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Adjustments, Briefcase } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

    import type { BorderedIconType } from "$lib/figma/types";

    export let type: BorderedIconType;
    export let ariaLabel: string;
    // TODO allow disabling

    $: src = {
        workspace: Briefcase,
        filter: Adjustments,
    }[type];

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
    // TODO add callback property and remote dispatch
</script>

<button
    on:click={click}
    class="group h-9 w-9 rounded-llg border border-transparent p-0.5 focus:border-base-content focus:outline-none"
>
    <div
        class="rounded-lg border border-border p-1 group-hover:bg-secondary-hover group-active:bg-primary group-active:text-base-100"
    >
        <Icon {src} theme="outline" />
    </div>
    <div class="sr-only">
        {ariaLabel}
    </div>
</button>
