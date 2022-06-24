<script lang="ts">
    import { page } from "$app/stores";
    import type { OnboardingState } from "../../lib/types/onboarding";
    import { onboardingStates } from "../../lib/types/onboarding";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import { goto } from "$app/navigation";
    import IconPlus from "$lib/components/icons/icon-plus.svelte";
    import IconMinus from "$lib/components/icons/icon-minus.svelte";

    $: state = $page.url.searchParams.get("state") as OnboardingState;
    $: {
        if (!state) {
            state = "about-you";
        }
    }

    let fullName = "";
    let workspaceTitle = "";
    let boardTitle = "";
    let taskTitle = "";
    let labelName = "";

    function gotoNextState() {
        const stateInx = onboardingStates.findIndex((s) => s === state);

        if (state == "billing-details") {
            goto("https://stripe.com/");
        } else if (state == "payment-success") {
            goto(`?state=new-board`);
        } else if (state == "payment-error") {
            goto("https://stripe.com/");
        } else if (state == "assign-task") {
            goto("/dashboard");
        } else {
            state = onboardingStates[stateInx + 1];
            goto(`?state=${state}`);
        }
    }

    function gotoPrevStep() {
        const stateInx = onboardingStates.findIndex((s) => s === state);
        state = onboardingStates[stateInx - 1];
        goto(`?state=${state}`);
    }

    const billingSeats = [1, 5, 10, 15, 25];
    let numberOfSears = 1;
    $: selectedBillingSeatInx = billingSeats.findIndex(
        (it) => it == numberOfSears
    );

    function increaseSeats(positive: boolean = true) {
        if (positive) {
            numberOfSears++;
        } else {
            numberOfSears--;
        }

        numberOfSears = Math.max(1, numberOfSears);
    }
    function selectSeatInx(inx) {
        numberOfSears = billingSeats[inx];
    }
</script>

<main>
    <div class="flex min-h-[800px] grow">
        {#if state == "about-you"}
            <Onboarding
                title={"About you"}
                prompt={"Write your full name below."}
                nextBtnLabel={"Continue"}
                nextBtnDisabled={!fullName}
                hasContentPadding={true}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="inputs">
                    <input
                        type="text"
                        name="name"
                        class="input input-bordered"
                        bind:value={fullName}
                    />
                </svelte:fragment>

                <svelte:fragment slot="content-title">
                    Welcome{#if fullName},{/if}
                    {fullName}! 👋
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <div>User Profile picture</div>
                </svelte:fragment>
            </Onboarding>
        {:else if state == "new-workspace"}
            <Onboarding
                title={"Let’s set up your first workspace, full name."}
                prompt={"You can create and manage numerous workspaces"}
                nextBtnDisabled={!workspaceTitle}
                hasContentPadding={false}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="inputs">
                    <input
                        type="text"
                        name="workspaceTitle"
                        class="input input-bordered"
                        placeholder="e.g. the name of your company"
                        bind:value={workspaceTitle}
                    />
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration {state} {workspaceTitle} />
                </svelte:fragment>
            </Onboarding>
        {:else if state == "billing-details"}
            <Onboarding
                title={"Billing details"}
                nextBtnLabel={"Continue to checkout"}
                nextMessage={"We use Stripe for our payment processing services."}
                hasContentPadding={false}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>
                        Select the number of seats you’d like and then proceed
                        to the Stripe billing page. <br />Choose from pre-set
                        seat plans or a custom number.
                    </p>
                    <p>
                        Not sure yet? The default starts at 1 seat and you can
                        always change it later.
                    </p>
                </svelte:fragment>

                <svelte:fragment slot="inputs">
                    <div class="flex flex-col gap-20">
                        <div class="flex gap-8">
                            {#each billingSeats as seat, inx}
                                <button
                                    class:btn-active={selectedBillingSeatInx ==
                                        inx}
                                    class="btn btn-outline btn-primary btn-square"
                                    on:click={() => selectSeatInx(inx)}
                                >
                                    {seat}
                                </button>
                            {/each}
                        </div>
                        <div class="flex items-center gap-2">
                            <button
                                class="btn btn-circle btn-outline btn-primary btn-sm"
                                on:click={() => increaseSeats(false)}
                            >
                                <IconMinus />
                            </button>
                            <div class="max-w-fit text-center font-bold">
                                <input
                                    class="input-seats input"
                                    type="number"
                                    bind:value={numberOfSears}
                                />
                            </div>
                            <button
                                class="btn btn-circle btn-outline btn-primary btn-sm"
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
        {:else if state == "payment-success"}
            <Onboarding
                title={"Your workspace is all set up!"}
                hasContentPadding={false}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>Your free 31 day trial has begun.</p>
                    <p>
                        Your workspace has a # seats and the billing period
                        will start on year-month-day after your 31 trial period
                        ends.
                    </p>
                    <p>
                        Let’s continue by setting up your boards, tasks and
                        users.
                    </p>
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration {state} {workspaceTitle} />
                </svelte:fragment>
            </Onboarding>
        {:else if state == "payment-error"}
            <Onboarding
                title={"Please finish setting up your billing account"}
                nextBtnLabel={"Return to checkout"}
                hasContentPadding={false}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>Your free 31 day trial has not begun yet.</p>
                    <p>
                        Your workspace does not yet have seats assigned to it.
                    </p>
                    <p>
                        Please return to Stripe to finish the checkout process.
                    </p>
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration {state} {workspaceTitle} />
                </svelte:fragment>
            </Onboarding>
        {:else if state == "new-board"}
            <Onboarding
                title={"Add your first board"}
                hasContentPadding={false}
                stepCount={5}
                step={1}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>
                        You can create unlimited boards per workspace.
                        <br />They help you to focus on different projects you
                        may be working on.
                    </p>
                </svelte:fragment>

                <svelte:fragment slot="inputs">
                    <input
                        type="text"
                        name="boardTitle"
                        class="input input-bordered"
                        placeholder="e.g. marketing for Q1"
                        bind:value={boardTitle}
                    />
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration {state} {workspaceTitle} {boardTitle} />
                </svelte:fragment>
            </Onboarding>
        {:else if state == "new-task"}
            <Onboarding
                title={"What is a task you’d like to complete?"}
                hasContentPadding={false}
                stepCount={5}
                step={2}
                viewBackButton={true}
                on:back={() => gotoPrevStep()}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>
                        Tasks can be further divided into sub tasks and contain
                        detailed descriptions.
                    </p>
                </svelte:fragment>

                <svelte:fragment slot="inputs">
                    <input
                        type="text"
                        name="taskTitle"
                        class="input input-bordered"
                        placeholder="e.g. write document"
                        bind:value={taskTitle}
                    />
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration
                        {state}
                        {workspaceTitle}
                        {boardTitle}
                        {taskTitle}
                    />
                </svelte:fragment>
            </Onboarding>
        {:else if state == "new-section"}
            <Onboarding
                title={"We’ve put your task in a ‘To do’ section."}
                hasContentPadding={false}
                stepCount={5}
                step={3}
                viewBackButton={true}
                on:back={() => gotoPrevStep()}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>Add new sections and customise your section names.</p>
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration
                        {state}
                        {workspaceTitle}
                        {boardTitle}
                        {taskTitle}
                    />
                </svelte:fragment>
            </Onboarding>
        {:else if state == "new-label"}
            <Onboarding
                title={`Create a label for ${taskTitle}`}
                hasContentPadding={false}
                stepCount={5}
                step={4}
                viewBackButton={true}
                on:back={() => gotoPrevStep()}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>
                        Labels help you to filter between the types of tasks.
                    </p>
                </svelte:fragment>

                <svelte:fragment slot="inputs">
                    <input
                        type="text"
                        name="labelName"
                        class="input input-bordered"
                        placeholder="e.g. bug"
                        bind:value={labelName}
                    />
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration
                        {state}
                        {workspaceTitle}
                        {boardTitle}
                        {taskTitle}
                        {labelName}
                    />
                </svelte:fragment>
            </Onboarding>
        {:else if state == "assign-task"}
            <Onboarding
                title={`Task ${taskTitle} has been assigned to you!`}
                hasContentPadding={false}
                stepCount={5}
                step={5}
                nextBtnLabel={"Get started"}
                viewBackButton={true}
                on:back={() => gotoPrevStep()}
                on:next={() => gotoNextState()}
            >
                <svelte:fragment slot="prompt">
                    <p>You’re all set!</p>
                    <p>
                        If you wish to add new members to your workspace,
                        please go to the workspace settings menu next to your
                        workspace name.
                    </p>
                </svelte:fragment>

                <svelte:fragment slot="content">
                    <AppIllustration
                        {state}
                        {workspaceTitle}
                        {boardTitle}
                        {taskTitle}
                        {labelName}
                    />
                </svelte:fragment>
            </Onboarding>
        {/if}

        <!-- Debug -->
        <div
            class="absolute bottom-[0px] right-0 flex gap-2 bg-[#ffffff] bg-opacity-90 p-2 "
        >
            {#each onboardingStates as s}
                <a class:text-primary={state == s} href={`?state=${s}`}>{s}</a>
            {/each}
        </div>
    </div>
</main>

<style lang="scss">
    .input-seats {
        width: 100px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        padding-right: 8px;
    }
</style>
