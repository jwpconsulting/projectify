<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";

    let fullName = "";
</script>

<Onboarding
    title={"About you"}
    prompt={"Write your full name below."}
    nextBtnLabel={"Continue"}
    nextBtnDisabled={!fullName}
    hasContentPadding={true}
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
