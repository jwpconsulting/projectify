<script lang="ts">
    import AvatarV3 from "$lib/figma/AvatarV3.svelte";
    import AvatarV5 from "$lib/figma/AvatarV5.svelte";
    import { fr, fc, users, user1, user2 } from "$lib/storybook";
    import type { AvatarV5Content } from "$lib/figma/types";
    import { avatarV3Sizes, avatarV5Sizes } from "$lib/figma/types";

    const avatarV5Contents: AvatarV5Content[] = [
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
    {#each avatarV3Sizes as size}
        <div class="capitalize">
            {size}
        </div>
        <div class={fr}>
            {#each users as user}
                <div class="group">
                    <AvatarV3 {user} {size} />
                </div>
            {/each}
        </div>
    {/each}
</div>

Avatar V5
<div class={fc}>
    {#each avatarV5Sizes as size}
        <div class="capitalize">
            {size}
        </div>
        <div class={fr}>
            {#each avatarV5Contents as content}
                <div class="capitalize">
                    {content.kind}
                </div>
                <AvatarV5 {size} {content} />
            {/each}
        </div>
    {/each}
</div>
