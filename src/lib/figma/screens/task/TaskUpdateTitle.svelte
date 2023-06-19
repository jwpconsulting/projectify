<script lang="ts">
    // TODO rename to just Title or maybe TaskTitle
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Minus } from "@steeze-ui/heroicons";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    export let title: string | undefined;

    export let readonly = false;
</script>

<div class="flex flex-row items-center gap-2">
    <Icon src={Minus} class="w-6" theme="outline" />
    {#if readonly}
        <div>{title}</div>
    {:else}
        <InputField
            name="title"
            style={{ kind: "field", inputType: "text" }}
            bind:value={title}
            placeholder={$_("task-screen.new-task-name")}
        />
    {/if}
</div>
