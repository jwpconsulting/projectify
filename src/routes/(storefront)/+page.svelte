<script lang="ts">
    import { _ } from "svelte-i18n";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100 xl:p-24 2xl:p-24">
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div class="">
                <h1 class="mb-8 text-4xl font-bold md:text-6xl">
                    {$_("index.hero-header")}
                </h1>
                <p class="mb-8 max-w-md">
                    {$_("index.hero-text")}
                </p>
                <a href={"/"} class="btn btn-primary btn-md max-w-fit">
                    {$_("index.hero-button")}
                </a>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/hero.png" alt="" />
            </div>
        </div>
        <div class="m-8 grid grid-cols-1 text-center sm:ml-32 sm:mr-32">
            <h2 class="mb-4 text-3xl font-bold md:text-5xl">
                {$_("index.trust-header-1")}
                <span class="text-primary">{$_("index.trust-header-2")}</span>
                {$_("index.trust-header-3")}
                <span class="text-primary">{$_("index.trust-header-4")}</span>
            </h2>
            <h4 class="text-2xl font-bold md:text-3xl">
                {$_("index.trust-text")}
            </h4>
        </div>
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div>
                <h4 class="mb-8 text-xl font-bold sm:mt-24 sm:text-4xl">
                    {$_("index.feature-1-header")}
                </h4>
                <p class="text-l sm:text-l">
                    {$_("index.feature-1-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/task-menu.png" alt="" />
            </div>
        </div>
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div class="sm:order-last">
                <h4 class="mb-8 text-xl font-bold sm:mt-24 sm:text-4xl">
                    {$_("index.feature-2-header")}
                </h4>
                <p class="text-l sm:text-l">
                    {$_("index.feature-2-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/sub-task.png" alt="" />
            </div>
        </div>
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div>
                <h4 class="mb-8 text-xl font-bold sm:mt-24 sm:text-4xl">
                    {$_("index.feature-3-header")}
                </h4>
                <p class="text-l sm:text-l">
                    {$_("index.feature-3-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/filters.png" alt="" />
            </div>
        </div>
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div class="sm:order-last">
                <h4 class="mb-8 text-xl font-bold sm:mt-24 sm:text-4xl">
                    {$_("index.feature-4-header")}
                </h4>
                <p class="text-l sm:text-l">
                    {$_("index.feature-4-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/notifications.png" alt="" />
            </div>
        </div>
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div>
                <h4 class="mb-8 text-xl font-bold sm:mt-24 sm:text-4xl">
                    {$_("index.feature-5-header")}
                </h4>
                <p class="text-l sm:text-l">
                    {$_("index.feature-5-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/responsive.png" alt="" />
            </div>
        </div>
        <div class="page bg base-200 mb-8 mt-8 p-6">
            <div class="mb-12 text-center">
                <h2 class="mb-4 text-2xl font-bold sm:text-4xl">
                    {$_("index.solution-header")}
                </h2>
                <p class="text-l">
                    {$_("index.solution-subtitle")}
                </p>
            </div>
            <div
                class="mb-8 grid grid-cols-1 gap-8 text-center text-xl font-bold underline sm:grid-cols-3 sm:text-3xl"
            >
                <div>
                    <img
                        src="assets/solutions/hero-development.png"
                        alt=""
                        class="mb-4"
                    />
                    <a href={"solutions/development-teams"} class="mt-4">
                        {$_("index.solution-1")}
                    </a>
                </div>
                <div>
                    <img
                        src="assets/solutions/hero-research.png"
                        alt=""
                        class="mb-4"
                    />
                    <a href="solutions/research">
                        {$_("index.solution-2")}
                    </a>
                </div>
                <div>
                    <img
                        src="assets/solutions/hero-project-management.png"
                        alt=""
                        class="mb-4"
                    />
                    <a href="solutions/project-management">
                        {$_("index.solution-3")}
                    </a>
                </div>
            </div>
            <div class="text-l text-center font-bold underline sm:text-xl">
                <a href="/">
                    {$_("index.solution-more")}
                </a>
            </div>
        </div>
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div>
                <h4 class="mb-8 text-xl font-bold sm:mt-24 sm:text-4xl">
                    {$_("index.feature-6-header")}
                </h4>
                <p class="text-l sm:text-l">
                    {$_("index.feature-6-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/privacy.png" alt="" />
            </div>
        </div>
        <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div class="sm:order-last">
                <h4 class="mb-8 text-xl font-bold sm:text-4xl">
                    {$_("index.feature-7-header")}
                </h4>
                <p class="text-l sm:text-l">
                    {$_("index.feature-7-text-1")}
                </p>
                <br />
                <a href="/" class="font-bold underline">Learn more</a>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/landing/open-source.png" alt="" />
            </div>
        </div>
    </main>
</PageLayout>
