<script lang="ts">
    import AvatarV3 from "$lib/figma/AvatarV3.svelte";
    import type { AvatarV5Size, AvatarV5Content } from "$lib/figma/types";

    export let content: AvatarV5Content;
    export let size: AvatarV5Size;

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
    $: assignStyle = size === "small" ? "w-9 h-9" : "w-12 h-12";
</script>

{#if content.kind === "assign"}
    <div class={`relative ${assignStyle}`}>
        <div class="absolute left-1/3 bottom-1/3">
            <AvatarV3 user={content.users[1]} {size} />
        </div>
        <div class="absolute top-1/3 right-1/3">
            <AvatarV3 user={content.users[0]} {size} />
        </div>
    </div>
{:else}
    <div class="flex flex-row" class:p-0.5={size === "medium"}>
        {#each content.users as user, inx}
            <div
                class:w-3={size === "small" && inx < content.users.length - 1}
                class:w-4={size === "medium" && inx < content.users.length - 1}
                class={`${zIndices.get(inx)}`}
            >
                <AvatarV3 {user} {size} />
            </div>
        {/each}
    </div>
{/if}
