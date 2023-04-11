<script lang="ts">
    import { _ } from "svelte-i18n";
    import CheckBox from "$lib/figma/select-controls/CheckBox.svelte";
    import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { SubTaskState } from "$lib/figma/types";
    import type { SubTask } from "$lib/types/workspace";

    export let state: SubTaskState;
    export let subTask: SubTask;
    // TODO missing:
    // proper input field
    // Wire into rest of application
    // Sub tasks need assignees
</script>

<div class="flex w-full flex-row items-center justify-between gap-2 px-2 py-1">
    <div class="flex flex-row items-center gap-2">
        <CheckBox checked={subTask.done} disabled={false} contained={false} />
        <InputField
            style={{ kind: "subTask" }}
            placeholder={$_("task-screen.enter-a-subtask")}
            name="sub-task"
        />
    </div>
    {#if state === "normal"}
        <AvatarVariant
            size="small"
            content={{ kind: "multiple", users: [null] }}
        />
    {:else}
        <div class="flex flex-row gap-2">
            <CircleIcon
                size="medium"
                icon="up"
                disabled={false}
                action={{ kind: "button", action: console.error }}
            />
            <CircleIcon
                size="medium"
                icon="down"
                disabled={false}
                action={{ kind: "button", action: console.error }}
            />
            <CircleIcon
                size="medium"
                icon="delete"
                disabled={false}
                action={{ kind: "button", action: console.error }}
            />
        </div>
    {/if}
</div>
