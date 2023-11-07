<script lang="ts">
    import { AvatarMarble as Avatar } from "svelte-boring-avatars";

    import { getDisplayName, type User } from "$lib/types/user";

    export let user: User;
    export let size: 24 | 32 | 92;
    $: profilePicture = user.profile_picture;
    $: name = `${user.email}${getDisplayName(user)}`;
</script>

{#if profilePicture}
    <img
        src={profilePicture}
        alt={name}
        class="h-full w-full rounded-full object-cover object-center"
    />
{:else}
    <Avatar {size} {name} />
{/if}
