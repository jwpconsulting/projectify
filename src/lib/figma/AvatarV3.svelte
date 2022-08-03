<script lang="ts">
    import UserAvatar from "$lib/components/UserAvatar.svelte";
    import type { User } from "$lib/types";

    export let user: User | null;
</script>

<div
    class="flex h-6 w-6 items-center justify-center rounded-full border border-primary"
    class:bg-background={user === null}
>
    {#if user}
        <UserAvatar {user} size={24} />
    {/if}
</div>
