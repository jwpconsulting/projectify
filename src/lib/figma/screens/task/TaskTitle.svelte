<script lang="ts">
    // TODO rename to just Title or maybe TaskTitle
    import { _ } from "svelte-i18n";

    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    export let title: string | undefined;
    export let onInteract: (() => void) | undefined = undefined;

    export let readonly = false;
</script>

<InputField
    name="title"
    style={{ kind: "field", inputType: "text" }}
    bind:value={title}
    placeholder={$_("task-screen.new-task-name")}
    onClick={onInteract}
    {readonly}
    required
/>
