<script lang="ts">
    import AvatarV3 from "$lib/figma/AvatarV3.svelte";
    import AvatarWithHover from "$lib/figma/AvatarWithHover.svelte";
    import { fr } from "$lib/storybook";

    const users = [
        {
            email: "hello@example.com",
            full_name: "Max Mustermann",
        },
        null,
    ];
</script>

Avatar V3
<div class={fr}>
    {#each users as user}
        <AvatarV3 {user} />
    {/each}
</div>
Avatar with hover
<div class={fr}>
    {#each users as user}
        <AvatarWithHover
            {user}
            on:click={() => console.log("AvatarWithHover", user)}
        />
    {/each}
</div>
