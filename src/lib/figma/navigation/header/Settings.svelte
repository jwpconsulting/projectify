<script lang="ts">
    import { _ } from "svelte-i18n";
    import Header from "$lib/figma/navigation/header/Header.svelte";
    import HeaderMobile from "$lib/figma/navigation/header/HeaderMobile.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import AvatarWithHover from "$lib/figma/buttons/UserAccount.svelte";
    import type { User } from "$lib/types/user";

    export let user: User;
</script>

<Header logoVisible>
    <slot slot="right">
        <div class="flex flex-row gap-4">
            <a href="/notifications">
                <NotificationButton isActive />
            </a>
            <AvatarWithHover {user} />
        </div>
    </slot>
</Header>

<HeaderMobile logoVisible>
    <div class="flex flex-row gap-4">
        <a href="/notifications">
            <NotificationButton isActive />
        </a>
        <AvatarWithHover {user} />
    </div>
</HeaderMobile>
