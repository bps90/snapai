"use client";
import CodeBlock from '@/components/CodeBlock';
import { Dialog, DialogPanel, DialogTitle, Transition, TransitionChild } from '@headlessui/react';
import { Button } from '@mui/material';
import clsx from 'clsx';
import { createContext, useContext, useState, ReactNode, Fragment } from 'react';

type ErrorModalContextType = {
    showModal: (message: string | React.ReactNode, title?: string | React.ReactNode) => void;
};

const ErrorModalContext = createContext<ErrorModalContextType | undefined>(undefined);

export function useErrorModal() {
    const context = useContext(ErrorModalContext);
    if (!context) {
        throw new Error('useModal precisa estar dentro de ModalProvider');
    }
    return context;
}

export function ErrorModalProvider({ children }: { children: ReactNode }) {
    const [isOpen, setIsOpen] = useState(false);
    const [errorMessage, setMessage] = useState<string | React.ReactNode>('');
    const [errorTitle, setErrorTitle] = useState<string | React.ReactNode>('Error')

    const showModal = (msg: string | React.ReactNode, title: string | React.ReactNode = 'Error') => {
        setMessage(msg);
        setErrorTitle(title);
        setIsOpen(true);
    };

    const closeModal = () => {
        setIsOpen(false);
    };

    return (
        <ErrorModalContext.Provider value={{ showModal }}>
            {children}
            <Transition appear show={isOpen} as={Fragment}>
                <Dialog as="div" className="relative z-50" onClose={closeModal}>
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
                                <DialogPanel className="w-full max-w-3xl transform overflow-hidden rounded-2xl bg-white p-6 shadow-xl transition-all">
                                    {errorTitle && <DialogTitle className={clsx('text-xl', 'font-medium', 'leading-6', 'text-red-600')}>{errorTitle}</DialogTitle>}

                                    <div className="mt-2 overflow-x-auto w-full">
                                        <CodeBlock boxAttr={{ className: clsx('bg-red-50', 'w-full'), }} code={errorMessage} />
                                    </div>

                                    <div className="mt-4">
                                        <Button
                                            type="button"
                                            variant="contained"
                                            color="inherit"
                                            onClick={closeModal}
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
        </ErrorModalContext.Provider>
    );
}
