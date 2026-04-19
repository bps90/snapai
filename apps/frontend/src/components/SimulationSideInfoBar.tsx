import { Divider } from "@mui/material"
import SimulationInfoBar from "./SimulationInfoBar"
import NodeInfo from "./NodeInfo"
import Logs from "./Logs"
import { useSimulationContext } from "@/contexts/SimulationContext"

export type SimulationSideInfoBarProps = {

}

export default function SimulationSideInfoBar({ }: SimulationSideInfoBarProps) {
    const {
        mouseInNode,
        graphData,
        logs, time, numberOfMessagesInThisRound, numberOfMessagesOverAll
    } = useSimulationContext();

    return (<div className="flex w-full flex-col h-full gap-2">
        <SimulationInfoBar
            cards={[
                { type: 'time', value: time },
                { type: 'totalMsgSent', value: numberOfMessagesOverAll },
                { type: 'msgSentOnRound', value: numberOfMessagesInThisRound },
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
        <Logs logs={logs} />

    </div>)
}