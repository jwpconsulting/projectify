<script lang="ts">
    import { _ } from "svelte-i18n";
</script>

<dl class="inline-grid max-w-sm auto-cols-min grid-cols-2 items-center gap-8">
    <dt class="font-bold">
        {$_("task-screen.task-title")}
    </dt>
    <dd>
        <slot name="title" />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.assignee")}
    </dt>
    <dd>
        <slot name="assignee" />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.labels")}
    </dt>
    <dd>
        <slot name="labels" />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.section")}
    </dt>
    <dd>
        <slot name="section" />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.due-date")}
    </dt>
    <dd>
        <slot name="due-date" />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.description")}
    </dt>
    <dd>
        <slot name="description" />
    </dd>
</dl>
