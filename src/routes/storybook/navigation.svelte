<script lang="ts">
    import AvatarV3 from "$lib/figma/AvatarV3.svelte";
    import { fr, fc, users } from "$lib/storybook";
    import { avatarV3Sizes } from "$lib/figma/types";
</script>

Avatar V3
<div class={fc}>
    {#each avatarV3Sizes as size}
        <div class="capitalize">
            {size}
        </div>
        <div class={fr}>
            {#each users as user}
                <AvatarV3 {user} {size} />
            {/each}
        </div>
    {/each}
</div>
