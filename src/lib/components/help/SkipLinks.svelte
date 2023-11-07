<script lang="ts">
    import { _ } from "svelte-i18n";

    export let sections: { title: string; id: string }[];
</script>

<div class="flex flex-col gap-4 py-8">
    <p class="text-xl font-bold">
        {$_("help.skip")}
    </p>
    <ul class="space-y-1 text-primary">
        {#each sections as section}
            <li>
                <a href={`#${section.id}`}>
                    {section.title}
                </a>
            </li>
        {/each}
    </ul>
</div>
