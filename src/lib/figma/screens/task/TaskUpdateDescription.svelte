<script lang="ts">
    import { _ } from "svelte-i18n";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    export let description: string | undefined;
</script>

<div class="flex flex-row items-center gap-2">
    <InputField
        name="description"
        style={{ kind: "field", inputType: "text" }}
        bind:value={description}
        placeholder={$_("task-screen.description")}
    />
</div>
