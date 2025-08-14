"use client";
import { useEffect, useRef, useState } from "react";
import { MultiDirectedGraph as Graph } from "graphology";
import "@react-sigma/core/lib/style.css";
import { Sigma } from "sigma";
import { Button } from "@mui/material";

const boundData = {
    nodes: [
        { id: 'b-lb', x: 0, y: 0, size: 0, color: "#00000000", dragable: false, forceLabel: false, highlighted: false, bound: true, },
        { id: 'b-rb', x: 100, y: 0, size: 0, color: "#00000000", bound: true, },
        { id: 'b-lt', x: 0, y: 100, size: 0, color: "#00000000", bound: true, },
        { id: 'b-rt', x: 100, y: 100, size: 0, color: "#00000000", bound: true, },
    ],
    links: [
        { source: 'b-lb', target: 'b-rb', color: "#ccc" },
        { source: 'b-lt', target: 'b-lb', color: "#ccc" },
        { source: 'b-lt', target: 'b-rt', color: "#ccc" },
        { source: 'b-rt', target: 'b-rb', color: "#ccc" },
    ],
};

const initialData = {
    nodes: [
        { id: 1, x: 20, y: 70, size: 10, label: "(20,70)" },
        { id: 2, x: 80, y: 70, size: 10, label: "(80,70)" },
        { id: 3, x: 20, y: 30, size: 10, label: "(20,30)" },
        { id: 4, x: 60, y: 40, size: 10, label: "(60,40)" },
        { id: 0, x: 50, y: 50, size: 10, color: "#ff0000", label: "(50,50)" },
    ],
    links: [
        { source: 1, target: 2 },
        { source: 3, target: 1 },
        { source: 1, target: 4 },
        { source: 4, target: 2 },
        { source: 0, target: 1 },
        { source: 0, target: 2 },
        { source: 0, target: 4 },
    ],
};

export default function GraphViewer() {
    const containerRef = useRef<HTMLDivElement>(null);
    const sigmaRef = useRef<Sigma | null>(null);
    const graphRef = useRef<Graph | null>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        // Se já existir uma instância, limpa antes de criar nova
        if (sigmaRef.current) {
            sigmaRef.current.kill();
            sigmaRef.current = null;
        }

        // Cria grafo
        const g = new Graph();
        boundData.nodes.forEach(n => g.addNode(n.id, {
            ...n,
            size: -1,
            highlighted: false,
            color: '#00000000',
            dragable: false,
            forceLabel: false,
            bound: true,
        }));
        boundData.links.forEach(e => g.addEdge(e.source, e.target, e));
        initialData.nodes.forEach(n => g.addNode(n.id, n));
        initialData.links.forEach(e => g.addEdge(e.source, e.target, e));

        graphRef.current = g;

        // Cria instância do Sigma
        sigmaRef.current = new Sigma(g, containerRef.current, {
            renderEdgeLabels: true,
            defaultNodeColor: "#3388ff",
        });

        let draggedNode: string | null = null;

        // Quando clicar num nó, marca ele como sendo arrastado
        sigmaRef.current.on("downNode", (e) => {
            draggedNode = e.node;
            sigmaRef.current!.getCamera().disable(); // Desativa o pan/zoom enquanto arrasta
        });

        // Quando mover o mouse, se estiver arrastando, atualiza a posição
        sigmaRef.current.getMouseCaptor().on("mousemove", (e) => {
            if (draggedNode) {
                const pos = sigmaRef.current!.viewportToGraph(e);
                graphRef.current!.setNodeAttribute(draggedNode, "x", pos.x);
                graphRef.current!.setNodeAttribute(draggedNode, "y", pos.y);
                graphRef.current!.setNodeAttribute(draggedNode, "label", `(${pos.x.toFixed(2)},${pos.y.toFixed(2)})`);
            }
        });

        // Quando soltar o mouse, para de arrastar
        sigmaRef.current.getMouseCaptor().on("mouseup", () => {
            if (draggedNode) {
                draggedNode = null;
                sigmaRef.current!.getCamera().enable(); // Reativa pan/zoom
            }
        });
        // Função de animação
        let interval: NodeJS.Timeout | null = null;
        const animate = () => {
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
                    graphRef.current!.updateNodeAttributes(node, (attr) => ({
                        ...attr,
                        ...coords,
                        label: coords.x + ',' + coords.y
                    }));
                })
            }
        };
        interval = setInterval(animate);

        return () => clearTimeout(interval);
    }, []);

    const resetCam = () => {
        if (sigmaRef.current) {
            sigmaRef.current.getCamera().animatedReset({
                duration: 300,
            });
        }
    }

    return (<>
        <div ref={containerRef} style={{ width: "90dvh", height: "90dvh", border: '1px solid #ccc' }} />
        <Button onClick={resetCam}>Reset Camera</Button>
    </>);
}
