<script lang="ts">
    import { _ } from "svelte-i18n";

    import TabBar from "$lib/figma/screens/workspace-settings/TabBar.svelte";
    import type { SettingKind } from "$lib/types/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="flex w-full max-w-xl flex-col gap-4">
    <h1 class="px-2 text-2xl font-bold sm:px-0">
        {$_("workspace-settings.title")}
    </h1>
    <main
        class="flex w-full max-w-xl flex-col gap-6 rounded-lg bg-foreground p-4 shadow-context-menu"
    >
        <TabBar {workspace} {activeSetting} />
        <slot />
    </main>
</div>
