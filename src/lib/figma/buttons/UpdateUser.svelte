<script lang="ts">
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { getDisplayName } from "$lib/types/user";
    import type { User } from "$lib/types/user";
    import type { AvatarVariantContent } from "$lib/figma/types";

    export let user: User | null;
    export let action: () => void;

    let avatarContent: AvatarVariantContent = {
        kind: "multiple",
        users: [null],
    };
    $: {
        avatarContent = {
            kind: "multiple",
            users: [user],
        };
    }
    let displayName: string | null = null;
    $: {
        displayName = user ? getDisplayName(user) : null;
    }
</script>

<button
    class="group rounded-2.5xl border border-transparent p-0.5 focus:border-border-focus focus:outline-none"
    on:click={action}
    on:keydown={action}
>
    <div
        class="flex flex-row items-center gap-2 rounded-2.5xl border border-dashed border-primary px-2 py-1 text-xxs font-bold text-primary group-hover:bg-background group-active:bg-secondary-hover"
        class:bg-task-hover={user !== null}
    >
        <AvatarVariant size="small" content={avatarContent} />
        {#if user}
            {displayName}
        {:else}
            Assign user
        {/if}
    </div>
</button>
