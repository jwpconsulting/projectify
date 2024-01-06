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
<script>
</script>

<div class="h-20 w-20 text-primary">
    <svg viewBox="-50 -50 100 100" fill="none">
        <circle cx="0" cy="0" />
        <circle cx="0" cy="0" />
    </svg>
</div>

<style lang="scss">
    svg {
        position: relative;
        width: 100%;
        height: 100%;
        --stroke-size: 5px;
    }
    svg > circle {
        stroke: currentColor;
        stroke-width: var(--stroke-size);
        opacity: 1;
        border-radius: 50%;
        animation: ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
        animation-delay: 0.5s;
    }
    svg circle:nth-child(2) {
        animation-delay: 1s;
    }
    @keyframes ripple {
        0% {
            opacity: 1;
            r: 0px;
        }
        100% {
            opacity: 0;
            r: calc(50% - var(--stroke-size));
        }
    }
</style>
