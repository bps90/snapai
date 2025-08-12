import ControlButton from "@/components/ControlButton";
import StopCircleRoundedIcon from '@mui/icons-material/StopCircleRounded';
import PlayCircleRoundedIcon from '@mui/icons-material/PlayCircleRounded';
import AddCircleRoundedIcon from '@mui/icons-material/AddCircleRounded';
import { Divider } from "@mui/material";
import ControlInput from "@/components/ControlInput";

export default function DashboardControls() {
    return (
        <div className="flex flex-col w-full justify-center min-h-dvh px-4 col-start-3 col-end-13">
            <div className="control-bar gap-1 flex">
                <ControlButton
                    label="Initialize"
                    iconImage={{
                        src: "/assets/initialize.svg",
                        alt: "Gear with a reloading wheel icon",
                    }}
                    helpText="Reset all variables and prepare the simulator for a new simulation."
                />
                <ControlButton
                    label="Add Nodes"
                    icon={<AddCircleRoundedIcon style={{ color: "#2867CE" }} />}
                    helpText="Open form to add nodes to the network."
                />
                <ControlButton
                    label="Reevaluate Connections"
                    iconImage={{
                        alt: "Network icon",
                        src: "/assets/reevaluate-connections.svg"
                    }}
                    helpText="Reevaluate the connections between the nodes in the network."
                />
                <Divider orientation="vertical" flexItem />
                <div className="playpause-bar flex gap-1">
                    <ControlInput title="Number of Rounds" placeholder="Rounds" helpText="The number of rounds that the simulation should run for. The simulation will stop after this number of rounds or when the stop button is pressed." />
                    <ControlInput
                        title="Refresh Rate (Rounds per second)"
                        placeholder="Refresh rate"
                        helpText="The number of rounds that the simulation should run for each second. For no limit, set to 0 or leave blank."
                    />
                    <ControlButton
                        iconImage={{
                            alt: "Play icon with a number 1",
                            src: "/assets/run1.svg"
                        }}
                        helpText="Run the simulation for one round."
                    />
                    <ControlButton
                        icon={<PlayCircleRoundedIcon style={{ color: "#27ae60" }} />}
                        helpText="Run the simulation for the specified number of rounds."
                    />
                    <ControlButton
                        icon={<StopCircleRoundedIcon style={{ color: "#E74C3C" }} />}
                        helpText="Stop the simulation."
                    />
                </div>
            </div>
        </div>
    );
}