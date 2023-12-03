<script lang="ts">
    import { _, number } from "svelte-i18n";

    import { pricePerSeat } from "$lib/config";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { createBillingPortalSession } from "$lib/repository/corporate";
    import type { Customer } from "$lib/types/corporate";
    import type { Workspace } from "$lib/types/workspace";

    async function editBillingDetails() {
        const { url } = await createBillingPortalSession(workspace.uuid, {
            fetch,
        });
        await goto(url);
    }

    export let workspace: Workspace;
    export let customer: Customer;
</script>

<div class="flex flex-col gap-6 border-b border-border px-4 py-6">
    <dl class="flex flex-col gap-6 text-base text-base-content">
        <div>
            <dt class="font-bold">
                {$_("workspace-settings.billing.subscription-status.title")}
            </dt>
            <dd>
                {#if customer.subscription_status === "ACTIVE"}{$_(
                        "workspace-settings.billing.subscription-status.active"
                    )}
                {:else}
                    {$_(
                        "workspace-settings.billing.subscription-status.inactive"
                    )}
                {/if}
            </dd>
        </div>
        <div>
            <dt class="font-bold">
                {$_("workspace-settings.billing.seats.number-of-seats")}
            </dt>
            <dd>
                {$_("workspace-settings.billing.seats.format", {
                    values: {
                        seats: $number(customer.seats),
                        seatsRemaining: $number(customer.seats_remaining),
                    },
                })}
            </dd>
        </div>
        <div>
            <dt class="font-bold">
                {$_("workspace-settings.billing.monthly-total.title", {
                    values: { pricePerSeat },
                })}
            </dt>
            <dd>
                {$_("workspace-settings.billing.monthly-total.status", {
                    values: { total: customer.seats * pricePerSeat },
                })}
            </dd>
        </div>
    </dl>
    <Button
        action={{ kind: "button", action: editBillingDetails }}
        color="blue"
        style={{ kind: "primary" }}
        label={$_("workspace-settings.billing.edit-billing-details")}
        size="medium"
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
