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

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    const hasBeenEdited = false;
    let currentPassword = "";
    let newEmail = "";
</script>

<div class="flex flex-col items-center gap-12">
    <h1 class="text-2xl font-bold">
        {$_("user-account-settings.update-email.title")}
    </h1>
    <div class="flex w-full flex-col gap-10">
        <div class="flex flex-col gap-4">
            <InputField
                label={$_(
                    "user-account-settings.update-email.current-password.label",
                )}
                placeholder={$_(
                    "user-account-settings.update-email.current-password.placeholder",
                )}
                name="current-password"
                style={{ inputType: "password" }}
                bind:value={currentPassword}
            />
            <InputField
                label={$_(
                    "user-account-settings.update-email.new-email.label",
                )}
                placeholder={$_(
                    "user-account-settings.update-email.new-email.placeholder",
                )}
                name="new-email"
                style={{ inputType: "text" }}
                bind:value={newEmail}
            />
        </div>
        <div class="flex flex-row gap-2">
            <Button
                action={{
                    kind: "a",
                    href: "/user/profile",
                }}
                size="medium"
                color="blue"
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.update-email.cancel")}
            />
            <Button
                action={{
                    kind: "button",
                    action: console.error.bind(
                        null,
                        "Update email not implemented",
                    ),
                    disabled: hasBeenEdited,
                }}
                size="medium"
                color="blue"
                style={{ kind: "primary" }}
                label={$_("user-account-settings.update-email.save")}
            />
        </div>
    </div>
</div>
