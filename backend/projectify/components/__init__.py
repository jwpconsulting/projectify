"""Components."""

from typing import Any

from django_components import Component, register

"""
export type ButtonAction =
    | { kind: "a"; href: string; onInteract?: () => void }
    | { kind: "button"; form?: string; action: () => void; disabled?: boolean }
    // For the case that a disabled button is disabled because no callback is
    // present
    | { kind: "button"; form?: string; action?: undefined; disabled: true }
    | { kind: "submit"; form?: string; disabled?: boolean };

// For buttons/Button.svelte
export type ButtonStyle =
    | { kind: "primary" }
    | { kind: "secondary" }
    // TODO make this icon? instead Justus 2023-08-28
    | {
          kind: "tertiary";
          icon?: { position: "right" | "left"; icon: IconSource };
      };
export type ButtonColor = "blue" | "red";
"""


@register("pbutton")
class PButton(Component[Any, Any, Any, Any, Any, Any]):
    """Projectify Button Component."""

    template_name = "pbutton.html"
