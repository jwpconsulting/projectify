<script lang="ts">
    import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
    import type {
        AvatarVariantContent,
        AvatarVariantSize,
    } from "$lib/figma/types";

    export let content: AvatarVariantContent;
    export let size: AvatarVariantSize;
    export let hoverableParent = false;
    $: assignStyle = {
        small: "w-9 h-9",
        medium: "w-12 h-12",
        large: "w-24 h-24",
        hoverable: "w-12 h-12 group-hover:w-12 h-12",
    }[size];
</script>

{#if content.kind === "assign"}
    <div class={`relative ${assignStyle}`} class:group={!hoverableParent}>
        <div class="absolute bottom-1/3 left-1/3">
            <AvatarState user={content.users[1]} {size} />
        </div>
        <div class="absolute right-1/3 top-1/3">
            <AvatarState user={content.users[0]} {size} />
        </div>
    </div>
{:else}
    <div class="p-0.5">
        <AvatarState user={content.user} {size} />
    </div>
{/if}
