<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
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
    <AvatarState {user} size="medium" />
</button>
