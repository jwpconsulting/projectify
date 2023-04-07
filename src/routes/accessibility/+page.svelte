<script lang="ts">
    import { _ } from "svelte-i18n";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";

    $: sections = [
        {
            title: $_("accessibility.a-goals"),
            contents: [$_("accessibility.a-goals-text")],
        },
        {
            title: $_("accessibility.a-measures"),
            listItems: [
                $_("accessibility.a-measures-list-1"),
                $_("accessibility.a-measures-list-2"),
                $_("accessibility.a-measures-list-3"),
                $_("accessibility.a-measures-list-4"),
                $_("accessibility.a-measures-list-5"),
            ],
        },
        {
            title: $_("accessibility.a-conformance"),
            contents: [$_("accessibility.a-conformance-text")],
        },
        {
            title: $_("accessibility.a-compatibility"),
            contents: [$_("accessibility.a-compatibility-text")],
        },
        {
            title: $_("accessibility.a-platform"),
            contents: [$_("accessibility.a-platform-text")],
        },
        {
            title: $_("accessibility.a-website"),
            listItems: [
                $_("accessibility.a-website-list-1"),
                $_("accessibility.a-website-list-2"),
                $_("accessibility.a-website-list-3"),
                $_("accessibility.a-website-list-4"),
                $_("accessibility.a-website-list-5"),
                $_("accessibility.a-website-list-6"),
            ],
        },
        {
            title: $_("accessibility.a-limitations"),
            contents: [$_("accessibility.a-limitations-text")],
            listItems: [
                $_("accessibility.a-limitations-list-1"),
                $_("accessibility.a-limitations-list-2"),
            ],
        },
        {
            title: $_("accessibility.a-evaluation"),
            contents: [$_("accessibility.a-evaluation-text")],
        },
        {
            title: $_("accessibility.a-contact"),
            contents: [$_("accessibility.a-contact-text")],
        },
    ];
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100">
        <div>
            <div class="page bg base-200">
                <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
                    <div class="/">
                        <h1 class="mb-8 text-4xl font-bold md:text-6xl">
                            {$_("accessibility.hero-header")}
                        </h1>
                    </div>
                    <div class="min-w-full max-w-md">
                        <img
                            src="/assets/accessibility/accessibility-hero.png"
                            alt=""
                        />
                    </div>
                </div>
            </div>

            <div class="m-16 flex flex-col justify-center">
                {#each sections as section}
                    <section class=" items-center text-3xl font-bold">
                        {section.title}
                        {#if section.contents}
                            {#each section.contents as content}
                                <p class="items-center text-sm font-bold">
                                    {content}
                                </p>
                            {/each}
                        {/if}
                        {#if section.listItems}
                            <ul class="list-disc">
                                {#each section.listItems as listItem}
                                    <li class="items-center text-sm font-bold">
                                        {listItem}
                                    </li>
                                {/each}
                            </ul>
                        {/if}
                    </section>
                {/each}
            </div>
        </div>
    </main>
</PageLayout>
