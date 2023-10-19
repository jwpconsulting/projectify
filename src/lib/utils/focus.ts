function getFirstAndLastFocusable(inside: HTMLElement): {
    first: HTMLElement;
    last: HTMLElement;
} {
    const focusables = inside.querySelectorAll("a, button, input");
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (!(first instanceof HTMLElement)) {
        throw new Error("Expected HTMLElement");
    }
    if (!(last instanceof HTMLElement)) {
        throw new Error("Expected HTMLElement");
    }
    return { first, last };
}

export function keepFocusInside(inside: HTMLElement): () => void {
    const listener = ({ target }: FocusEvent) => {
        if (!target) {
            throw new Error("Expected target");
        }
        if (!(target instanceof Node)) {
            throw new Error("Expected Node");
        }
        const { first, last } = getFirstAndLastFocusable(inside);
        const position = target.compareDocumentPosition(inside);
        const contained = position & Node.DOCUMENT_POSITION_CONTAINS;
        const preceding = position & Node.DOCUMENT_POSITION_PRECEDING;
        const following = position & Node.DOCUMENT_POSITION_FOLLOWING;
        if (contained) {
            // We are inside, nothing to do
            return;
        }
        if (preceding) {
            last.focus();
        } else if (following) {
            first.focus();
        } else {
            throw new Error(`Unexpected position ${position}`);
        }
    };
    document.addEventListener("focusin", listener);
    return () => {
        document.removeEventListener("focusin", listener);
    };
}
