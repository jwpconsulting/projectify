<script lang="ts">
    import { seats, seatMinus, seatAdd } from "$lib/stores/onboarding";
    import IncrementSeats from "$lib/figma/buttons/IncrementSeats.svelte";
    import MinusSeats from "$lib/figma/buttons/MinusSeats.svelte";
</script>

<div class="flex flex-row items-center gap-4">
    <MinusSeats on:click={seatMinus} disabled={$seats < 1} />
    <input
        class="w-10 text-xl font-bold text-base-content"
        type="text"
        inputmode="numberic"
        bind:value={$seats}
    />
    <IncrementSeats on:click={seatAdd} />
</div>
