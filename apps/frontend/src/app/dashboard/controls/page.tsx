"use client";

import dynamic from "next/dynamic";
import ControlBar, { PreRunFormSchema } from "@/components/ControlBar";
import { useEffect, useRef } from "react";
import { Divider } from "@mui/material";
import { GraphData, GraphViewerRef } from "@/components/GraphViewer";

import SimulationInfoBar from "@/components/SimulationInfoBar";
import { useSimulationContext } from "@/contexts/SimulationContext";
import NodeInfo from "@/components/NodeInfo";
import Logs from "@/components/Logs";
import { useQueryState } from 'nuqs';
import LinkWithQuery from "@/components/LinkWithQuery";
import AddNodeFormDialog from "@/components/AddNodesFormDialog";

// Importa sem SSR
const GraphViewer = dynamic(() => import("@/components/GraphViewer"), { ssr: false });

const mockData: GraphData = {
    nodes: [
        { id: '1', x: 20, y: 70, size: 10, label: "(20,70)", color: '#aaddff' },
        { id: '2', x: 80, y: 70, size: 10, label: "(80,70)", color: "#ffddaa" },
        { id: '3', x: 20, y: 30, size: 10, label: "(20,30)", color: "#0000ff" },
        { id: '4', x: 60, y: 40, size: 10, label: "(60,40)", color: "#00ff00" },
        { id: '0', x: 50, y: 50, size: 10, label: "(50,50)", dragable: true, color: "#ff0000" },
    ],
    links: [
        { source: '1', target: '2' },
        { source: '3', target: '1' },
        { source: '1', target: '4' },
        { source: '4', target: '2' },
        { source: '0', target: '1' },
        { source: '0', target: '2' },
        { source: '0', target: '4', type: 'line' },
        { source: '4', target: '0' },
    ],
}

type BypassKeys = "projectValidation";

export default function DashboardControls() {
    const [bypass] = useQueryState<BypassKeys[]>('bypass', {
        defaultValue: [],
        parse: (s) => s.split(",") as BypassKeys[]
    });
    const graphViewerRef = useRef<GraphViewerRef>(null);
    const {
        showIds, showArrows, graphData, setGraphData, mouseInNode,
        setIsRunning, selectedProject
    } = useSimulationContext();
    const [addNodesDialogOpen, setAddNodesDialogOpen] = useQueryState('add_nodes_form_open', {
        defaultValue: false,
        parse: (s) => s === 'true',
    });

    const onPlay = (data: PreRunFormSchema) => {
        console.log(data);
        setIsRunning(true);
    };

    const onPause = () => {
        setIsRunning(false);
    };

    const closeAddNodesDialog = () => {
        setAddNodesDialogOpen(false);
    }

    useEffect(() => {
        setGraphData(mockData);
    }, []);

    if (!selectedProject && !bypass.includes("projectValidation"))
        return (
            <div className="w-full">
                <div style={{ height: '40dvh' }} className="y-spacer"></div>
                <main className="mx-auto max-w-5xl flex flex-col items-center justify-center px-4 ">
                    <div className="text-9xl mb-10 -mt-32">⚠️</div>
                    <h1 className="text-5xl font-bold text-gray-900 mb-8 text-center">
                        Go to <LinkWithQuery href="/dashboard/configuration" className="text-blue-600 underline">Configurations</LinkWithQuery> page to select a project
                    </h1>
                </main></div>
        )

    return (
        <>
            <div className="flex gap-2 flex-col w-full justify-center min-h-dvh max-h-dvh px-4">
                <ControlBar
                    onPlay={onPlay}
                    onPauseButtonClick={onPause}
                    onResetCamButtonClick={() => graphViewerRef.current?.resetCam()}
                    onDownloadGraphButtonClick={() => graphViewerRef.current?.toImage()}
                    onAddNodesButtonClick={() => setAddNodesDialogOpen(true)}
                />
                <Divider variant="middle" />
                <div className="grid grid-cols-2 gap-2 controls-and-graph">
                    <div className="flex flex-col gap-2 p-4 bg-gray-50 w-full overflow-y-auto" style={{ height: "90dvh" }}>
                        <div className="flex w-full flex-col h-full gap-2">
                            <SimulationInfoBar
                                cards={[
                                    { type: 'time', value: 156423 },
                                    { type: 'totalMsgSent', value: 540198946 },
                                    { type: 'msgSentOnRound', value: 5465 },
                                ]}
                            />
                            <SimulationInfoBar
                                cards={[
                                    { type: 'nodes', value: graphData.nodes.length },
                                    { type: 'edges', value: graphData.links.length },
                                    { type: 'remainingEvents', value: '----' },
                                ]}
                            />
                            <Divider variant="middle" />
                            <NodeInfo node={mouseInNode ?? undefined} />
                            <Logs logs={[
                                'log1',
                                'log2',
                                'log3 Lorem, ipsum dolor sit amet consectetur adipisicing elit. ',
                                'log4 Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore excepturi ex, impedit perferendis tempora, vero mollitia consectetur eveniet neque adipisci libero aut laudantium necessitatibus praesentium delectus ratione voluptates sed distinctio.',
                            ]} />

                        </div>
                    </div>

                    <div className="graph-container" style={{ minWidth: "90dvh", width: "90dvh", height: "90dvh" }} >
                        <GraphViewer
                            ref={graphViewerRef}
                            dimensions={{ x: [0, 100], y: [0, 100] }}
                            data={graphData}
                            arrowHeadSize={1.5}
                            renderLabels={showIds}
                            showArrows={showArrows}
                        />
                    </div>
                </div>

            </div>
            <AddNodeFormDialog
                onClose={closeAddNodesDialog}
                onSubmit={closeAddNodesDialog}
                open={addNodesDialogOpen}
            />
        </>);
}
