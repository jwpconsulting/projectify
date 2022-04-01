<script lang="ts">
    export const prerender = false;
    import DatePicker from "$lib/components/datePicker.svelte";

    const monthDates = new Array(32).fill({}).map((it, inx) => {
        const date = new Date(1);
        date.setFullYear(2022);
        date.setMonth(inx);
        date.setDate(1);
        return date;
    });
</script>

<div
    class="flex min-h-full flex-wrap items-center justify-center bg-secondary p-8"
>
    {#each monthDates as date}
        <div class="m-1">
            <DatePicker {date} />
        </div>
    {/each}
</div>
