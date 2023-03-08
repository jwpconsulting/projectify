<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/figma/buttons/Button.svelte";
    import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";
    import SquovalIcon from "$lib/figma/buttons/SquovalIcon.svelte";

    // Very much WIP TODO
</script>

<div class="flex flex-row items-center justify-between">
    <div class="flex flex-row items-center gap-6">
        <div class="shrink-0">
            <CircleIcon size="medium" icon="close" disabled={false} />
        </div>
        <div class="text-sm font-bold text-utility">
            Board &gt; Section &gt; #1
        </div>
    </div>
    <div class="flex flex-row items-center gap-4">
        <SquovalIcon icon="dotsVertical" state="active" />
        <Button
            color="blue"
            size="small"
            disabled={true}
            style={{ kind: "primary" }}
            label={$_("task-screen.save")}
        />
    </div>
</div>
