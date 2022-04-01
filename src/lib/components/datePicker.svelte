<script lang="ts">
    import { getCalendar, months, weekDays } from "$lib/utils/date";
    import { createEventDispatcher } from "svelte";
    import IconArrowLeft from "./icons/icon-arrow-left.svelte";
    import IconArrowRight from "./icons/icon-arrow-right.svelte";

    const dispatch = createEventDispatcher();

    export let date = new Date();

    $: year = date.getFullYear();
    $: month = date.getMonth();
    $: calendar = getCalendar(year, month);

    let today = new Date();
    today = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    function selectDate(d) {
        date = d;
        dispatch("date-changed", { date });
    }

    function selectToday() {
        selectDate(today);
    }

    function setNextMonth() {
        month++;
        if (month > 11) {
            month = 0;
            year++;
        }
        calendar = getCalendar(year, month);
    }

    function setPrevMonth() {
        month--;
        if (month < 0) {
            month = 11;
            year--;
        }
        calendar = getCalendar(year, month);
    }
</script>

<div
    class="flex flex-col select-none bg-base-100 rounded-lg overflow-hidden divide-y divide-base-300"
>
    <div class="flex justify-center items-center">
        <div
            class="header-btn header-arrow header-arrow-prev"
            on:click={() => setPrevMonth()}
        >
            <div><IconArrowLeft /></div>
        </div>
        <div
            class="header-btn grow h-12 font-bold flex justify-center items-center "
        >
            <div class="flex space-x-2">
                <div>{year}</div>
                <div>{months[month]}</div>
            </div>
        </div>
        <div
            class="header-btn header-arrow header-arrow-next"
            on:click={() => setNextMonth()}
        >
            <div><IconArrowRight /></div>
        </div>
    </div>

    <div class="p-4">
        <div class="grid grid-cols-7">
            {#each weekDays as day}
                <div
                    class="capitalize w-8 h-8 m-0 flex items-center justify-center"
                >
                    {day.substring(0, 2)}
                </div>
            {/each}
        </div>
        <div class="grid grid-cols-7 justify-items-center items-center">
            {#each calendar.days as day}
                <div
                    class:day-today={day.date.getTime() === today.getTime()}
                    class:day-selected={day.date.getTime() === date.getTime()}
                    class:day-disbled={day.moff !== 0}
                    class="day"
                    on:click={() => selectDate(day.date)}
                >
                    <div>{day.inx}</div>
                </div>
            {/each}
        </div>
    </div>
    <div
        class="header-btn h-8 flex justify-center items-center"
        on:click={() => selectToday()}
    >
        <div class="text-xs text-primary link">Today</div>
    </div>
</div>

<style lang="scss">
    .header-btn {
        @apply cursor-pointer;
        > * {
            @apply transition-all;
        }
        &:hover {
            @apply bg-base-200;
            > * {
                @apply scale-90;
            }
        }
    }
    .header-arrow {
        @apply flex items-center justify-center p-1 overflow-hidden w-12 h-12;

        // @apply bg-base-200;
        > * {
            @apply flex items-center justify-center w-4 h-4;
        }

        &.header-arrow-prev {
            @apply pl-3;
        }
        &.header-arrow-next {
            @apply pr-3;
        }
    }
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
