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
    class="flex select-none flex-col divide-y divide-base-300 overflow-hidden rounded-lg bg-base-100"
>
    <div class="flex items-center justify-center">
        <div
            class="header-btn header-arrow header-arrow-prev"
            on:click={() => setPrevMonth()}
        >
            <div><IconArrowLeft /></div>
        </div>
        <div
            class="header-btn flex h-12 grow items-center justify-center font-bold "
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
                    class="m-0 flex h-8 w-8 items-center justify-center capitalize"
                >
                    {day.substring(0, 2)}
                </div>
            {/each}
        </div>
        <div class="grid grid-cols-7 items-center justify-items-center">
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
        class="header-btn flex h-8 items-center justify-center"
        on:click={() => selectToday()}
    >
        <div class="link text-xs text-primary">Today</div>
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
        @apply flex h-12 w-12 items-center justify-center overflow-hidden p-1;

        // @apply bg-base-200;
        > * {
            @apply flex h-4 w-4 items-center justify-center;
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
            @apply m-0 flex h-8 w-8 cursor-pointer items-center justify-center rounded-full;
            @apply transition-all;
        }

        &.day-today > * {
            @apply border border-primary bg-primary-content text-primary;
        }

        &:hover > * {
            @apply bg-base-300 text-base-100;
            @apply scale-75;
            @apply border-0 ring-0;
        }
        &.day-disbled > * {
            @apply opacity-50;
        }
        &.day-selected {
            > * {
                @apply pointer-events-none bg-primary text-primary-content;
            }
            &:hover > * {
                @apply cursor-default bg-primary text-primary-content;
                @apply scale-100;
            }
        }
    }
</style>
