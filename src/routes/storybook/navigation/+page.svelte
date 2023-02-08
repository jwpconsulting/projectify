<script lang="ts">
    import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { fr, fc, users, user1, user2 } from "$lib/storybook";
    import type { AvatarVariantContent } from "$lib/figma/types";
    import { avatarStateSizes, avatarVariantSizes } from "$lib/figma/types";

    const avatarV5Contents: AvatarVariantContent[] = [
        { kind: "assign", users: [user1, user2] },
        { kind: "assign", users: [null, user1] },
        { kind: "assign", users: [user2, null] },
        { kind: "multiple", users: [] },
        { kind: "multiple", users: [user1] },
        { kind: "multiple", users: [user1, user2, user1, user2, user1] },
    ];
</script>

Avatar V3
<div class={fc}>
    {#each avatarStateSizes as size}
        <div class="capitalize">
            {size}
        </div>
        <div class={fr}>
            {#each users as user}
                <div class="group">
                    <AvatarState {user} {size} />
                </div>
            {/each}
        </div>
    {/each}
</div>

Avatar V5
<div class={fc}>
    {#each avatarVariantSizes as size}
        <div class="capitalize">
            {size}
        </div>
        <div class={fr}>
            {#each avatarV5Contents as content}
                <div class="capitalize">
                    {content.kind}
                </div>
                <AvatarVariant {size} {content} />
            {/each}
        </div>
    {/each}
</div>
