<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import PolyLogo from "$lib/figma/navigation/polylogo.svg";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { signUpUrl } from "$lib/urls/user";
</script>

<footer class="flex w-full flex-col gap-6 border-t border-border p-8">
    <div class="flex flex-col gap-8 sm:flex-row sm:flex-wrap">
        <!-- Header -->
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
        <!-- Nav -->
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
                    <li>
                        <Anchor
                            href="https://www.jwpconsulting.net"
                            label={$_(
                                "navigation.footer.nav.company.corporate-info",
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
                    <li>
                        <Anchor
                            label={$_(
                                "navigation.footer.nav.legal.free-software",
                            )}
                            href="/free-software"
                        />
                    </li>
                </ul>
            </section>
        </nav>
        <!-- epilogue -->
        <section>
            {$_("navigation.footer.epilogue.copyright")}
            <br />
            {$_("navigation.footer.epilogue.free-software")}
            <Anchor
                href="/free-software"
                label={$_("navigation.footer.epilogue.details")}
            />
        </section>
    </div>
</footer>
