<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import TabBar from "$lib/figma/screens/workspace-settings/TabBar.svelte";
    import type { SettingKind } from "$lib/types/dashboard";

    import type { LayoutData } from "./$types";

    import { page } from "$app/stores";

    export let data: LayoutData;
    const { workspace } = data;

    function getActiveSetting({ pathname }: URL): SettingKind {
        if (pathname.endsWith("settings")) {
            return "index";
        } else if (pathname.endsWith("billing")) {
            return "billing";
        } else if (pathname.endsWith("team-members")) {
            return "team-members";
        } else if (pathname.endsWith("quota")) {
            return "quota";
        }
        throw new Error("Unknown settings path");
    }

    $: activeSetting = getActiveSetting($page.url);
</script>

<svelte:head>
    <title
        >{$_("workspace-settings.title", {
            values: { title: workspace.title },
        })}</title
    >
</svelte:head>

<div class="flex w-full max-w-xl flex-col gap-4">
    <h1 class="px-2 text-2xl font-bold sm:px-0">
        {$_("workspace-settings.heading")}
    </h1>
    <main
        class="flex w-full max-w-xl flex-col gap-10 rounded-lg bg-foreground p-4 shadow-context-menu"
    >
        <TabBar {workspace} {activeSetting} />
        <slot />
    </main>
</div>
