<script lang="ts">
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { SubTaskState } from "$lib/figma/types";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import type { CreateOrUpdateSubTask } from "$lib/types/ui";

    export let state: SubTaskState;
    export let createOrUpdateSubTask: CreateOrUpdateSubTask;
    // TODO missing:
    // proper input field
    // Wire into rest of application
    // Sub tasks need assignees

    let title: string | undefined = undefined;
    let done: boolean | undefined = undefined;

    $: {
        // XXX need to set isInitialized flag here?
        if (createOrUpdateSubTask.kind == "update") {
            const { update: subTask } = createOrUpdateSubTask;
            title = subTask.title;
            done = subTask.done;
        }
    }
</script>

<div class="flex w-full flex-row items-center justify-between gap-2 px-2 py-1">
    <div class="flex flex-row items-center gap-2">
        <Checkbox checked={done ?? false} disabled={false} contained={false} />
        <!-- XXX should be only editable when in edit mode -->
        <InputField
            style={{ kind: "subTask" }}
            placeholder={$_("task-screen.enter-a-subtask")}
            name="sub-task"
            bind:value={title}
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
