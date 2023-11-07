<script lang="ts">
    export let sections: { id: string; content: string; title: string }[];
</script>

<div class="flex flex-col gap-8">
    {#each sections as section}
        <section id={section.id} class="flex flex-col gap-4">
            <h3 class="text-3xl font-bold">{section.title}</h3>
            <p>
                {section.content}
            </p>
        </section>
    {/each}
</div>
