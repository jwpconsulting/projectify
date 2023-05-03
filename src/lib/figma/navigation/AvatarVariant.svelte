<script lang="ts">
    import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
    import type {
        AvatarVariantContent,
        AvatarVariantSize,
    } from "$lib/figma/types";

    export let content: AvatarVariantContent;
    export let size: AvatarVariantSize;
    export let hoverableParent = false;

    const zIndices = new Map<number, string>([
        [0, "z-[110]"],
        [1, "z-[100]"],
        [2, "z-[90]"],
        [3, "z-[80]"],
        [4, "z-[70]"],
        [5, "z-[60]"],
        [6, "z-[50]"],
        [7, "z-40"],
        [8, "z-30"],
        [9, "z-20"],
        [10, "z-10"],
        [11, "z-0"],
    ]);
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
{:else if content.kind === "single"}
    <div class="p-0.5">
        <AvatarState user={content.user} {size} />
    </div>
{:else}
    <div
        class="isolate flex flex-row"
        class:p-0.5={size === "medium"}
        class:group={!hoverableParent}
    >
        {#each content.users as user, inx}
            <div
                class={`${zIndices.get(inx)} ${
                    size === "small" && inx < content.users.length - 1
                        ? "w-3"
                        : ""
                } ${
                    size === "medium" && inx < content.users.length - 1
                        ? "w-4"
                        : ""
                } ${
                    size === "hoverable" && inx < content.users.length - 1
                        ? "w-3 group-hover:w-4"
                        : ""
                }`}
            >
                <AvatarState {user} {size} />
            </div>
        {/each}
    </div>
{/if}
