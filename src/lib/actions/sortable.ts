import Sortable from "sortablejs";

type SortableParamenters = {
    group?: string;
};

export function sortable(
    node: HTMLElement,
    params: SortableParamenters = {}
): any {
    const sortable = Sortable.create(node, {
        group: params.group,
        animation: 300,
        put: true,
        pull: true,
        forceFallback: true,
        fallbackOnBody: true,
        filter: ".ignore-elements",
        onStart(e) {
            node.dispatchEvent(new CustomEvent("dragStart"));
        },
        onEnd(e) {
            node.dispatchEvent(
                new CustomEvent("dragEnd", {
                    detail: {
                        from: e.from,
                        to: e.to,
                        oldIndex: e.oldIndex,
                        newIndex: e.newIndex,
                    },
                })
            );
        },
    });
    return {
        destroy() {
            console.log("destro");
            sortable.destroy();
        },
    };
}
