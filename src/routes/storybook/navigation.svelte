<script lang="ts">
    import Avatar from "$lib/figma/Avatar.svelte";
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

Avatar
<div class={fr}>
    {#each users as user}
        <Avatar {user} />
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
