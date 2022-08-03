<script lang="ts">
    import AvatarV3 from "$lib/figma/AvatarV3.svelte";
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
    <AvatarV3 {user} />
</button>
