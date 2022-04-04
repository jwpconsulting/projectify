<script lang="ts">
    import DatePicker from "./datePicker.svelte";

    export let placeholder = "Select date";
    export let input;
    export let isEditing = false;

    let dataPickerEl;
</script>

<div class="dropdown-end dropdown w-full">
    <input
        tabindex="0"
        type="text"
        name={input.name}
        {placeholder}
        class="input input-bordered w-full select-none caret-transparent"
        bind:value={input.value}
        on:keypress={(e) => {
            e.preventDefault();
        }}
        on:focus={() => {
            isEditing = true;
        }}
    />
    <div
        tabindex="0"
        class="dropdown-content rounded-box relative w-64"
        bind:this={dataPickerEl}
    >
        <DatePicker
            date={input.value}
            on:change={({ detail: { date } }) => {
                isEditing = true;
                dataPickerEl.blur();
                input.value = date;
            }}
        />
    </div>
</div>
