<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ArrowRight } from "@steeze-ui/heroicons";
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
    <div>
        <a href="/solutions/development-teams" class="space-y-4">
            <img
                src="https://placedog.net/500/280"
                alt=""
                class="rounded-lg"
            />
            <div class="space-y-4 font-bold">
                <p>
                    {$_("solutions-page.developer")}
                </p>
                <p class="font-normal">
                    {$_("solutions-page.dev-description")}
                </p>
                <div class="flex flex-row items-center gap-2 text-primary">
                    <p>
                        {$_("solutions-page.more")}
                    </p>
                    <Icon src={ArrowRight} theme="outline" class="h-4 w-4" />
                </div>
            </div>
        </a>
    </div>
    <div>
        <a href="/solutions/project-management" class="space-y-4">
            <img
                src="https://placedog.net/500/280"
                alt=""
                class="rounded-lg"
            />
            <div class="space-y-4 font-bold">
                <p>
                    {$_("solutions-page.project-management")}
                </p>
                <p class="font-normal">
                    {$_("solutions-page.project-description")}
                </p>
                <div class="flex flex-row items-center gap-2 text-primary">
                    <p>
                        {$_("solutions-page.more")}
                    </p>
                    <Icon src={ArrowRight} theme="outline" class="h-4 w-4" />
                </div>
            </div>
        </a>
    </div>
    <div>
        <a href="/solutions/research" class="space-y-4">
            <img
                src="https://placedog.net/500/280"
                alt=""
                class="rounded-lg"
            />
            <div class="space-y-4 font-bold">
                <p>
                    {$_("solutions-page.research")}
                </p>
                <p class="font-normal">
                    {$_("solutions-page.research-description")}
                </p>
                <div class="flex flex-row items-center gap-2 text-primary">
                    <p>
                        {$_("solutions-page.more")}
                    </p>
                    <Icon src={ArrowRight} theme="outline" class="h-4 w-4" />
                </div>
            </div>
        </a>
    </div>
    <div>
        <a href="/solutions/remote" class="space-y-4">
            <img
                src="https://placedog.net/500/280"
                alt=""
                class="rounded-lg"
            />
            <div class="space-y-4 font-bold">
                <p>
                    {$_("solutions-page.remote")}
                </p>
                <p class="font-normal">
                    {$_("solutions-page.remote-description")}
                </p>
                <div class="flex flex-row items-center gap-2 text-primary">
                    <p>
                        {$_("solutions-page.more")}
                    </p>
                    <Icon src={ArrowRight} theme="outline" class="h-4 w-4" />
                </div>
            </div>
        </a>
    </div>
    <div>
        <a href="/solutions/academic" class="space-y-4">
            <img
                src="https://placedog.net/500/280"
                alt=""
                class="rounded-lg"
            />
            <div class="space-y-4 font-bold">
                <p>
                    {$_("solutions-page.academic")}
                </p>
                <p class="font-normal">
                    {$_("solutions-page.academic-description")}
                </p>
                <div class="flex flex-row items-center gap-2 text-primary">
                    <p>
                        {$_("solutions-page.more")}
                    </p>
                    <Icon src={ArrowRight} theme="outline" class="h-4 w-4" />
                </div>
            </div>
        </a>
    </div>
    <div>
        <a href="/solutions/planning" class="space-y-4">
            <img
                src="https://placedog.net/500/280"
                alt=""
                class="rounded-lg"
            />
            <div class="space-y-4 font-bold">
                <p>
                    {$_("solutions-page.planning")}
                </p>
                <p class="font-normal">
                    {$_("solutions-page.planning-description")}
                </p>
                <div class="flex flex-row items-center gap-2 text-primary">
                    <p>
                        {$_("solutions-page.more")}
                    </p>
                    <Icon src={ArrowRight} theme="outline" class="h-4 w-4" />
                </div>
            </div>
        </a>
    </div>
</div>
