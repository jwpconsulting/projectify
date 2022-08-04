<script lang="ts">
    import UserAvatar from "$lib/components/UserAvatar.svelte";
    import type { User } from "$lib/types";
    import type { AvatarV3Size } from "$lib/figma/types";

    export let user: User | null;
    export let size: AvatarV3Size;

    $: outerSize = {
        medium: "h-8 w-8",
        small: "h-6 w-6",
    }[size];
    $: innerSize = {
        medium: 32,
        small: 24,
    }[size];
</script>

<div
    class={`flex ${outerSize} items-center justify-center rounded-full border border-primary`}
    class:bg-background={user === null}
>
    {#if user}
        <UserAvatar {user} size={innerSize} />
    {/if}
</div>
