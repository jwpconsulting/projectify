<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { CheckCircle } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { AvatarVariantContent } from "$lib/figma/types";
    import type { User } from "$lib/types/user";

    export let user: User | undefined;
    export let active: boolean;
    export let ariaLabel: string;

    let content: AvatarVariantContent;
    $: content = {
        kind: "single",
        user,
    };

    // TODO make select / deselect callback props instead Justus 2023-09-19
    const dispatch = createEventDispatcher();
    function click() {
        active = !active;
        if (active) {
            dispatch("select");
        } else {
            dispatch("deselect");
        }
    }
</script>

<button on:click={click} class="group relative text-primary">
    {#if active}
        <div
            class="absolute left-6 top-0 z-10 h-4 w-4 rounded-full border-2 border-base-TODO bg-primary"
        />
    {:else}
        <Icon
            src={CheckCircle}
            theme="outline"
            class="absolute left-6 top-0 z-10 h-4 w-4 rounded-full bg-base-TODO group-active:bg-primary group-active:text-base-TODO"
        />
    {/if}
    <div class="relative z-0 p-0.5">
        <AvatarVariant {content} size="medium" />
    </div>
    <div class="sr-only">
        {ariaLabel}
    </div>
</button>
