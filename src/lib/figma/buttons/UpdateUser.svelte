<script lang="ts">
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { AvatarVariantContent } from "$lib/figma/types";
    import { getDisplayName } from "$lib/types/user";
    import type { User } from "$lib/types/user";

    export let user: User | null;
    export let action: (() => void) | undefined;

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
    class="group rounded-2.5xl border border-transparent p-0.5 {action
        ? 'focus:border-border-focus focus:outline-none'
        : ''}"
    on:click={action}
    on:keydown={action}
    disabled={!action}
>
    <div
        class="flex flex-row items-center gap-2 rounded-2.5xl border border-dashed border-primary px-2 py-1 text-xxs font-bold text-primary {action
            ? 'group-hover:bg-background group-active:bg-secondary-hover'
            : ''}"
        class:bg-task-hover={user !== null}
    >
        <AvatarVariant size="small" content={avatarContent} />
        <div class="line-clamp-1 overflow-hidden">
            {#if user}
                {displayName}
            {:else if action}
                {$_("dashboard.assign-user")}
            {:else}
                {$_("dashboard.no-user-assigned")}
            {/if}
        </div>
    </div>
</button>
