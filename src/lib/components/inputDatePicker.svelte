<script lang="ts">
    import { _ } from "svelte-i18n";
    import { dateStringToLocal } from "$lib/utils/date";
    // import { createEventDispatcher } from "svelte";
    import IconCalendar from "$lib/components/icons/icon-calendar.svelte";
    import type { Input } from "$lib/types/ui";

    export let placeholder = $_("select-date");
    export let input: Input;
    // TODO export let isEditing = false;

    // const dispatch = createEventDispatcher();

    $: dateStr = input?.value ? dateStringToLocal(input.value) : "";

    async function openDataPicker() {
        // TODO let modalRes = await getModal("dataPicker").open(input.value);
        // TODO if (modalRes) {
        // TODO     input.value = modalRes.date;
        // TODO     isEditing = true;
        // TODO     dispatch("change", { date: input.value });
        // TODO }
    }
</script>

<div class="relative">
    <input
        tabindex="0"
        type="text"
        name={input.name}
        {placeholder}
        class="input input-bordered w-full select-none caret-transparent"
        value={dateStr}
        on:keypress={(e) => {
            e.preventDefault();
        }}
        on:focus={() => {
            openDataPicker();
        }}
    />

    <button
        on:click={() => openDataPicker()}
        class="btn btn-square btn-ghost absolute right-0 top-0 rounded-l-none"
        ><IconCalendar /></button
    >
</div>
