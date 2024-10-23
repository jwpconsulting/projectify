<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Pencil } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { AvatarVariantContent } from "$lib/figma/types";
    import { getDisplayName } from "$lib/types/user";
    import type { TaskDetailAssignee } from "$lib/types/workspace";

    // Either a user has been assigned, or if not we should ask the user
    // to assign a user
    export let teamMember: TaskDetailAssignee | null;
    export let onInteract: ((anchor: HTMLElement) => void) | undefined =
        undefined;
    export let readonly = false;

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

    $: user = teamMember?.user;

    let displayName: string | undefined = undefined;
    $: {
        displayName = user ? getDisplayName(user) : undefined;
    }

    $: action =
        !readonly && onInteract ? onInteract.bind(null, btnRef) : undefined;
</script>

<div class="flex flex-row gap-2">
    <button
        class="flex w-full flex-row items-center gap-2 rounded-2.5xl border border-dashed border-primary px-2 py-1 font-bold text-primary {action !==
        undefined
            ? 'hover:bg-background active:bg-secondary-hover'
            : ''}"
        class:bg-task-hover={user !== undefined}
        type="button"
        on:click={action}
        disabled={!action}
        bind:this={btnRef}
    >
        <AvatarVariant size="medium" content={avatarContent} />
        <div class="truncate">
            {#if user}
                {displayName}
            {:else if action}
                {$_("dashboard.assign-user")}
            {:else}
                {$_("dashboard.no-user-assigned")}
            {/if}
        </div>
    </button>
    {#if onInteract && readonly}
        <button
            on:click|preventDefault={onInteract.bind(null, btnRef)}
            type="button"
        >
            <Icon src={Pencil} theme="outline" class="h-4 w-4" />
        </button>
    {/if}
</div>
