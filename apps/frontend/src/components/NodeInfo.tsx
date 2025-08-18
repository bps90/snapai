import { Divider } from "@mui/material";
import { useEffect, useState } from "react";
import { GraphViewerNode } from "./GraphViewer";
import { useSimulationContext } from "@/contexts/SimulationContext";
import { set } from "react-hook-form";

export type NodeInfoProps = {
    node?: string;
};

const NodeInfo = ({ node: nodeId }: NodeInfoProps) => {
    const [node, setNode] = useState<GraphViewerNode>();
    const { graphData } = useSimulationContext();

    useEffect(() => {
        if (!nodeId) {
            setNode(undefined);
            return;
        }
        const node = graphData.nodes.find(node => node.id === nodeId);
        if (!node) {
            setNode(undefined);
            return;
        }
        setNode(node);
    }, [nodeId])

    return (
        <div className="font-mono bg-amber-50 w-full rounded-md border border-amber-200 text-slate-700 px-3 py-2">
            <div className="font-mono flex items-center">
                <span>ID</span>
                <Divider className="flex-1" variant="middle" />
                <span className="font-extrabold">{node?.id ?? '----'}</span>
            </div>
            <div className="font-mono flex items-center">
                <span>Label</span>
                <Divider className="flex-1" variant="middle" />
                <span className="font-extrabold">{node?.label ?? '----'}</span>
            </div>
            <div className="font-mono flex items-center">
                <span>Coordinate X</span>
                <Divider className="flex-1" variant="middle" />
                <span className="font-extrabold">{node?.x ?? '----'}</span>
            </div>
            <div className="font-mono flex items-center">
                <span>Coordinate Y</span>
                <Divider className="flex-1" variant="middle" />
                <span className="font-extrabold">{node?.y ?? '----'}</span>
            </div>
            <div className="font-mono flex items-center">
                <span>Size</span>
                <Divider className="flex-1" variant="middle" />
                <span className="font-extrabold">{node?.size ?? '----'}</span>
            </div>
            <div className="font-mono flex items-center">
                <span>Color</span>
                <Divider className="flex-1" variant="middle" />
                <span className="font-extrabold">
                    {node?.color ? (<>
                        <span className="inline-block w-4 h-4 rounded-full mr-2" style={{ backgroundColor: node.color }}></span>
                        {node.color}
                    </>) : '----'}
                </span>
            </div>
            <div className="font-mono flex items-center">
                <span>Dragable</span>
                <Divider className="flex-1" variant="middle" />
                <span className="font-extrabold">
                    {node?.dragable ? "✅ true" : node?.dragable === false ? "❌ false" : "----"}
                </span>
            </div>
        </div>
    );
};

export default NodeInfo;