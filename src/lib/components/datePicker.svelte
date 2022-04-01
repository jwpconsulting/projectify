<script lang="ts">
    import { getCalendar, months, weekDays } from "$lib/utils/date";

    export let date = new Date();

    // currentDateObj.setDate(1);
    // currentDateObj.setMonth(currentDateObj.getMonth());

    $: year = date.getFullYear();
    $: month = date.getMonth();
    $: calendar = getCalendar(year, month);

    function selectDay(day) {
        console.log(day);
        date = day.date;
    }
</script>

<div class="flex flex-col space-y-4 select-none bg-base-100">
    <div>
        {year}
        {months[month]}
    </div>
    <div class="grid grid-cols-7">
        {#each weekDays as day}
            <div
                class="capitalize bg-debug w-8 h-8 m-1 flex items-center justify-center"
            >
                {day.substring(0, 2)}
            </div>
        {/each}
    </div>
    <div class="grid grid-cols-7">
        {#each calendar.days as day}
            <div
                class:opacity-50={day.moff !== 0}
                class="capitalize bg-debug w-8 h-8 m-1 flex items-center justify-center"
                on:click={() => selectDay(day)}
            >
                {day.inx}
            </div>
        {/each}
    </div>
</div>
