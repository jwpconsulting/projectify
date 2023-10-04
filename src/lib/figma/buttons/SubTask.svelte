<script lang="ts">
    // TODO missing:
    // proper input field
    // Wire into rest of application
    // Sub tasks need assignees
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import type { SubTask } from "$lib/types/workspace";

    export let subTask: Partial<SubTask>;

    const { title, done } = subTask;

    const showEditButtons = false;
</script>

<div class="flex w-full flex-row items-center justify-between gap-2 px-2 py-1">
    <div class="flex grow flex-row items-center gap-2">
        <Checkbox checked={done ?? false} disabled={true} contained={false} />
        <!-- XXX should be only editable when in edit mode -->
        <div class="grow">
            <InputField
                style={{ kind: "subTask" }}
                placeholder={$_("task-screen.enter-a-subtask")}
                name="sub-task"
                value={title}
                readonly
            />
        </div>
    </div>
    {#if showEditButtons}
        <div class="flex flex-row gap-2">
            <CircleIcon
                size="medium"
                icon="up"
                action={{ kind: "button", action: console.error }}
            />
            <CircleIcon
                size="medium"
                icon="down"
                action={{ kind: "button", action: console.error }}
            />
            <CircleIcon
                size="medium"
                icon="delete"
                action={{ kind: "button", action: console.error }}
            />
        </div>
    {/if}
</div>
