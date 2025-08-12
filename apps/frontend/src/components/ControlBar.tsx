import { Divider } from "@mui/material"
import ControlInput from "./ControlInput"
import ControlButton from "./ControlButton"
import StopCircleRoundedIcon from '@mui/icons-material/StopCircleRounded';
import PlayCircleRoundedIcon from '@mui/icons-material/PlayCircleRounded';
import AddCircleRoundedIcon from '@mui/icons-material/AddCircleRounded';
import { FieldErrors, useForm, UseFormRegister } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";


const preRunFormSchema = z.object({
    rounds: z.number().int().min(1).optional(),
    refreshRate: z.number().int().min(0).optional(),
})

export type PreRunFormSchema = z.infer<typeof preRunFormSchema>;

export type ControlBarProps = {

}

export default function ControlBar({
}: ControlBarProps) {

    const { register, handleSubmit, formState: { errors } } = useForm<PreRunFormSchema>({
        resolver: zodResolver(preRunFormSchema)
    });

    const handlePreRunFormSubmit = (data: PreRunFormSchema) => {
        console.log(data);
    }

    const handlePreRunFormSubmitBuilder = (oneRound: boolean) => {
        return (data: PreRunFormSchema) => {
            if (oneRound) data.rounds = 1;
            if (!data.refreshRate) data.refreshRate = 0;
            return handlePreRunFormSubmit(data);
        }
    }

    return (
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
                />
            </div>
        </div>
    )
}