<script lang="ts">
    import Avatar from "$lib/figma/Avatar.svelte";
    import { fr } from "$lib/storybook";

    const users = [
        {
            email: "hello@example.com",
            full_name: "Max Mustermann",
        },
        null,
    ];
</script>

<div class={fr}>
    {#each users as user}
        <Avatar {user} />
    {/each}
</div>
