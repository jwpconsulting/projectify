<script lang="ts">
    import { _ } from "svelte-i18n";

    import PolyLogo from "$lib/figma/navigation/polylogo.svg";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { signUpUrl } from "$lib/urls/user";
</script>

<footer class="flex w-full flex-col gap-6 border-t border-border p-8">
    <div class="flex flex-col gap-8 sm:flex-row">
        <div class="flex flex-col gap-6">
            <div class="flex flex-col gap-2">
                <div class="flex flex-row items-center gap-2">
                    <img
                        src={PolyLogo}
                        alt={$_("navigation.footer.logo.alt")}
                    />
                </div>
                <p>{$_("navigation.footer.logo.heading")}</p>
            </div>
            <Button
                action={{ kind: "a", href: signUpUrl }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                grow={false}
                label={$_("navigation.footer.cta")}
            />
        </div>
        <nav class="flex flex-col gap-12 sm:flex-row">
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.product.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            href="/pricing"
                            label={$_("navigation.footer.nav.product.pricing")}
                        />
                    </li>
                </ul>
            </section>
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.resources.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            href="/help"
                            label={$_(
                                "navigation.footer.nav.resources.help-and-tips",
                            )}
                        />
                    </li>
                </ul>
            </section>
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.company.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            href="/accessibility"
                            label={$_(
                                "navigation.footer.nav.company.accessibility-statement",
                            )}
                        />
                    </li>
                    <li>
                        <Anchor
                            href="/contact-us"
                            label={$_(
                                "navigation.footer.nav.company.contact-us",
                            )}
                        />
                    </li>
                </ul>
            </section>
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.legal.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            label={$_("navigation.footer.nav.legal.privacy")}
                            href="/privacy"
                        />
                    </li>
                    <li>
                        <Anchor
                            label={$_("navigation.footer.nav.legal.tos")}
                            href="/tos"
                        />
                    </li>
                </ul>
            </section>
        </nav>
    </div>
</footer>
