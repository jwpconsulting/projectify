<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { currentWorkspaceBoard } from "$lib/stores/dashboard";
    import { toggleMobileMenu } from "$lib/stores/globalUi";
    import type { User } from "$lib/types/user";
    import { getWorkspaceBoardSearchUrl } from "$lib/urls/dashboard";
    import { unwrap } from "$lib/utils/type";

    export let user: User;
    let searchInput: string | undefined = undefined;

    async function performSearch() {
        const workspaceBoard = unwrap(
            $currentWorkspaceBoard,
            "Expected $currentWorkspaceBoard"
        );
        await goto(
            getWorkspaceBoardSearchUrl(
                workspaceBoard,
                unwrap(searchInput, "Expected searchInput")
            )
        );
    }

    $: canSearch = searchInput !== undefined;
</script>

<Layout logoVisibleDesktop>
    <svelte:fragment slot="desktop-right">
        <form
            on:submit|preventDefault={performSearch}
            class="flex flex-row items-center gap-2"
        >
            <!-- XXX definitely not ideal, placeholder will disappear after input -->
            <label class="sr-only" for="search"
                >{$_("dashboard.search-task")}</label
            >
            <InputField
                style={{ inputType: "text" }}
                label={undefined}
                placeholder={$_("dashboard.search-task")}
                name="search"
                bind:value={searchInput}
                showClearButton={false}
            />
            <Button
                label={$_("dashboard.search-task")}
                action={{ kind: "submit", disabled: !canSearch }}
                style={{
                    kind: "tertiary",
                    icon: { position: "left", icon: Search },
                }}
                size="small"
                color="blue"
                grow={false}
            />
        </form>
        <div class="flex flex-row gap-4">
            <UserAccount {user} />
        </div>
    </svelte:fragment>
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
