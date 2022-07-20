<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    export let label: string;
    export let icon: IconSource;
    export let open = true;

    function onOpen() {
        open = !open;
    }
</script>

<button
    class="group w-full rounded-lg border-base-content p-0.5 focus:border focus:p-px dark:border-base-100"
    on:click={onOpen}
>
    <div
        class="text-task-update-text flex flex-row justify-between px-4 py-2 group-hover:text-base-content"
    >
        <div class="flew-row flex items-center gap-2">
            <Icon src={icon} theme="outline" class="h-5 w-5" />
            <div class="text-xs font-bold uppercase">
                {label}
            </div>
        </div>
        <div class="h-4 w-4">
            <Icon
                src={open ? ChevronUp : ChevronDown}
                theme="outline"
                class="h-5 w-5"
            />
        </div>
    </div>
</button>
