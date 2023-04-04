<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import IconPlus from "$lib/components/icons/icon-plus.svelte";
    import IconMinus from "$lib/components/icons/icon-minus.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let state: OnboardingState = "billing-details";
    let numberOfSeats = 1;
    const billingSeats = [1, 5, 10, 15, 25];
    $: selectedBillingSeatInx = billingSeats.findIndex(
        (it) => it == numberOfSeats
    );
    function increaseSeats(positive = true) {
        if (positive) {
            numberOfSeats++;
        } else {
            numberOfSeats--;
        }

        numberOfSeats = Math.max(1, numberOfSeats);
    }
    function selectSeatInx(inx: number) {
        numberOfSeats = billingSeats[inx];
    }
</script>

<Onboarding
    title={"Billing details"}
    nextBtnLabel={"Continue to checkout"}
    nextMessage={"We use Stripe for our payment processing services."}
    hasContentPadding={false}
>
    <svelte:fragment slot="prompt">
        <p>
            Select the number of seats you’d like and then proceed to the
            Stripe billing page. <br />Choose from pre-set seat plans or a
            custom number.
        </p>
        <p>
            Not sure yet? The default starts at 1 seat and you can always
            change it later.
        </p>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <div class="flex flex-col gap-20">
            <div class="flex gap-8">
                {#each billingSeats as seat, inx}
                    <button
                        class:btn-active={selectedBillingSeatInx == inx}
                        class="btn btn-square btn-outline btn-primary"
                        on:click={() => selectSeatInx(inx)}
                    >
                        {seat}
                    </button>
                {/each}
            </div>
            <div class="flex items-center gap-2">
                <button
                    class="btn btn-outline btn-primary btn-circle btn-sm"
                    on:click={() => increaseSeats(false)}
                >
                    <IconMinus />
                </button>
                <div class="max-w-fit text-center font-bold">
                    <input
                        class="input w-24 pr-2 text-center text-xl font-bold"
                        type="number"
                        bind:value={numberOfSeats}
                    />
                </div>
                <button
                    class="btn btn-outline btn-primary btn-circle btn-sm"
                    on:click={() => increaseSeats(true)}
                >
                    <IconPlus />
                </button>
            </div>
        </div>
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} />
    </svelte:fragment>
</Onboarding>
