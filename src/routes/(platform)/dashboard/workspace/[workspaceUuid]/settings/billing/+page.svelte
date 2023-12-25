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

    import type { PageData } from "./$types";

    export let data: PageData;

    $: customer = $currentCustomer ?? data.customer;
    $: workspace = data.workspace;

    async function goToCheckout() {
        let checkoutSeats: number;
        try {
            checkoutSeats = parseInt(checkoutSeatsRaw, 10);
        } catch {
            throw new Error("Expected valid seats");
        }
        const response = await createCheckoutSession(
            workspace.uuid,
            checkoutSeats,
            { fetch },
        );
        if (!response.ok) {
            // XXX not pretty
            checkoutError = JSON.stringify(response.error);
            console.error(response);
            return;
        }
        const { url } = response.data;
        await goto(url);
    }
    async function editBillingDetails() {
        const response = await createBillingPortalSession(workspace.uuid, {
            fetch,
        });
        if (!response.ok) {
            // XXX not pretty
            editBillingError = JSON.stringify(response.error);
            console.error(response);
            return;
        }
        const { url } = response.data;
        await goto(url);
    }

    let checkoutSeatsRaw = "1";
    let checkoutError: string | undefined = undefined;
    let editBillingError: string | undefined = undefined;
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
        {#if editBillingError}
            <p>{editBillingError}</p>
        {/if}
        <Button
            action={{ kind: "button", action: editBillingDetails }}
            color="blue"
            style={{ kind: "primary" }}
            label={$_(
                "workspace-settings.billing.active.edit-billing-details",
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
                    "workspace-settings.billing.unpaid.checkout.seats.explanation",
                )}
            </p>
        </section>
        <form
            on:submit|preventDefault={goToCheckout}
            class="flex flex-col gap-4"
        >
            <InputField
                label={$_(
                    "workspace-settings.billing.unpaid.checkout.seats.label",
                )}
                bind:value={checkoutSeatsRaw}
                name="checkout-seats"
                placeholder={$_(
                    "workspace-settings.billing.unpaid.checkout.seats.placeholder",
                )}
                style={{ inputType: "numeric", min: 1, max: 100 }}
            />
            {#if checkoutError}
                <p>{checkoutError}</p>
            {/if}
            <Button
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                action={{ kind: "submit" }}
                label={$_("workspace-settings.billing.unpaid.checkout.action")}
            />
        </form>
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
