import { spring } from "svelte/motion";
import delay from "delay";

type DraggableParamenters = {
    direction?: string;
    handle?: string;
    moveToBody?: boolean;
};

export function draggable(
    node: HTMLElement,
    params: DraggableParamenters = {}
): any {
    let x;
    let y;
    let dragOverIt: HTMLElement = null;

    let dragStarted = false;

    let handle = node;

    if (params.handle) {
        handle = node.querySelector(params.handle);
    }

    const springOpts = {
        stiffness: 0.2,
        damping: 0.4,
    };

    const coordinates = spring({ x: 0, y: 0 }, springOpts);

    // Default Directions
    const directions = {
        y: true,
        x: true,
    };

    if (params?.direction === "x") {
        directions.y = false;
    } else if (params?.direction === "y") {
        directions.x = false;
    }

    let draggingItem: HTMLElement = node;

    coordinates.subscribe(($coords) => {
        if (!draggingItem) {
            return;
        }
        draggingItem.style.transform = `translate3d(${$coords.x}px, ${$coords.y}px, 0)`;
    });

    handle.addEventListener("mousedown", handleMouseDown);

    handle.addEventListener("click", handleClick);

    let zIndex;

    function handleMouseDown(event) {
        x = event.clientX;
        y = event.clientY;
        zIndex = node.style.zIndex;
        node.style.zIndex = "10000";
        window.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("mouseup", handleMouseUp);
        dragStarted = false;

        coordinates.stiffness = coordinates.damping = 1;

        if (params.moveToBody) {
            const bounds = node.getBoundingClientRect();

            draggingItem = node.cloneNode(true) as HTMLElement;
            draggingItem.style.position = "fixed";
            draggingItem.style.left = `${bounds.x}px`;
            draggingItem.style.top = `${bounds.y}px`;
            draggingItem.style.zIndex = "10000";
            draggingItem.style.opacity = "0.9";

            node.style.opacity = "0.0";

            document.body.appendChild(draggingItem);
        }
    }

    function handleMouseMove(event) {
        if (!dragStarted) {
            dragStarted = true;
            node.dispatchEvent(new CustomEvent("dragstart"));
        }
        const dx = event.clientX - x;
        const dy = event.clientY - y;
        x = event.clientX;
        y = event.clientY;
        coordinates.update(($coords) => {
            return {
                x: directions.x ? $coords.x + dx : 0,
                y: directions.y ? $coords.y + dy : 0,
            };
        });

        let els = document.elementsFromPoint(x, y);
        els = els.filter((el) => {
            if (!el.classList.contains("sortable-item")) {
                return false;
            }
            return true;
        });
        if (els[1]) {
            if (!dragOverIt || els[1] != dragOverIt) {
                if (dragOverIt && els[1] != dragOverIt) {
                    dragOverIt.dispatchEvent(new CustomEvent("dragout"));
                }

                dragOverIt = els[1] as HTMLElement;
                dragOverIt.dispatchEvent(new CustomEvent("dragover"));
            }
        } else {
            if (dragOverIt) {
                dragOverIt.dispatchEvent(new CustomEvent("dragout"));
                dragOverIt = null;
            }
        }
    }

    async function handleMouseUp(e) {
        coordinates.stiffness = springOpts.stiffness;
        coordinates.damping = springOpts.damping;

        // Fire up event
        node.dispatchEvent(
            new CustomEvent("dragend", {
                detail: {
                    x,
                    y,
                },
            })
        );

        // Reset values
        x = 0;
        y = 0;
        coordinates.update(() => {
            return {
                x: 0,
                y: 0,
            };
        });
        // Remove event listers
        window.removeEventListener("mousemove", handleMouseMove);
        window.removeEventListener("mouseup", handleMouseUp);

        const curNode = node;
        const curDraggingItem = draggingItem;
        draggingItem = node;

        if (params.moveToBody && curDraggingItem) {
            curDraggingItem.remove();
        }

        curNode.style.opacity = "1";

        if (dragOverIt) {
            dragOverIt.dispatchEvent(new CustomEvent("dragout"));
            dragOverIt = null;
        }

        await delay(1000);

        curNode.style.zIndex = zIndex;
    }

    function handleClick(e) {
        if (!dragStarted) {
            handle.dispatchEvent(new CustomEvent("dragClick"));
        }
    }

    return {
        destroy() {
            handle.removeEventListener("mousedown", handleMouseDown);
        },
    };
}
