<script lang="ts">
    // TODO: Support onInteract
    import { Plus, CheckCircle } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { number, _ } from "svelte-i18n";

    import SubTaskProgressBar from "$lib/figma/screens/task/SubTaskProgressBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";

    export let progress: number | undefined;
    export let subTaskAssignment: SubTaskAssignment | undefined = undefined;
    // TODO make buttons do something
</script>

<div class="flex flex-col gap-4">
    <div class="flex flex-row justify-between">
        <div class="flex flex-row gap-4">
            <div>
                <Icon src={CheckCircle} class="h-6" theme="outline" />
            </div>
            <!-- TODO add a text saying something like "Sub task completion is: ... -->
            {#if progress !== undefined}
                <div>{$number(progress, { style: "percent" })}</div>
            {/if}
            <!-- TODO: and if there is no progress, display: This task has no sub tasks -->
        </div>
        {#if subTaskAssignment}
            <div class="flex flex-row items-center gap-6">
                <Button
                    style={{
                        kind: "tertiary",
                        icon: { position: "left", icon: Plus },
                    }}
                    color="blue"
                    size="medium"
                    label={$_("task-screen.sub-tasks.add-sub-task")}
                    action={{
                        kind: "button",
                        action: subTaskAssignment.addSubTask,
                    }}
                />
                <SquovalIcon
                    icon="ellipsis"
                    state="active"
                    action={{ kind: "button", action: console.error }}
                />
            </div>
        {/if}
    </div>
    {#if progress !== undefined}
        <SubTaskProgressBar {progress} />
    {/if}
</div>
