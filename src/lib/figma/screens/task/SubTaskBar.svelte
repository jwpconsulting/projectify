<script lang="ts">
    // TODO: Support onInteract
    import { CheckCircle } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import SubTaskProgressBar from "$lib/figma/screens/task/SubTaskProgressBar.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";

    export let progress: number;
    export let subTaskAssignment: SubTaskAssignment | undefined = undefined;

    let progressString: string;
    $: {
        if (progress < 0 || progress > 100) {
            throw new Error(
                `Progress must be between 0 and 100. Given: ${progress}`
            );
        }
        progressString = `${progress}%`;
    }
    // TODO make buttons do something
</script>

<div class="flex flex-col gap-4">
    <div class="flex flex-row justify-between">
        <div class="flex flex-row gap-4">
            <div>
                <Icon src={CheckCircle} class="h-6" theme="outline" />
            </div>
            <div>{progressString}</div>
        </div>
        {#if subTaskAssignment}
            <div class="flex flex-row gap-6">
                <SquovalIcon
                    icon="plus"
                    state="active"
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
    <SubTaskProgressBar {progress} />
</div>
