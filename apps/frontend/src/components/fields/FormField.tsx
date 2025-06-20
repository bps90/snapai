import { Field } from "@/lib/fetchers"
import TextField, { TextField as TextFieldType } from "./TextField"
import { HTMLAttributes } from "react"
import { Control, UseFormRegister } from "react-hook-form"
import { ConfigFormSchema } from "../ConfigForm"
import NumberField, { NumberField as NumberFieldType } from "./NumberField"
import CheckboxField, { CheckboxField as CheckboxFieldType } from "./CheckboxField"
import NumberPairField, { NumberPairField as NumberPairFieldType } from "./NumberPairField"

export type FormFieldProps = {
    field: Field
    fieldIndex: number,
    containerAttr?: HTMLAttributes<HTMLDivElement>,
    register: UseFormRegister<ConfigFormSchema>,
    control: Control<ConfigFormSchema>
}

export default function FormField({
    field,
    ...fieldAttrs
}: FormFieldProps) {
    switch (field.type) {
        case 'text':
            return <TextField field={field as TextFieldType} {...fieldAttrs} />
        case 'number':
            return <NumberField field={field as NumberFieldType} {...fieldAttrs} />
        case 'checkbox':
            return <CheckboxField field={field as CheckboxFieldType} {...fieldAttrs} />
        case 'number_pair':
            return <NumberPairField field={field as NumberPairFieldType} {...fieldAttrs} />
    }
}