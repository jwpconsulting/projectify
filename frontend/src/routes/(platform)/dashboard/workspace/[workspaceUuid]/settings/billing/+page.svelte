<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import { pricePerSeat } from "$lib/config";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { currentCustomer } from "$lib/stores/dashboard/customer";

    import type { PageData } from "./$types";

    import { invalidateAll } from "$app/navigation";
    import { openApiClient } from "$lib/repository/util";

    export let data: PageData;

    $: customer = $currentCustomer ?? data.customer;
    $: workspace = data.workspace;

    // Unpaid
    async function goToCheckout() {
        let checkoutSeats: number;
        try {
            checkoutSeats = parseInt(checkoutSeatsRaw, 10);
        } catch {
            throw new Error("Expected valid seats");
        }
        const { data, error } = await openApiClient.POST(
            "/corporate/workspace/{workspace_uuid}/create-checkout-session",
            {
                params: { path: { workspace_uuid: workspace.uuid } },
                body: { seats: checkoutSeats },
            },
        );
        if (error === undefined) {
            const { url } = data;
            window.location.href = url;
            return;
        } else if (error.code !== 400) {
            throw new Error("Could not create checkout session");
        }
        if (error.details.seats) {
            checkoutError = error.details.seats;
        } else {
            throw new Error(
                "Unknown validation error when creating checkout session",
            );
        }
    }

    async function submitRedeemCoupon() {
        if (!couponCode) {
            throw new Error("Expected couponCode");
        }
        const { error } = await openApiClient.POST(
            "/corporate/workspace/{workspace_uuid}/redeem-coupon",
            {
                params: { path: { workspace_uuid: workspace.uuid } },
                body: { code: couponCode },
            },
        );
        if (error === undefined) {
            await invalidateAll();
            return;
        }
        if (error.code !== 400) {
            throw new Error("Could not redeem coupon");
        }
        if (error.details.code) {
            couponCodeValidation = {
                ok: false,
                error: error.details.code,
            };
        } else {
            couponError = $_(
                "workspace-settings.billing.unpaid.coupon.unknown-error",
            );
        }
    }

    // Paid
    async function editBillingDetails() {
        const { error, data } = await openApiClient.POST(
            "/corporate/workspace/{workspace_uuid}/create-billing-portal-session",
            { params: { path: { workspace_uuid: workspace.uuid } } },
        );
        if (error === undefined) {
            const { url } = data;
            window.location.href = url;
            return;
        }
        throw new Error("Could not open billing portal");
    }

    // Unpaid user:
    // Checkout
    let checkoutSeatsRaw = "1";
    let checkoutError: string | undefined = undefined;
    // Coupon
    let couponCode: string | undefined = undefined;
    let couponError: string | undefined = undefined;
    let couponCodeValidation: InputFieldValidation | undefined = undefined;

    // Paid user:
    const editBillingError: string | undefined = undefined;
    $: quota = workspace.quota.team_members_and_invites;
    $: seatsRemaining = (quota.current ?? 0) - (quota.limit ?? 0);
</script>

<svelte:head>
    <title
        >{$_("workspace-settings.billing.title", {
            values: { title: workspace.title },
        })}</title
    >
</svelte:head>

<section class="flex flex-col gap-12 px-4 py-6">
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
                        seatsRemaining,
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
    {:else if customer.subscription_status === "UNPAID" || customer.subscription_status === "CANCELLED"}
        <section>
            <p class="font-bold">
                {#if customer.subscription_status === "UNPAID"}
                    {$_("workspace-settings.billing.unpaid.status.title")}
                {:else}
                    {$_("workspace-settings.billing.unpaid.cancelled.title")}
                {/if}
            </p>
            <p>
                {#if customer.subscription_status === "UNPAID"}
                    {$_(
                        "workspace-settings.billing.unpaid.status.explanation",
                    )}
                {:else}
                    {$_(
                        "workspace-settings.billing.unpaid.cancelled.explanation",
                    )}
                {/if}
            </p>
        </section>
        <form
            on:submit|preventDefault={goToCheckout}
            class="flex flex-col gap-4"
        >
            <header class="flex flex-col gap-1">
                <h2 class="font-bold">
                    {$_("workspace-settings.billing.unpaid.checkout.title")}
                </h2>
                <p>
                    {$_(
                        "workspace-settings.billing.unpaid.checkout.seats.explanation",
                    )}
                </p>
            </header>
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
                required
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
        <form
            on:submit|preventDefault={submitRedeemCoupon}
            class="flex flex-col gap-4"
        >
            <header class="flex flex-col gap-1">
                <h2 class="font-bold">
                    {$_("workspace-settings.billing.unpaid.coupon.title")}
                </h2>
                <p>
                    {$_(
                        "workspace-settings.billing.unpaid.coupon.description",
                    )}
                </p>
            </header>
            <InputField
                label={$_(
                    "workspace-settings.billing.unpaid.coupon.code.label",
                )}
                bind:value={couponCode}
                name="code"
                placeholder={$_(
                    "workspace-settings.billing.unpaid.coupon.code.placeholder",
                )}
                style={{ inputType: "text" }}
                validation={couponCodeValidation}
                required
            />
            {#if couponError}
                <p>{couponError}</p>
            {/if}
            <Button
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                action={{ kind: "submit" }}
                label={$_("workspace-settings.billing.unpaid.coupon.action")}
            />
        </form>
    {:else if customer.subscription_status === "CUSTOM"}
        <section class="flex flex-col gap-2">
            <p class="font-bold">
                {$_("workspace-settings.billing.custom.status.title")}
            </p>
            <p>
                {$_("workspace-settings.billing.custom.status.explanation")}
            </p>
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
