<script lang="ts">
    import { _, json } from "svelte-i18n";

    $: sections = [
        {
            title: $_("accessibility.goals.title"),
            text: $_("accessibility.goals.text"),
        },
        {
            title: $_("accessibility.measures.title"),
            list: $json("accessibility.measures.list") as string[],
        },
        {
            title: $_("accessibility.conformance.title"),
            text: $_("accessibility.conformance.text"),
        },
        {
            title: $_("accessibility.compatibility.title"),
            text: $_("accessibility.compatibility.text"),
        },
        {
            title: $_("accessibility.platform.title"),
            text: $_("accessibility.platform.text"),
        },
        {
            title: $_("accessibility.website.title"),
            list: $json("accessibility.website.list") as string[],
        },
        {
            title: $_("accessibility.limitations.title"),
            text: $_("accessibility.limitations.text"),
            list: $json("accessibility.limitations.list") as string[],
        },
        {
            title: $_("accessibility.evaluation.title"),
            text: $_("accessibility.evaluation.text"),
        },
        {
            title: $_("accessibility.contact.title"),
            text: $_("accessibility.contact.text"),
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
                {#if section.text}
                    <p>
                        {section.text}
                    </p>
                {/if}
                {#if section.list}
                    <ul>
                        {#each section.list as item}
                            <li>
                                {item}
                            </li>
                        {/each}
                    </ul>
                {/if}
            </section>
        {/each}
    </div>
</main>
