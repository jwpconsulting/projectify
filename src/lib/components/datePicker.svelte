<script lang="ts">
    import { getCalendar, months, weekDays } from "$lib/utils/date";

    export let date = new Date();

    $: year = date.getFullYear();
    $: month = date.getMonth();
    $: calendar = getCalendar(year, month);

    let today = new Date();
    today = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    function selectDay(day) {
        date = day.date;
    }
</script>

<div class="p-2 flex flex-col select-none bg-base-100 rounded-lg">
    <div class="font-bold p-2 flex space-x-2">
        <div>{year}</div>
        <div>{months[month]}</div>
    </div>
    <div class="px-2 mb-1 grid grid-cols-7">
        {#each weekDays as day}
            <div
                class="capitalize w-8 h-8 m-0 flex items-center justify-center"
            >
                {day.substring(0, 2)}
            </div>
        {/each}
    </div>
    <div class="px-2 pb-1 grid grid-cols-7 justify-items-center items-center">
        {#each calendar.days as day}
            <div
                class:day-today={day.date.getTime() === today.getTime()}
                class:day-selected={day.date.getTime() === date.getTime()}
                class:day-disbled={day.moff !== 0}
                class="day"
                on:click={() => selectDay(day)}
            >
                <div>{day.inx}</div>
            </div>
        {/each}
    </div>
</div>

<style lang="scss">
    .day {
        > * {
            @apply text-sm capitalize;
            @apply w-8 h-8 m-0 flex items-center justify-center rounded-full cursor-pointer;
            @apply transition-all;
        }

        &.day-today > * {
            @apply bg-primary-content text-primary border border-primary;
        }

        &:hover > * {
            @apply bg-base-300 text-base-100;
            @apply scale-75;
            @apply ring-0 border-0;
        }
        &.day-disbled > * {
            @apply opacity-50;
        }
        &.day-selected {
            > * {
                @apply bg-primary text-primary-content pointer-events-none;
            }
            &:hover > * {
                @apply bg-primary text-primary-content cursor-default;
                @apply scale-100;
            }
        }
    }
</style>
