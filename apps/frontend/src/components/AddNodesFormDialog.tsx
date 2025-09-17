import { Dialog, DialogPanel, DialogTitle, Transition, TransitionChild } from "@headlessui/react";
import clsx from "clsx";
import { Fragment } from "react";
import AddNodesForm from "./form/AddNodesForm";
import { Button } from "@mui/material";

export type AddNodeFormDialogProps = {
    open: boolean;
    onClose: () => void;
    onSubmit: () => void;
}

export default function AddNodeFormDialog(
    { open, onClose, onSubmit }: AddNodeFormDialogProps
) {
    return (
        <Transition appear show={open} as={Fragment}>
            <Dialog as="div" className="relative z-50" onClose={onClose}>
                <TransitionChild
                    as={Fragment}
                    enter="ease-out duration-300"
                    enterFrom="opacity-0"
                    enterTo="opacity-100"
                    leave="ease-in duration-200"
                    leaveFrom="opacity-100"
                    leaveTo="opacity-0"
                >
                    <div className="fixed inset-0 bg-black/25" />
                </TransitionChild>

                <div className="fixed inset-0 overflow-y-auto">
                    <div className="flex min-h-full items-center justify-center p-4">
                        <TransitionChild
                            as={Fragment}
                            enter="ease-out duration-300"
                            enterFrom="opacity-0 scale-95"
                            enterTo="opacity-100 scale-100"
                            leave="ease-in duration-200"
                            leaveFrom="opacity-100 scale-100"
                            leaveTo="opacity-0 scale-95"
                        >
                            <DialogPanel className="w-full max-w-5xl transform overflow-hidden rounded-2xl bg-stone-50 p-6 shadow-xl transition-all">
                                <DialogTitle className={clsx('text-xl', 'font-medium', 'leading-6')}>Add a new Batch of Nodes</DialogTitle>

                                <div className="mt-2 overflow-x-auto w-full">
                                    <AddNodesForm onSubmit={onSubmit} />
                                </div>

                                <div className="mt-4">
                                    <Button
                                        type="button"
                                        variant="contained"
                                        color="inherit"
                                        onClick={onClose}
                                    >
                                        Fechar
                                    </Button>
                                </div>
                            </DialogPanel>
                        </TransitionChild>
                    </div>
                </div>
            </Dialog>
        </Transition>
    );
}