<script lang="ts">
    import { getCalendar, months, weekDays } from "$lib/utils/date";
    import { createEventDispatcher } from "svelte";
    import IconArrowLeft from "./icons/icon-arrow-left.svelte";
    import IconArrowRight from "./icons/icon-arrow-right.svelte";
    import { scale } from "svelte/transition";
    import { quintOut } from "svelte/easing";

    const dispatch = createEventDispatcher();

    export let date: Date | null = null;
    $: {
        if (!date) {
            date = new Date();
        }
        if (typeof date === "string") {
            date = new Date(date);
        }
    }

    let year: number;
    let month: number;

    $: {
        if (date) {
            year = date.getFullYear();
            month = date.getMonth();
        }
    }
    $: calendar = getCalendar(year, month);

    let today = new Date();
    today = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    let viewMode: "day" | "month" | "year" = "day";

    function selectDate(d: Date | null) {
        date = d;
        dispatch("change", { date });
    }

    function selectToday() {
        selectDate(today);
    }

    function selectMonth(m: number) {
        if (!date) {
            throw new Error("Expected date");
        }
        viewMode = "day";
        date.setMonth(m);
        date.setFullYear(year);
        selectDate(date);
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

    function setNextYear() {
        year++;
        calendar = getCalendar(year, month);
    }
    function setPrevYear() {
        year--;
        calendar = getCalendar(year, month);
    }

    function onNext() {
        if (viewMode === "day") {
            setNextMonth();
        } else if (viewMode === "month") {
            setNextYear();
        }
    }

    function onPrev() {
        if (viewMode === "day") {
            setPrevMonth();
        } else if (viewMode === "month") {
            setPrevYear();
        }
    }

    function setViewMode(mode: "day" | "month" | "year") {
        viewMode = mode;
    }

    function onHeaderClick() {
        if (viewMode === "day") {
            setViewMode("month");
        } else {
            setViewMode("day");
        }
    }
</script>

<div
    class="relative flex select-none flex-col divide-y divide-base-300 overflow-hidden rounded-lg bg-base-100 shadow-md"
>
    <div class="flex items-center justify-center">
        <div
            class="cal-btn header-arrow header-arrow-prev"
            on:click={() => onPrev()}
            on:keydown={() => onPrev()}
        >
            <div><IconArrowLeft /></div>
        </div>
        <div
            class="cal-btn flex h-12 grow items-center justify-center font-bold"
            on:click={() => onHeaderClick()}
            on:keydown={() => onHeaderClick()}
        >
            <div class="flex space-x-2">
                <div>{year}</div>
                {#if viewMode !== "month"}
                    <div>{months[month]}</div>
                {/if}
            </div>
        </div>
        <div
            class="cal-btn header-arrow header-arrow-next"
            on:click={() => onNext()}
            on:keydown={() => onNext()}
        >
            <div><IconArrowRight /></div>
        </div>
    </div>

    <div class="relative overflow-hidden p-4">
        <div class="grid grid-cols-7 justify-items-center">
            {#each weekDays as day, inx}
                <div
                    class:weekend={inx >= 5}
                    class="m-0 flex h-8 w-8 items-center justify-center font-medium capitalize"
                >
                    {day.substring(0, 2)}
                </div>
            {/each}
        </div>
        <div class="grid grid-cols-7 items-center justify-items-center">
            {#each calendar.days as day, inx}
                {#if date}
                    <div
                        class:day-today={day.date.getTime() ===
                            today.getTime()}
                        class:day-selected={day.date.getTime() ===
                            date.getTime()}
                        class:day-disbled={day.moff !== 0}
                        class:weekend={inx % 7 >= 5}
                        class="day"
                        on:click={() => selectDate(day.date)}
                        on:keydown={() => selectDate(day.date)}
                    >
                        <div>{day.inx}</div>
                    </div>
                {/if}
            {/each}
        </div>

        {#if viewMode === "month"}
            <div
                class="absolute top-0 left-0 grid h-full w-full grid-cols-3 grid-rows-4 bg-base-100"
                transition:scale={{
                    duration: 300,
                    delay: 0,
                    opacity: 0,
                    start: 1.2,
                    easing: quintOut,
                }}
            >
                {#each months as m, inx}
                    <div
                        class:active={months[month] === m}
                        class="cal-btn active flex items-center justify-center capitalize"
                        on:click={() => selectMonth(inx)}
                        on:keydown={() => selectMonth(inx)}
                    >
                        <div>{m.substring(0, 3)}</div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
    <footer class="flex divide-x divide-base-300">
        <div
            class="cal-btn flex h-8 grow items-center justify-center text-primary"
            on:click={() => selectDate(null)}
            on:keydown={() => selectDate(null)}
        >
            <div class="text-xs ">Clear</div>
        </div>
        {#if date}
            <div
                class:active={date.getTime() === today.getTime()}
                class="cal-btn flex h-8 grow items-center justify-center text-primary"
                on:click={() => selectToday()}
                on:keydown={() => selectToday()}
            >
                <div class="text-xs ">Today</div>
            </div>
        {/if}
    </footer>
</div>

<style lang="scss">
    .cal-btn {
        @apply cursor-pointer;
        > * {
            @apply transition-all;
        }
        &:hover {
            @apply bg-base-200;
        }

        &.active {
            @apply bg-primary text-primary-content shadow-md;
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

    .weekend {
        @apply text-primary-focus;
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
            @apply bg-primary-focus text-base-100;
            @apply border-0 ring-0;
        }
        &.day-disbled > * {
            @apply opacity-50;
        }
        &.day-selected {
            > * {
                @apply pointer-events-none bg-primary text-primary-content shadow-md;
            }
            &:hover > * {
                @apply cursor-default bg-primary text-primary-content;
                @apply scale-100;
            }
        }
    }
</style>
