<script lang="ts">
    import AvatarV3 from "$lib/figma/navigation/AvatarV3.svelte";
    import { createEventDispatcher } from "svelte";
    import type { User } from "$lib/types/user";

    export let user: User | null;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="flex h-11 w-11 flex-row items-center justify-center rounded-lg border border-transparent hover:bg-secondary-hover focus:border-base-content focus:outline-none"
>
    <AvatarV3 {user} size="medium" />
</button>
