<script lang="ts">
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import AvatarWithHover from "$lib/figma/buttons/UserAccount.svelte";
    import HeaderUniversal from "$lib/figma/navigation/header/HeaderUniversal.svelte";
    import type { User } from "$lib/types/user";

    export let user: User;
</script>

<HeaderUniversal logoVisibleDesktop logoVisibleMobile>
    <slot slot="desktop-right">
        <div class="flex flex-row gap-4">
            <a href="/notifications">
                <NotificationButton isActive />
            </a>
            <AvatarWithHover {user} />
        </div>
    </slot>
    <div slot="mobile" class="flex flex-row gap-4">
        <a href="/notifications">
            <NotificationButton isActive />
        </a>
        <AvatarWithHover {user} />
    </div>
</HeaderUniversal>
