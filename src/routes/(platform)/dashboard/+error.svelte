<script lang="ts">
    import { _ } from "svelte-i18n";

    import { page } from "$app/stores";

    $: error = $page.error ?? {
        message: "No error was found, this is unexpected!",
    };
</script>

<div class="flex flex-col gap-6 p-16">
    <header class="flex flex-col gap-4">
        <h1 class="text-3xl font-bold">
            {$_("dashboard.error.title")}

            {error.message}
        </h1>
    </header>
    <main class="flex flex-col gap-4">
        <p>
            {$_("dashboard.error.description")}
        </p>
        <code>
            {error.message}
        </code>
        <p>
            {$_("dashboard.error.what-to-do.message")}
        </p>
        <ol>
            {#each $_("dashboard.error.what-to-do.options") as option}
                <li>
                    {option}
                </li>
            {/each}
        </ol>
    </main>
</div>
