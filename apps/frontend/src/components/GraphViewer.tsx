"use client";
import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from "react";
import { MultiDirectedGraph as Graph } from "graphology";
import { downloadAsPNG } from '@sigma/export-image';
import { Sigma } from "sigma";
import { createEdgeArrowProgram } from "sigma/rendering";
import { useSimulationContext } from "@/contexts/SimulationContext";
import { v4 as uuid } from 'uuid';

export type GraphViewerNode = {
    id: string;
    x: number;
    y: number;
    label?: string;
    size?: number;
    color?: string;
    dragable?: boolean;
    forceLabel?: boolean;
    highlighted?: boolean;
    bound?: boolean;
}

export type GraphViewerLink = {
    source: string;
    target: string;
    color?: string;
    label?: string;
    type?: 'line' | 'arrow' | 'curve' | 'quadratic' | 'curvedArrow' | 'curvedLine';
    width?: number;
    highlighted?: boolean;
    bound?: boolean;
    forceLabel?: boolean;
    dragable?: boolean;
}

export type GraphData = {
    nodes: GraphViewerNode[];
    links: GraphViewerLink[];
}

export type GraphViewerProps = {
    dimensions: {
        x: [number, number];
        y: [number, number];
    }
    data: GraphData,
    renderLabels?: boolean;
    showArrows?: boolean;
    arrowHeadSize?: number;
}

export type GraphViewerRef = {
    resetCam: () => void;
    getSigma: () => Sigma;
    getGraph: () => Graph;
    toImage: () => void;
}

const GraphViewer = forwardRef<GraphViewerRef, GraphViewerProps>(({
    dimensions,
    data,
    renderLabels,
    showArrows,
    arrowHeadSize
}, ref) => {
    const renderId = uuid();
    const containerRef = useRef<HTMLDivElement>(null);
    const sigmaRef = useRef<Sigma | null>(null);
    const graphRef = useRef<Graph | null>(null);
    const {
        setGraphData,
        mouseInNode, setMouseInNode,
        cameraState, setCameraState,
        isRunning
    } = useSimulationContext();

    const enableDrag = () => {
        if (!graphRef.current) return;
        if (!sigmaRef.current) return;
        let draggedNode: string | null = null;

        sigmaRef.current.on("downNode", (e) => {
            if (!graphRef.current?.getNodeAttributes(e.node)?.dragable) return;
            draggedNode = e.node;
            sigmaRef.current!.getCamera().disable(); // Desativa o pan/zoom enquanto arrasta
        });

        sigmaRef.current.getMouseCaptor().on("mousemove", (e) => {
            if (draggedNode) {
                const pos = sigmaRef.current!.viewportToGraph(e);
                graphRef.current!.setNodeAttribute(draggedNode, "x", pos.x);
                graphRef.current!.setNodeAttribute(draggedNode, "y", pos.y);
                graphRef.current!.setNodeAttribute(draggedNode, "label", `(${pos.x.toFixed(2)},${pos.y.toFixed(2)})`);
            }
        });

        sigmaRef.current.getMouseCaptor().on("mouseup", () => {
            if (draggedNode) {
                draggedNode = null;
                sigmaRef.current!.getCamera().enable(); // Reativa pan/zoom
            }
        });
    }

    const enableNodeInfo = () => {
        if (!graphRef.current) return;
        if (!sigmaRef.current) return;
        sigmaRef.current.on("enterNode", (e) => {
            if (mouseInNode) return;
            setMouseInNode(e.node);
        });
        sigmaRef.current.on("leaveNode", (e) => {
            setMouseInNode(null);
        });
    }

    const createBoundary = (g: Graph) => {
        const boundData = {
            nodes: [
                { id: 'b-lb', x: dimensions.x[0], y: dimensions.y[0] },
                { id: 'b-rb', x: dimensions.x[1], y: dimensions.y[0] },
                { id: 'b-lt', x: dimensions.x[0], y: dimensions.y[1] },
                { id: 'b-rt', x: dimensions.x[1], y: dimensions.y[1] },
            ],
            links: [
                { source: 'b-lb', target: 'b-rb' },
                { source: 'b-lt', target: 'b-lb' },
                { source: 'b-lt', target: 'b-rt' },
                { source: 'b-rt', target: 'b-rb' },
            ],
        }
        boundData.nodes.forEach(n => g.addNode(n.id, {
            ...n,
            size: -1,
            highlighted: false,
            color: '#00000000',
            dragable: false,
            forceLabel: false,
            bound: true,
        }));
        boundData.links.forEach(e => g.addEdge(e.source, e.target, {
            ...e,
            color: '#ccc',
            bound: true,
            dragable: false,
            highlighted: false,
            forceLabel: false,
        }));
    }

    const initCamera = () => {
        if (!graphRef.current) return;
        if (!sigmaRef.current) return;
        if (cameraState) sigmaRef.current.getCamera().setState(cameraState);

        sigmaRef.current.getCamera().on('updated', (state) => setCameraState(state));
    }

    useEffect(() => {
        console.log(showArrows, renderLabels)
        if (!containerRef.current) return;

        if (sigmaRef.current) {
            sigmaRef.current.kill();
            sigmaRef.current = null;
        }

        const g = new Graph();

        createBoundary(g);

        data.nodes.forEach(n => g.addNode(n.id, n));
        data.links.forEach(e => g.addEdge(e.source, e.target, {
            ...e,
            arrowSize: 5,
            weight: 7,
            type: e.type ?? showArrows ? 'arrow' : 'line',
        }));

        graphRef.current = g;

        sigmaRef.current = new Sigma(g, containerRef.current, {
            renderEdgeLabels: true,
            autoCenter: false,
            renderLabels: renderLabels ?? true,
            edgeProgramClasses: {
                arrow: createEdgeArrowProgram({
                    lengthToThicknessRatio: 2.5 * (arrowHeadSize ?? 1),
                    widenessToThicknessRatio: 2 * (arrowHeadSize ?? 1)
                })
            }
        });

        enableDrag();
        enableNodeInfo();
        initCamera();
        // Função de animação
        let interval: NodeJS.Timeout | null | undefined = null;
        const animate = () => {
            console.log(renderId)
            if (graphRef.current) {
                graphRef.current.forEachNode((node, attr) => {
                    if (attr.bound === true) return null;
                    if (node === '0') return null;
                    const coords = {
                        x: attr.x + Math.random() - 0.5,
                        y: attr.y + Math.random() - 0.5
                    };
                    if (coords.x < 0) coords.x = 0;
                    if (coords.y < 0) coords.y = 0;
                    if (coords.x > 100) coords.x = 100;
                    if (coords.y > 100) coords.y = 100;

                    if (node.length < 2) {
                        graphRef.current!.updateNodeAttributes(node, (attr) => ({
                            ...attr,
                            ...coords,
                            label: node
                        }));
                        const newId = uuid();
                        graphRef.current!.addNode(newId, {
                            ...attr,
                            ...coords,
                            size: 1,
                            id: newId,
                            label: graphRef.current!.nodes().length
                        });

                        setGraphData((prev) => ({
                            ...prev,
                            nodes: [
                                ...prev.nodes.filter(n => n.id !== node),
                                {
                                    ...attr,
                                    ...coords,
                                    id: node,
                                    label: node
                                },
                                {
                                    ...attr,
                                    ...coords,
                                    size: 1,
                                    id: newId,
                                    label: (graphRef.current!.nodes().length - 1).toString()
                                }
                            ]
                        }));
                    }
                });

            }
        };
        interval = isRunning ? setInterval(animate, 50) : undefined;

        return () => interval && clearTimeout(interval);
    }, [renderLabels, arrowHeadSize, showArrows, isRunning]);

    const resetCam = () => {
        if (sigmaRef.current) {
            sigmaRef.current.getCamera().animatedReset({
                duration: 300,
            });
        }
    }

    const toImage = () => {
        if (!sigmaRef.current) return;

        downloadAsPNG(sigmaRef.current, {
            fileName: "graph",       // nome do arquivo sem extensão
            backgroundColor: "#fff", // cor de fundo (ou transparente)
            width: null,             // usa largura do container
            height: null,            // usa altura do container
            layers: null,            // exporta todos os layers
            cameraState: null        // estado atual da câmera
        });
    };


    useImperativeHandle(ref, () => ({
        resetCam,
        toImage,
        getSigma: () => sigmaRef.current!,
        getGraph: () => graphRef.current!,
    }));

    return (<>
        <div ref={containerRef} style={{ width: "100%", height: "100%", border: '1px solid #ccc' }} />
    </>);
})

export default GraphViewer;