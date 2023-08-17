<script lang="ts">
    import { _ } from "svelte-i18n";

    import WorkspaceSettingsPage from "$lib/figma/screens/workspace-settings/WorkspaceSettingsPage.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
</script>

<WorkspaceSettingsPage {workspace} activeSetting="billing">
    <div class="flex flex-col gap-6 border-b border-border px-4 py-6">
        <div
            class="flex flex-col gap-[21px] text-base font-bold text-base-content"
        >
            <p>
                {$_("settings.current-plan")}
            </p>
            <p>
                {$_("settings.number-of-seats")}
            </p>
            <p>
                {$_("settings.monthly-total")}
            </p>
        </div>
        <div class="">
            <Anchor
                label={$_("settings.edit-billing-details")}
                href="#TODO"
                size="normal"
            />
        </div>
    </div>

    <div class="flex flex-col gap-6 p-4">
        <div class="text-base font-bold text-base-content">
            {$_("settings.contact-us-to-request-changes")}
        </div>

        <div class="">
            <Anchor
                label={$_("settings.billing-contact")}
                href={`mailto:${$_("settings.billing-contact")}`}
                size="normal"
            />
        </div>
    </div>
</WorkspaceSettingsPage>
