<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { CheckCircle } from "@steeze-ui/heroicons";
    import type { User } from "$lib/types/user";
    import type { AvatarV5Content } from "$lib/figma/types";
    import AvatarV5 from "$lib/figma/navigation/AvatarV5.svelte";

    export let user: User | null;
    export let active: boolean;

    let content: AvatarV5Content;
    $: content = {
        kind: "multiple",
        users: [user],
    };

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
            class="absolute left-4 top-0 z-10 h-4 w-4 rounded-full border-2 border-base-TODO bg-primary group-hover:left-6"
        />
    {:else}
        <Icon
            src={CheckCircle}
            theme="outline"
            class="absolute left-4 top-0 z-10 h-4 w-4 rounded-full bg-base-TODO group-hover:left-6 group-active:bg-primary group-active:text-base-TODO"
        />
    {/if}
    <div class="relative z-0 p-0.5">
        <AvatarV5 {content} size="hoverable" />
    </div>
</button>
