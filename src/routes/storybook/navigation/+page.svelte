<script lang="ts">
    import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
    import { avatarStateSizes } from "$lib/figma/types";
    import { fc, fr, users } from "$lib/storybook";
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
