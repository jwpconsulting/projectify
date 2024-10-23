<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<div class="flex h-full flex-col p-4 pt-0">
    <slot name="top-bar" />
    <div class="flex flex-col gap-8">
        <slot name="tab-bar-mobile" />
        <slot name="content" />
    </div>
</div>
