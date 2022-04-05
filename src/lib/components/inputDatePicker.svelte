<script lang="ts">
    import { dateStringToLocal } from "$lib/utils/date";

    import { getContainer } from "./componentContainer.svelte";

    import DatePicker from "./datePicker.svelte";
    import { getModal } from "./dialogModal.svelte";

    export let placeholder = "Select date";
    export let input;
    export let isEditing = false;

    $: dateStr = input?.value ? dateStringToLocal(input.value) : "";

    async function openDataPicker() {
        let modalRes = await getModal("dataPicker").open(input.value);
        if (modalRes) {
            input.value = modalRes.date;
        }
    }
</script>

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
        isEditing = true;
        openDataPicker();
    }}
/>
