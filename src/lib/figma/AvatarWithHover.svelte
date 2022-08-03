<script lang="ts">
    import Avatar from "$lib/figma/Avatar.svelte";
    import { createEventDispatcher } from "svelte";
    import type { User } from "$lib/types";

    export let user: User | null;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="rounded-lg border border-transparent p-1.5 hover:bg-secondary-hover focus:border-base-content focus:outline-none"
>
    <Avatar {user} />
</button>
