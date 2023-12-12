<script lang="ts">
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { AvatarVariantContent } from "$lib/figma/types";
    import { getDisplayName } from "$lib/types/user";
    import type { WorkspaceUser } from "$lib/types/workspace";

    // Either a user has been assigned, or if not we should ask the user
    // to assign a user
    export let workspaceUser: WorkspaceUser | undefined;
    export let onInteract: ((anchor: HTMLElement) => void) | undefined =
        undefined;

    let btnRef: HTMLElement;

    let avatarContent: AvatarVariantContent = {
        kind: "single",
    };
    $: {
        avatarContent = {
            kind: "single",
            user,
        };
    }

    $: user = workspaceUser?.user;

    let displayName: string | undefined = undefined;
    $: {
        displayName = user ? getDisplayName(user) : undefined;
    }

    $: action = onInteract ? onInteract.bind(null, btnRef) : undefined;
</script>

<button
    class="group rounded-2.5xl border border-transparent p-0.5 {action
        ? 'focus:border-border-focus focus:outline-none'
        : ''}"
    type="button"
    on:click={action}
    disabled={!action}
    bind:this={btnRef}
>
    <div
        class="flex flex-row items-center gap-2 rounded-2.5xl border border-dashed border-primary px-2 py-1 text-sm font-bold text-primary {action
            ? 'group-hover:bg-background group-active:bg-secondary-hover'
            : ''}"
        class:bg-task-hover={user !== undefined}
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
