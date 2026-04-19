import { Divider } from "@mui/material"
import ControlInput from "./ControlInput"
import ControlButton from "./ControlButton"
import StopCircleRoundedIcon from '@mui/icons-material/StopCircleRounded';
import PlayCircleRoundedIcon from '@mui/icons-material/PlayCircleRounded';
import AddCircleRoundedIcon from '@mui/icons-material/AddCircleRounded';
import { FieldErrors, set, useForm, UseFormRegister } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import FitScreenIcon from '@mui/icons-material/FitScreen';
import { forwardRef, useEffect, useImperativeHandle, useState } from "react";
import FileDownloadRoundedIcon from '@mui/icons-material/FileDownloadRounded';
import { useSimulationContext } from "@/contexts/SimulationContext";
import { initSimulation } from "@/lib/fetchers";

const preRunFormSchema = z.object({
    rounds: z.number().int().min(1).optional(),
    refreshRate: z.number().int().min(0).optional(),
})

export type PreRunFormSchema = z.infer<typeof preRunFormSchema>;

export type ControlBarRef = {};

export type ControlBarProps = {
    onResetCamButtonClick?: () => void;
    onDownloadGraphButtonClick?: () => void;
    onPlay?: (data: PreRunFormSchema) => void;
    onPauseButtonClick?: () => void;
    onAddNodesButtonClick?: () => void;
}

const ControlBar = forwardRef<ControlBarRef, ControlBarProps>(({
    onResetCamButtonClick,
    onDownloadGraphButtonClick,
    onPlay,
    onPauseButtonClick,
    onAddNodesButtonClick
}, ref) => {
    const [initializeButtonLoading, setInitializeButtonLoading] = useState(false);
    const [initializeButtonDisabled, setInitializeButtonDisabled] = useState(false);
    const [initializeButtonState, setInitializeButtonState] = useState<'success' | 'error' | 'idle'>('idle');
    const [initializeButtonBg, setInitializeButtonBg] = useState<string | undefined>(undefined);
    const { showArrows, showIds, setShowArrows, setShowIds, selectedProject, setDimensions } = useSimulationContext();

    const { register, handleSubmit, formState: { errors } } = useForm<PreRunFormSchema>({
        resolver: zodResolver(preRunFormSchema)
    });

    const handlePreRunFormSubmit = (data: PreRunFormSchema) => {
        if (onPlay) onPlay(data);
    }

    const handlePreRunFormSubmitBuilder = (oneRound: boolean) => {
        return (data: PreRunFormSchema) => {
            if (oneRound) data.rounds = 1;
            if (!data.refreshRate) data.refreshRate = 0;
            return handlePreRunFormSubmit(data);
        }
    }

    const onInitializeButtonClick = async () => {
        if (!selectedProject) return;
        setInitializeButtonLoading(true);
        await initSimulation(selectedProject)
            .then(({ dimensions }) => {
                setInitializeButtonState('success');
                console.log(dimensions);
                setDimensions(dimensions);
                (window as Window & typeof globalThis & { electron: any }).electron.send('initialize');
            },
                () => setInitializeButtonState('error'));
        setTimeout(() => {
            setInitializeButtonState('idle');
            setInitializeButtonLoading(false);
        }, 1000);
    }

    useEffect(() => {
        setInitializeButtonDisabled(!selectedProject);
    }, [selectedProject])

    useEffect(() => {
        setInitializeButtonBg(initializeButtonState === 'success' ? '#E9CC2840' : initializeButtonState === 'error' ? '#ff4d4d40' : undefined);
    }, [initializeButtonState])

    return (
        <div className="control-bar gap-1 flex">
            <ControlButton
                disabled={initializeButtonDisabled || initializeButtonLoading}
                label="Initialize"
                iconImage={{
                    src: "/assets/reload.svg",
                    alt: "Gear with a reloading wheel icon",
                }}
                style={{ backgroundColor: initializeButtonBg }}
                helpText={initializeButtonDisabled ? "Select a project first!" : "Reset all variables and prepare the simulator for a new simulation."}
                onClick={onInitializeButtonClick}
            />
            <ControlButton
                label="Add Nodes"
                icon={<AddCircleRoundedIcon style={{ color: "#2867CE" }} />}
                helpText="Open form to add nodes to the network."
                onClick={onAddNodesButtonClick}
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
                <ControlInput
                    title="Number of Rounds"
                    placeholder="Rounds"
                    helpText="The number of rounds that the simulation should run for. The simulation will stop after this number of rounds or when the stop button is pressed."
                    register={register("rounds", { setValueAs: value => value ? Number(value) : undefined })}
                    error={errors.rounds?.message}
                    type="number"
                    min={1}
                />
                <ControlInput
                    title="Refresh Rate (Rounds per second)"
                    placeholder="Refresh rate"
                    helpText="The number of rounds that the simulation should run for each second. For no limit, set to 0 or leave blank."
                    register={register("refreshRate", { setValueAs: value => value ? Number(value) : undefined })}
                    error={errors.refreshRate?.message}
                    type="number"
                    min={0}
                />
                <ControlButton
                    onClick={handleSubmit(handlePreRunFormSubmitBuilder(true))}
                    iconImage={{
                        alt: "Play icon with a number 1",
                        src: "/assets/run1.svg"
                    }}
                    helpText="Run the simulation for one round."
                />
                <ControlButton
                    onClick={handleSubmit(handlePreRunFormSubmitBuilder(false))}
                    icon={<PlayCircleRoundedIcon style={{ color: "#27ae60" }} />}
                    helpText="Run the simulation for the specified number of rounds."
                />
                <ControlButton
                    icon={<StopCircleRoundedIcon style={{ color: "#E74C3C" }} />}
                    helpText="Stop the simulation."
                    onClick={onPauseButtonClick}
                />
            </div>
            <Divider orientation="vertical" flexItem />
            <ControlButton
                icon={<FitScreenIcon className="text-gray-400" fontSize="small" />}
                helpText="Reset camera to fit the screen. (Autoscale)"
                onClick={onResetCamButtonClick}
            />
            <ControlButton
                iconImage={{
                    src: `/assets/arrow-${showArrows ? "closed" : "open"}-eye.svg`,
                    alt: "Arrow with an eye icon"
                }}
                helpText={`${showArrows ? "Hide" : "Show"} the network graph arrows.`}
                onClick={() => setShowArrows(!showArrows)}
            />
            <ControlButton
                iconImage={{
                    src: `/assets/${showIds ? "not-" : ""}id.svg`,
                    alt: "ID icon"
                }}
                helpText={`${showIds ? "Hide" : "Show"} the network nodes IDs.`}
                onClick={() => setShowIds(!showIds)}
            />
            <ControlButton
                icon={<FileDownloadRoundedIcon className="text-gray-400" fontSize="small" />}
                helpText="Download the network graph as an image."
                onClick={onDownloadGraphButtonClick}
            />
        </div>
    )
});

export default ControlBar;