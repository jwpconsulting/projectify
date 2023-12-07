<script lang="ts">
    import { _, number } from "svelte-i18n";

    import { pricePerSeat } from "$lib/config";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import {
        createBillingPortalSession,
        createCheckoutSession,
    } from "$lib/repository/corporate";
    import { currentCustomer } from "$lib/stores/dashboard";
    import type { Customer } from "$lib/types/corporate";
    import type { Workspace } from "$lib/types/workspace";

    async function goToCheckout() {
        let checkoutSeats: number;
        try {
            checkoutSeats = parseInt(checkoutSeatsRaw, 10);
        } catch {
            throw new Error("Expected valid seats");
        }
        const { url } = await createCheckoutSession(
            workspace.uuid,
            checkoutSeats,
            {
                fetch,
            }
        );
        await goto(url);
    }
    async function editBillingDetails() {
        const { url } = await createBillingPortalSession(workspace.uuid, {
            fetch,
        });
        await goto(url);
    }

    export let workspace: Workspace;
    export let customer: Customer;

    let checkoutSeatsRaw = "1";

    $: customer = $currentCustomer ?? customer;
</script>

<section class="flex flex-col gap-6 px-4 py-6">
    {#if customer.subscription_status === "ACTIVE"}
        <section>
            <p class="font-bold">
                {$_("workspace-settings.billing.active.status.title")}
            </p>
            <p>
                {$_("workspace-settings.billing.active.status.explanation")}
            </p>
        </section>
        <section>
            <p class="font-bold">
                {$_("workspace-settings.billing.active.monthly-total.title", {
                    values: { pricePerSeat },
                })}
            </p>
            <p>
                {$_("workspace-settings.billing.active.monthly-total.status", {
                    values: { total: customer.seats * pricePerSeat },
                })}
            </p>
        </section>
        <section>
            <p class="font-bold">
                {$_("workspace-settings.billing.active.seats.title", {
                    values: {
                        pricePerSeat,
                    },
                })}
            </p>
            <p>
                {$_("workspace-settings.billing.active.seats.status", {
                    values: {
                        seats: customer.seats,
                        seatsRemaining: $number(customer.seats_remaining),
                    },
                })}
            </p>
        </section>
        <Button
            action={{ kind: "button", action: editBillingDetails }}
            color="blue"
            style={{ kind: "primary" }}
            label={$_(
                "workspace-settings.billing.active.edit-billing-details"
            )}
            size="medium"
        />
    {:else if customer.subscription_status === "UNPAID"}
        <section>
            <p class="font-bold">
                {$_("workspace-settings.billing.unpaid.status.title")}
            </p>
            <p>
                {$_("workspace-settings.billing.unpaid.status.explanation")}
            </p>
        </section>
        <section>
            <p class="font-bold">
                {$_("workspace-settings.billing.unpaid.checkout.title")}
            </p>
            <p>
                {$_(
                    "workspace-settings.billing.unpaid.checkout.seats.explanation"
                )}
            </p>
            <InputField
                label={$_(
                    "workspace-settings.billing.unpaid.checkout.seats.label"
                )}
                bind:value={checkoutSeatsRaw}
                name="checkout-seats"
                placeholder={$_(
                    "workspace-settings.billing.unpaid.checkout.seats.placeholder"
                )}
                style={{ inputType: "numeric", min: 1, max: 100 }}
            />
            <Button
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                action={{ kind: "button", action: goToCheckout }}
                label={$_("workspace-settings.billing.unpaid.checkout.action")}
            />
        </section>
    {/if}
</section>

<section class="flex flex-col gap-2 p-4">
    <div class="text-base font-bold">
        {$_("workspace-settings.billing.contact-us")}
    </div>
    <Anchor
        label={$_("workspace-settings.billing.billing-contact")}
        href={`mailto:${$_("workspace-settings.billing.billing-contact")}`}
        size="normal"
    />
</section>
