<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Minus } from "@steeze-ui/heroicons";
    import InputField from "$lib/figma/input-fields/InputField.svelte";

    export let title: string | undefined;
</script>

<div class="flex flex-row items-center gap-2">
    <Icon src={Minus} class="w-6" theme="outline" />
    <InputField
        name="title"
        style={{ kind: "field", inputType: "text" }}
        bind:value={title}
        placeholder={$_("task-screen.new-task-name")}
    />
</div>
