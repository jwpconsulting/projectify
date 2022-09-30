<script lang="ts">
    import { dateStringToLocal } from "$lib/utils/date";
    import { createEventDispatcher } from "svelte";
    import { _ } from "svelte-i18n";
    import { getModal } from "./dialogModal.svelte";
    import IconCalendar from "./icons/icon-calendar.svelte";
    import type { Input } from "$lib/types/ui";

    export let placeholder = $_("select-date");
    export let input: Input;
    export let isEditing = false;

    const dispatch = createEventDispatcher();

    $: dateStr = input?.value ? dateStringToLocal(input.value) : "";

    async function openDataPicker() {
        let modalRes = await getModal("dataPicker").open(input.value);
        if (modalRes) {
            input.value = modalRes.date;
            isEditing = true;
            dispatch("change", { date: input.value });
        }
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
        class="btn btn-square btn-ghost absolute top-0 right-0 rounded-l-none"
        ><IconCalendar /></button
    >
</div>
