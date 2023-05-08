<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { MenuAlt1 } from "@steeze-ui/heroicons";
    import InputField from "$lib/figma/input-fields/InputField.svelte";

    export let description: string | undefined;
</script>

<div class="flex flex-row items-center gap-2">
    <Icon src={MenuAlt1} class="w-6" theme="outline" />
    <InputField
        name="description"
        style={{ kind: "field", inputType: "text" }}
        bind:value={description}
        placeholder={$_("task-screen.description")}
    />
</div>
