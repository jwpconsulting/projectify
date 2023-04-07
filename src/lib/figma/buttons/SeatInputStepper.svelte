<script lang="ts">
    import { seatAdd, seatMinus, seats } from "$lib/stores/onboarding";
    import IncrementSeats from "$lib/figma/buttons/IncrementSeats.svelte";
    import DecrementSeats from "$lib/figma/buttons/DecrementSeats.svelte";
</script>

<div class="flex flex-row items-center gap-4">
    <DecrementSeats on:click={seatMinus} disabled={$seats < 1} />
    <input
        class="w-10 text-xl font-bold text-base-content"
        type="text"
        inputmode="numeric"
        bind:value={$seats}
    />
    <IncrementSeats on:click={seatAdd} />
</div>
