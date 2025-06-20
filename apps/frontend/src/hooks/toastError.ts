import { toast } from "sonner";

export const toastError = (message: string, description?: string) => {
    toast.error(message, { description: description ?? 'See console for more details' });
};