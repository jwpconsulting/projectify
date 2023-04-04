<script lang="ts">
    import DatePicker from "$lib/components/datePicker.svelte";
    let date: Date;
</script>

<DatePicker
    {date}
    on:change={({ detail: { date } }) => {
        console.error(date);
    }}
/>
