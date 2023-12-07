<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { taskSearchInput } from "$lib/stores/dashboard/task";
    import { toggleMobileMenu } from "$lib/stores/globalUi";
    import type { User } from "$lib/types/user";

    export let user: User;
</script>

<Layout logoVisibleDesktop>
    <slot slot="desktop-right">
        <!-- XXX definitely not ideal, placeholder will disappear after input -->
        <label class="sr-only" for="search"
            >{$_("dashboard.search-task")}</label
        >
        <InputField
            style={{ inputType: "text" }}
            label={undefined}
            placeholder={$_("dashboard.search-task")}
            name="search"
            bind:value={$taskSearchInput}
        >
            <Icon slot="left" src={Search} class="w-4" theme="outline" />
        </InputField>
        <div class="flex flex-row gap-4">
            <UserAccount {user} />
        </div>
    </slot>
    <slot slot="mobile">
        <div class="flex flex-row gap-4">
            <HamburgerMenu
                isActive
                action={() => toggleMobileMenu({ kind: "dashboard" })}
            />
            <SearchMobile />
        </div>

        <div class="flex flex-row gap-4">
            <UserAccount {user} />
        </div>
    </slot>
</Layout>
