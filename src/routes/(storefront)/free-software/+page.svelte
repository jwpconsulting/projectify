<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
</script>

<HeroLayout>
    <div slot="hero">
        <h1 class="text-3xl font-bold">{$_("free-software.hero")}</h1>
    </div>
    <div slot="content" class="prose">
        <p>{$_("free-software.header")}</p>
        <!-- make sure to add future authors here -->
        <ul>
            <li>Copyright 2021-2023 JWP Consulting GK</li>
        </ul>
        <p>{$_("free-software.license")}</p>
        <p>{$_("free-software.warranty")}</p>
        <p>{$_("free-software.find-copy")}</p>
        <ul>
            <li>
                <a
                    href="https://github.com/jwp-consulting/projectify-frontend"
                >
                    {$_("free-software.source.frontend")}
                </a>
            </li>
            <li>
                <a href="https://github.com/jwp-consulting/projectify-backend">
                    {$_("free-software.source.backend")}
                </a>
            </li>
        </ul>
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        <p>{@html $_("free-software.trademark")}</p>
    </div>
</HeroLayout>
