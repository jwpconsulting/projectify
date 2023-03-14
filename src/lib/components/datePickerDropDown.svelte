<script lang="ts">
    import DatePicker from "$lib/components/datePicker.svelte";
    import { getContext } from "svelte";

    const modal = getContext<any>("modal");
    $: date = modal.getData();
</script>

<DatePicker
    {date}
    on:change={({ detail: { date } }) => {
        modal.close({ date });
    }}
/>
