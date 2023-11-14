<script lang="ts">
    import { _, json } from "svelte-i18n";

    $: sections = [
        {
            title: $_("accessibility.goals.title"),
            contents: [$_("accessibility.goals.text")],
        },
        {
            title: $_("accessibility.measures.title"),
            listItems: $json("accessibility.measures.list") as string[],
        },
        {
            title: $_("accessibility.conformance.title"),
            contents: [$_("accessibility.conformance.text")],
        },
        {
            title: $_("accessibility.compatibility.title"),
            contents: [$_("accessibility.compatibility.text")],
        },
        {
            title: $_("accessibility.platform.title"),
            contents: [$_("accessibility.platform.text")],
        },
        {
            title: $_("accessibility.website.title"),
            listItems: $json("accessibility.website.list") as string[],
        },
        {
            title: $_("accessibility.limitations.title"),
            contents: [$_("accessibility.limitations.text")],
            listItems: $json("accessibility.limitations.list") as string[],
        },
        {
            title: $_("accessibility.evaluation.title"),
            contents: [$_("accessibility.evaluation.text")],
        },
        {
            title: $_("accessibility.contact.title"),
            contents: [$_("accessibility.contact.text")],
        },
    ];
</script>

<main class="bg-base-100">
    <div class="page bg-base-200">
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <h1 class="mb-8 text-4xl font-bold md:text-6xl">
                {$_("accessibility.hero.title")}
            </h1>
            <div class="max-w-md">
                <img
                    src="/assets/accessibility/accessibility-hero.png"
                    alt={$_("accessibility.hero.illustration.alt")}
                />
            </div>
        </div>
    </div>

    <div class="flex flex-col justify-center p-16">
        {#each sections as section}
            <section class="flex flex-col gap-2">
                <h2 class="pt-4 text-3xl font-bold">
                    {section.title}
                </h2>
                {#if section.contents}
                    {#each section.contents as content}
                        <p>
                            {content}
                        </p>
                    {/each}
                {/if}
                {#if section.listItems}
                    <ul>
                        {#each section.listItems as listItem}
                            <li>
                                {listItem}
                            </li>
                        {/each}
                    </ul>
                {/if}
            </section>
        {/each}
    </div>
</main>
