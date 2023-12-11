<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { getWorkspaceBoardSearchUrl } from "$lib/urls/dashboard";

    import type { LayoutData } from "./$types";

    export let data: LayoutData;

    $: workspaceBoard = data.workspaceBoard;
    let searchInput: string | undefined = undefined;

    $: canSearch = searchInput !== undefined;
</script>

<div
    class="flex h-full flex-col items-center gap-4 overflow-y-auto bg-background py-4"
>
    <form
        action={getWorkspaceBoardSearchUrl(workspaceBoard)}
        class="flex w-full max-w-md flex-col gap-2 rounded-xl bg-foreground px-4 py-4"
    >
        <!-- XXX definitely not ideal, placeholder will disappear after input -->
        <InputField
            style={{ inputType: "text" }}
            label={$_("dashboard.search-task.input.label")}
            placeholder={$_("dashboard.search-task.input.placeholder")}
            name="search"
            bind:value={searchInput}
            showClearButton={false}
        />
        <Button
            label={$_("dashboard.search-task.button")}
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
    <!-- shared layout for workspace board and search results -->
    <!-- XXX: setting overflow-x-auto here magically solves an overflowing task card
    Why? Justus 2023-08-28 -->
    <div class="flex w-full grow flex-col">
        <slot />
    </div>
</div>
