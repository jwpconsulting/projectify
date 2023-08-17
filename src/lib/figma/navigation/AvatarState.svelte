<script lang="ts">
    import UserAvatar from "$lib/components/UserAvatar.svelte";
    import type { AvatarStateSize } from "$lib/figma/types";
    import type { User } from "$lib/types/user";

    export let user: User | null;
    export let size: AvatarStateSize;

    $: outerSize = {
        large: "h-24 w-24",
        medium: "h-8 w-8",
        small: "h-6 w-6",
        hoverable: "h-6 w-6 group-hover:h-8 group-hover:w-8",
    }[size];
    type Size = 24 | 32 | 92;
    let innerSize: Size;
    const sizes: Record<AvatarStateSize, Size> = {
        large: 92,
        medium: 32,
        small: 24,
        hoverable: 32,
    } as const;
    $: innerSize = sizes[size];
</script>

<div
    class={`flex ${outerSize} items-center justify-center rounded-full border border-primary`}
    class:bg-background={user === null}
>
    {#if user}
        <UserAvatar {user} size={innerSize} />
    {/if}
</div>
