<script lang="ts">
    import { _ } from "svelte-i18n";

    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    export let description: string | undefined;
    export let readonly = false;
</script>

<InputField
    name="description"
    style={{ kind: "field", inputType: "text" }}
    bind:value={description}
    placeholder={$_("task-screen.description")}
    {readonly}
/>
