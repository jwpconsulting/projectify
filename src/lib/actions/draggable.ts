import { spring } from "svelte/motion";
import delay from "delay";

type DraggableParamenters = {
    direction?: string;
    handle?: string;
};

export function draggable(
    node: HTMLElement,
    params: DraggableParamenters = {}
): any {
    let x;
    let y;

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

    coordinates.subscribe(($coords) => {
        node.style.transform = `translate3d(${$coords.x}px, ${$coords.y}px, 0)`;
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
    }

    function handleMouseMove(event) {
        if (!dragStarted) {
            dragStarted = true;
        }
        // Delta X = difference of where we clicked vs where we are currently
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
    }

    async function handleMouseUp(e) {
        coordinates.stiffness = springOpts.stiffness;
        coordinates.damping = springOpts.damping;

        // Fire up event
        node.dispatchEvent(
            new CustomEvent("dragStop", {
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

        await delay(1000);

        node.style.zIndex = zIndex;
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
