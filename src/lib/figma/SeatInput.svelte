<script lang="ts">
    import { seats, seatMinus, seatAdd } from "$lib/stores/onboarding";
    import AddSeats from "$lib/figma/AddSeats.svelte";
    import MinusSeats from "$lib/figma/MinusSeats.svelte";
</script>

<div class="flex flex-row items-center gap-4">
    <MinusSeats on:click={seatMinus} disabled={$seats < 1} />
    <input
        class="w-10 text-xl font-bold text-base-content"
        type="text"
        inputmode="numberic"
        bind:value={$seats}
    />
    <AddSeats on:click={seatAdd} />
</div>
