<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ArrowRight } from "@steeze-ui/heroicons";

    type Solution = {
        href: string;
        title: string;
        image: {
            src: string;
            alt: string;
        };
        description: string;
    };

    let solutions: Solution[];
    $: solutions = [
        {
            href: "/solutions/development-teams",
            title: $_("solutions-page.developer"),
            image: {
                src: "assets/solutions/hero-development.png",
                alt: "TODO",
            },
            description: $_("solutions-page.dev-description"),
        },
        {
            href: "/solutions/research",
            title: $_("solutions-page.research"),
            image: {
                src: "assets/solutions/hero-research.png",
                alt: "TODO",
            },
            description: $_("solutions-page.research-description"),
        },
        {
            href: "/solutions/project-management",
            title: $_("solutions-page.project-management"),
            image: {
                src: "assets/solutions/hero-project-management.png",
                alt: "TODO",
            },
            description: $_("solutions-page.project-description"),
        },
        {
            href: "/solutions/academic",
            title: $_("solutions-page.academic"),
            image: {
                src: "assets/solutions/hero-academic.png",
                alt: "TODO",
            },
            description: $_("solutions-page.academic-description"),
        },
        {
            href: "/solutions/remote",
            title: $_("solutions-page.remote"),
            image: {
                src: "assets/solutions/hero-remote.png",
                alt: "TODO",
            },
            description: $_("solutions-page.remote-description"),
        },
        {
            href: "/solutions/personal-use",
            title: $_("solutions-page.personal-use"),
            image: {
                src: "assets/solutions/hero-personal.png",
                alt: "TODO",
            },
            description: $_("solutions-page.personal-description"),
        },
    ];
</script>

<div>
    <div class="page bg base-200">
        <div class="m-6 grid grid-cols-1 gap-4 pt-4 sm:m-16 sm:grid-cols-2">
            <div>
                <h1 class="mb-8 text-4xl font-bold md:text-6xl">
                    {$_("solutions-page.hero-header")}
                </h1>
                <p class="mb-8 max-w-md">
                    {$_("solutions-page.hero-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/solutions/solution-hero.png" alt="" />
            </div>
        </div>
    </div>
</div>
<div class="m-8 grid grid-cols-1 gap-12 sm:grid-cols-3 sm:gap-8">
    {#each solutions as solution}
        <div>
            <a href={solution.href} class="space-y-4">
                <img
                    src={solution.image.src}
                    alt={solution.image.alt}
                    class="rounded-lg"
                />
                <div class="space-y-4 font-bold">
                    <p>
                        {solution.title}
                    </p>
                    <p class="font-normal">
                        {$_("solutions-page.dev-description")}
                    </p>
                    <div class="flex flex-row items-center gap-2 text-primary">
                        <p>
                            {$_("solutions-page.more")}
                        </p>
                        <Icon
                            src={ArrowRight}
                            theme="outline"
                            class="h-4 w-4"
                        />
                    </div>
                </div>
            </a>
        </div>
    {/each}
</div>
