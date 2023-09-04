<script lang="ts">
    import { _, number } from "svelte-i18n";

    import WorkspaceSettingsPage from "$lib/figma/screens/workspace-settings/WorkspaceSettingsPage.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { Customer } from "$lib/types/corporate";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let customer: Customer;
</script>

<WorkspaceSettingsPage {workspace} activeSetting="billing">
    <div class="flex flex-col gap-6 border-b border-border px-4 py-6">
        <dl class="flex flex-col gap-6 text-base text-base-content">
            <div>
                <dt class="font-bold">
                    {$_("workspace-settings.billing.current-plan")}
                </dt>
                <dd>PLAN NAME GOES HERE</dd>
            </div>
            <div>
                <dt class="font-bold">
                    {$_("workspace-settings.billing.seats.number-of-seats")}
                </dt>
                <dd>
                    {$_("workspace-settings.billing.seats.format", {
                        values: {
                            seats: $number(customer.seats),
                            seats_remaining: $number(customer.seats_remaining),
                        },
                    })}
                </dd>
            </div>
            <div>
                <dt class="font-bold">
                    {$_("workspace-settings.billing.monthly-total")}
                </dt>
                <dd>TODO calculate monthly total</dd>
            </div>
        </dl>
        <Anchor
            label={$_("workspace-settings.billing.edit-billing-details")}
            href="#TODO"
            size="normal"
        />
    </div>

    <div class="flex flex-col gap-6 p-4">
        <div class="text-base font-bold text-base-content">
            {$_("workspace-settings.billing.contact-us-to-request-changes")}
        </div>
        <Anchor
            label={$_("workspace-settings.billing.billing-contact")}
            href={`mailto:${$_("workspace-settings.billing.billing-contact")}`}
            size="normal"
        />
    </div>
</WorkspaceSettingsPage>
